import hashlib
import sqlite3
import json
import time
import os

CACHE_DB = os.path.join(os.path.dirname(__file__), 'akira_cache.db')

def get_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def init_db():
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            hash TEXT PRIMARY KEY,
            data TEXT,
            timestamp REAL,
            ttl REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_cache(hash_val, data, ttl_seconds):
    init_db()
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    timestamp = time.time()
    cursor.execute('''
        INSERT OR REPLACE INTO cache (hash, data, timestamp, ttl)
        VALUES (?, ?, ?, ?)
    ''', (hash_val, json.dumps(data), timestamp, ttl_seconds))
    conn.commit()
    conn.close()

def load_cache(hash_val):
    init_db()
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT data, timestamp, ttl FROM cache WHERE hash = ?', (hash_val,))
    result = cursor.fetchone()
    conn.close()

    if result:
        data, timestamp, ttl = result
        if (time.time() - timestamp) < ttl:
            return json.loads(data)
    return None

if __name__ == "__main__":
    init_db() # Ensure DB is initialized when script is run directly for testing or setup
    # Example usage for testing:
    # text = "test content for caching"
    # h = get_hash(text)
    # print(f"Hash: {h}")
    # save_cache(h, {"summary": "This is a test summary."}, 3600) # TTL 1 hour
    # cached_data = load_cache(h)
    # print(f"Cached data: {cached_data}")
