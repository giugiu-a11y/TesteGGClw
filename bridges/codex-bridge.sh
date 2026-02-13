#!/bin/bash
# Codex Bridge - Ponte para controlar Codex CLI via tmux
# Uso: ./codex-bridge.sh "seu prompt aqui"
#      ./codex-bridge.sh --status
#      ./codex-bridge.sh --kill

SOCKET="/tmp/codex-bridge.sock"
SESSION="codex-bridge"
WORKDIR="${CODEX_WORKDIR:-/home/ubuntu/projects}"

# Ensure codex command is in PATH, especially when running in tmux/subshells
export PATH="$PATH:/home/ubuntu/.npm-global/bin"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

start_session() {
    if ! tmux -S "$SOCKET" has-session -t "$SESSION" 2>/dev/null; then
        echo -e "${YELLOW}Iniciando sessão Codex...${NC}"
        tmux -S "$SOCKET" new-session -d -s "$SESSION" -c "$WORKDIR"
        sleep 0.5
        # Inicia o Codex em modo interativo
        tmux -S "$SOCKET" send-keys -t "$SESSION" "cd $WORKDIR && codex" Enter
        sleep 2
        echo -e "${GREEN}Sessão Codex iniciada em $WORKDIR${NC}"
    fi
}

get_output() {
    local lines="${1:-100}"
    tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION" -S -"$lines" 2>/dev/null
}

send_message() {
    local msg="$1"
    
    # Garante sessão ativa
    start_session
    
    # Captura estado antes
    local before_lines=$(get_output 500 | wc -l)
    
    # Envia mensagem (split text + Enter para TUI - delay maior para Codex)
    tmux -S "$SOCKET" send-keys -t "$SESSION" -l -- "$msg"
    sleep 0.5
    tmux -S "$SOCKET" send-keys -t "$SESSION" Enter
    sleep 0.5
    tmux -S "$SOCKET" send-keys -t "$SESSION" Enter
    
    # Aguarda resposta (poll até output estabilizar ou timeout)
    local timeout=120
    local interval=2
    local elapsed=0
    local last_lines=0
    local stable_count=0
    
    echo -e "${YELLOW}Aguardando resposta do Codex...${NC}" >&2
    
    while [ $elapsed -lt $timeout ]; do
        sleep $interval
        elapsed=$((elapsed + interval))
        
        local current_output=$(get_output 500)
        local current_lines=$(echo "$current_output" | wc -l)
        
        # Verifica se output estabilizou (mesmo número de linhas por 3 checks)
        if [ "$current_lines" -eq "$last_lines" ]; then
            stable_count=$((stable_count + 1))
            if [ $stable_count -ge 2 ]; then
                # Verifica se tem prompt de volta (❯ ou >)
                if echo "$current_output" | tail -5 | grep -qE '(❯|^>|^\$)'; then
                    break
                fi
            fi
        else
            stable_count=0
        fi
        
        last_lines=$current_lines
    done
    
    # Retorna output novo
    get_output 500
}

status() {
    if tmux -S "$SOCKET" has-session -t "$SESSION" 2>/dev/null; then
        echo -e "${GREEN}Sessão Codex ATIVA${NC}"
        echo -e "${YELLOW}Último output:${NC}"
        get_output 30
    else
        echo -e "${RED}Sessão Codex INATIVA${NC}"
    fi
}

kill_session() {
    if tmux -S "$SOCKET" has-session -t "$SESSION" 2>/dev/null; then
        tmux -S "$SOCKET" kill-session -t "$SESSION"
        echo -e "${GREEN}Sessão Codex encerrada${NC}"
    else
        echo -e "${YELLOW}Nenhuma sessão ativa${NC}"
    fi
}

# Main
case "$1" in
    --status|-s)
        status
        ;;
    --kill|-k)
        kill_session
        ;;
    --output|-o)
        get_output "${2:-100}"
        ;;
    --help|-h)
        echo "Codex Bridge - Ponte para Codex CLI"
        echo ""
        echo "Uso:"
        echo "  $0 \"prompt\"     Envia prompt para o Codex"
        echo "  $0 --status      Verifica status da sessão"
        echo "  $0 --output [n]  Mostra últimas n linhas (default 100)"
        echo "  $0 --kill        Encerra sessão"
        echo ""
        echo "Variáveis:"
        echo "  CODEX_WORKDIR    Diretório de trabalho (default: /home/ubuntu/projects)"
        ;;
    "")
        echo "Erro: prompt necessário"
        echo "Uso: $0 \"seu prompt aqui\""
        exit 1
        ;;
    *)
        send_message "$*"
        ;;
esac
