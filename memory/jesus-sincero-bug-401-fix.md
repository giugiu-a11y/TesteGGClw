# 🚨 BUG CRÍTICO: 401 Unauthorized no Twitter - SOLUÇÃO

**Data:** 2026-02-05
**Projeto:** Jesus Sincero (@jesussemfiltro)
**Resolvido por:** Opus 4.5

---

## O BUG

Scripts Python retornavam **401 Unauthorized** ao tentar postar no Twitter, mesmo com credenciais OAuth 1.0a corretas.

## A CAUSA

O comando `source .env` **NÃO EXPORTA** variáveis de ambiente para subprocessos!

Quando o shell executa:
```bash
source .env          # Carrega variáveis no shell atual
python3 script.py    # Subprocesso - NÃO VÊ as variáveis!
```

O Python (`os.environ.get()`) não consegue ver as variáveis porque elas não foram exportadas.

## A SOLUÇÃO

Usar `set -a` (auto-export) antes de `source .env`:

```bash
set -a          # Ativa auto-export (todas variáveis serão exportadas)
source .env     # Carrega E EXPORTA variáveis
set +a          # Desativa auto-export
python3 script.py   # Agora o Python VÊ as variáveis!
```

## ONDE APLICAR

### 1. Scripts Bash que chamam Python
```bash
# Em post-daily.sh, test-single-post.sh, etc:
set -a
source .env
set +a
python3 scripts/post_jesus.py "$TEXT"
```

### 2. Testes manuais no terminal
```bash
cd /home/ubuntu/clawd/sessions/personajes
source venv/bin/activate
set -a && source .env && set +a
python3 scripts/post_jesus.py "Teste"
```

### 3. Cron jobs
Os cron jobs chamam os scripts bash (post-daily.sh), que já têm `set -a` implementado.

---

## ARQUIVOS CORRIGIDOS

1. `/home/ubuntu/clawd/sessions/personajes/scripts/post-daily.sh` - Adicionado `set -a`
2. `/home/ubuntu/clawd/sessions/personajes/scripts/test-single-post.sh` - Adicionado `set -a`
3. `/home/ubuntu/clawd/sessions/personajes/scripts/post_jesus.py` - Comentários explicativos
4. `/home/ubuntu/clawd/sessions/personajes/TROUBLESHOOTING.md` - Documentação completa
5. `/home/ubuntu/clawd/sessions/personajes/README.md` - Aviso no topo

---

## SINTOMAS DO BUG

- ❌ `401 Unauthorized` persistente
- ❌ Credenciais parecem corretas mas não funcionam
- ❌ Funciona com substituição de shell (`$VAR`) mas não com `os.environ.get()`
- ❌ `tweepy` também falha (mesma causa)

---

## COMO DEBUGAR SE ACONTECER DE NOVO

```bash
# 1. Verificar se variáveis estão no shell
echo $TWITTER_CONSUMER_KEY

# 2. Verificar se variáveis chegam ao Python
python3 -c "import os; print(os.environ.get('TWITTER_CONSUMER_KEY', 'NOT SET'))"

# Se o passo 1 mostra o valor mas o passo 2 mostra "NOT SET", é o bug do export!
# Solução: set -a && source .env && set +a
```

---

## PARA OUTROS LLMs

**SE VOCÊ ESTÁ LENDO ISSO E TEM ERRO 401:**

1. Primeiro verifique se está usando `set -a && source .env && set +a`
2. O `source .env` SOZINHO não funciona para Python
3. Leia `/home/ubuntu/clawd/sessions/personajes/TROUBLESHOOTING.md`

---

## LIÇÕES APRENDIDAS

1. **Shell scripting é traiçoeiro** - `source` não exporta por padrão
2. **Documentação é crucial** - Sem isso, o próximo LLM vai sofrer igual
3. **Testes manuais enganam** - Funcionam no shell mas não em subprocessos
4. **OAuth 1.0a é necessário** - OAuth 2.0 Bearer não posta (403)

---

**Este arquivo deve ser consultado SEMPRE que houver problemas com Twitter API.**
