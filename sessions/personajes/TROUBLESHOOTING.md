# Troubleshooting Guide - Jesus Sincero Bot

Este documento contém soluções para problemas comuns encontrados durante o desenvolvimento e operação do bot.

---

## 🔴 ERRO: 401 Unauthorized

### Sintomas
```
❌ Twitter API error (401): Unauthorized
```

### Causa Principal (MAIS COMUM)
**Variáveis de ambiente NÃO exportadas para subprocessos Python.**

O comando `source .env` carrega variáveis no shell atual, mas **NÃO** as exporta para subprocessos. Quando o Python roda, ele não consegue ver essas variáveis via `os.environ.get()`.

### Solução
Use `set -a` (auto-export) antes de `source .env`:

```bash
# ❌ ERRADO - Python não consegue ver as variáveis
source .env
python3 scripts/post_jesus.py "texto"

# ✅ CORRETO - Python consegue ver as variáveis
set -a          # Ativa auto-export
source .env     # Carrega E exporta variáveis
set +a          # Desativa auto-export
python3 scripts/post_jesus.py "texto"
```

### Outras Causas Possíveis
1. **Tokens revogados/expirados** - Regenere no Twitter Developer Portal
2. **Credenciais incorretas no .env** - Verifique se copiou corretamente
3. **Permissões da app** - Deve ser "Read and Write" no Twitter

---

## 🔴 ERRO: 403 Forbidden

### Sintomas
```
❌ Twitter API error (403): Forbidden
Authenticating with OAuth 2.0 Application-Only is forbidden for this endpoint.
```

### Causa
Você está usando **OAuth 2.0 Bearer Token (App-Only)** em vez de **OAuth 1.0a User Context**.

Bearer tokens (App-Only) NÃO podem postar tweets. Apenas OAuth 1.0a User Context pode.

### Solução
Use as credenciais OAuth 1.0a:
- Consumer Key
- Consumer Secret
- Access Token
- Access Token Secret

**NÃO use:**
- Bearer Token
- Client ID
- Client Secret

---

## 🔴 ERRO: No module named 'requests_oauthlib'

### Sintomas
```
ModuleNotFoundError: No module named 'requests_oauthlib'
```

### Causa
O ambiente virtual (venv) não está ativado ou a biblioteca não está instalada.

### Solução
```bash
cd /home/ubuntu/clawd/sessions/personajes
source venv/bin/activate
pip install requests_oauthlib python-dotenv
```

---

## 🔴 ERRO: No post for DATE @ TIME

### Sintomas
```
⚠️ No post for 2026-02-05 @ 09:00
```

### Causa
O arquivo `data/posts_current.json` não contém um post para a data e hora especificadas.

### Solução
1. Verifique se o arquivo existe: `cat data/posts_current.json`
2. Verifique se há posts para a data de hoje
3. Gere novos posts: `bash scripts/batch-generator.sh`

---

## 🔴 ERRO: Posts file not found

### Sintomas
```
❌ Posts file not found: data/posts_current.json
```

### Causa
O arquivo de posts não existe ou o caminho está errado.

### Solução
```bash
cd /home/ubuntu/clawd/sessions/personajes
bash scripts/batch-generator.sh
```

---

## 🔴 ERRO: NameResolutionError / DNS

### Sintomas
```
Failed to resolve 'api.twitter.com'
NameResolutionError
```

### Causa
DNS instável no host (resolver local falhando).

### Solução (runtime)
```bash
resolvectl query api.twitter.com
sudo resolvectl dns enp39s0 1.1.1.1 8.8.8.8
sudo resolvectl domain enp39s0 ~.
sudo resolvectl flush-caches
```

### Healthcheck diário
```bash
cat /home/ubuntu/clawd/sessions/personajes/logs/healthcheck.log
cat /home/ubuntu/clawd/sessions/personajes/logs/error.log
```

---

## 🔴 Cron não está postando

### Checklist
1. **Cron está ativo?**
   ```bash
   crontab -l | grep personajes
   ```

2. **O cron ativa o venv?**
   ```bash
   # Deve conter: source venv/bin/activate
   ```

3. **Logs mostram erros?**
   ```bash
   tail -f logs/posting.log
   cat logs/error.log
   ```

4. **Permissões dos scripts?**
   ```bash
   chmod +x scripts/*.sh scripts/*.py
   ```

---

## 📋 Checklist de Diagnóstico

Quando algo não funciona, verifique nesta ordem:

1. **[ ] Venv ativado?** `source venv/bin/activate`
2. **[ ] Variáveis exportadas?** `set -a && source .env && set +a`
3. **[ ] Credenciais no .env?** `cat .env | grep TWITTER`
4. **[ ] Posts existem?** `cat data/posts_current.json | jq '.posts | length'`
5. **[ ] Scripts executáveis?** `ls -la scripts/`
6. **[ ] Teste manual funciona?** `bash scripts/test-single-post.sh "Teste"`

---

## 🧪 Teste Manual Completo

```bash
cd /home/ubuntu/clawd/sessions/personajes

# 1. Ativar venv
source venv/bin/activate

# 2. Exportar variáveis (CRÍTICO!)
set -a
source .env
set +a

# 3. Verificar variáveis carregadas
echo "Consumer Key: ${TWITTER_CONSUMER_KEY:0:10}..."
echo "Access Token: ${TWITTER_ACCESS_TOKEN:0:20}..."

# 4. Testar post
python3 scripts/post_jesus.py "Teste de conexão - $(date)"
```

---

## 📝 Histórico de Bugs Resolvidos

### 2026-02-05: 401 Unauthorized persistente
**Problema:** Scripts retornavam 401 mesmo com credenciais corretas.
**Causa:** `source .env` não exporta variáveis para subprocessos.
**Solução:** Usar `set -a && source .env && set +a`.
**Tempo para resolver:** ~45 minutos de debug.
**Lição:** SEMPRE usar `set -a` ao carregar .env para scripts Python.

---

## 🔗 Links Úteis

- [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [Twitter API v2 Docs](https://developer.twitter.com/en/docs/twitter-api)
- [requests_oauthlib Docs](https://requests-oauthlib.readthedocs.io/)

---

**Última atualização:** 2026-02-05
**Autor:** Opus 4.5 (Akira Master)
