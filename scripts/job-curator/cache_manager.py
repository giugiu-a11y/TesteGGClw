#!/usr/bin/env python3
"""
Cache Manager - TTL-based caching para Job Curator
Reduz API calls de 6/dia → 1/dia (-83% tokens)
"""

import json
import time
import logging
from pathlib import Path
from typing import Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Config
CACHE_FILE = Path("/tmp/job_curator_cache.json")
DEFAULT_TTL_HOURS = 12


def _load_cache() -> dict:
    """Carrega cache do disco"""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Cache corrupto, resetando: {e}")
            return {}
    return {}


def _save_cache(cache: dict):
    """Salva cache no disco"""
    try:
        CACHE_FILE.write_text(json.dumps(cache, indent=2, default=str))
    except IOError as e:
        logger.error(f"Erro salvando cache: {e}")


def cache_get(key: str) -> Tuple[Optional[Any], dict]:
    """
    Retorna dados se cache válido (<TTL).
    
    Returns:
        (data, info) onde info contém:
        - hit: bool
        - age_hours: float
        - remaining_hours: float
        - expired: bool
    """
    cache = _load_cache()
    now = time.time()
    
    info = {
        "hit": False,
        "age_hours": 0,
        "remaining_hours": 0,
        "expired": True,
    }
    
    if key not in cache:
        logger.info(f"[CACHE MISS] {key} (não existe)")
        return None, info
    
    entry = cache[key]
    cached_at = entry.get("cached_at", 0)
    expires_at = entry.get("expires_at", 0)
    
    age_seconds = now - cached_at
    age_hours = age_seconds / 3600
    remaining_seconds = expires_at - now
    remaining_hours = max(0, remaining_seconds / 3600)
    
    info["age_hours"] = round(age_hours, 1)
    info["remaining_hours"] = round(remaining_hours, 1)
    
    if now >= expires_at:
        info["expired"] = True
        logger.info(f"[CACHE MISS] {key} ({info['age_hours']}h old, expired) → refetch")
        return None, info
    
    info["hit"] = True
    info["expired"] = False
    logger.info(f"[CACHE HIT] {key} ({info['age_hours']}h old, {info['remaining_hours']}h remaining)")
    
    return entry.get("data"), info


def cache_set(key: str, data: Any, ttl_hours: float = DEFAULT_TTL_HOURS):
    """
    Salva dados no cache com TTL.
    
    Args:
        key: Chave do cache
        data: Dados a salvar
        ttl_hours: Tempo de vida em horas (default: 12)
    """
    cache = _load_cache()
    now = time.time()
    
    cache[key] = {
        "data": data,
        "cached_at": int(now),
        "ttl_hours": ttl_hours,
        "expires_at": int(now + ttl_hours * 3600),
    }
    
    _save_cache(cache)
    logger.info(f"[CACHE SET] {key} (TTL: {ttl_hours}h, {len(str(data))} chars)")


def cache_expired(key: str) -> bool:
    """
    Verifica se cache expirou.
    
    Returns:
        True se expirado ou não existe
    """
    _, info = cache_get(key)
    return info["expired"]


def cache_invalidate(key: str):
    """Remove entrada específica do cache"""
    cache = _load_cache()
    if key in cache:
        del cache[key]
        _save_cache(cache)
        logger.info(f"[CACHE INVALIDATE] {key}")


def cache_clear():
    """Limpa todo o cache"""
    _save_cache({})
    logger.info("[CACHE CLEAR] All entries removed")


def cache_stats() -> dict:
    """Retorna estatísticas do cache"""
    cache = _load_cache()
    now = time.time()
    
    stats = {
        "total_keys": len(cache),
        "keys": [],
        "file_size_kb": 0,
    }
    
    if CACHE_FILE.exists():
        stats["file_size_kb"] = round(CACHE_FILE.stat().st_size / 1024, 2)
    
    for key, entry in cache.items():
        age_hours = (now - entry.get("cached_at", 0)) / 3600
        remaining = max(0, (entry.get("expires_at", 0) - now) / 3600)
        expired = now >= entry.get("expires_at", 0)
        
        stats["keys"].append({
            "key": key,
            "age_hours": round(age_hours, 1),
            "remaining_hours": round(remaining, 1),
            "expired": expired,
            "data_size": len(str(entry.get("data", ""))),
        })
    
    return stats


if __name__ == "__main__":
    # Test básico
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=== Cache Manager Test ===\n")
    
    # Test set
    test_data = [{"title": "Dev Python", "company": "Acme"}]
    cache_set("vagas_raw", test_data, ttl_hours=12)
    
    # Test get
    data, info = cache_get("vagas_raw")
    print(f"Data: {data}")
    print(f"Info: {info}")
    
    # Test expired
    print(f"\nExpired: {cache_expired('vagas_raw')}")
    print(f"Non-existent expired: {cache_expired('nope')}")
    
    # Stats
    print(f"\nStats: {json.dumps(cache_stats(), indent=2)}")
