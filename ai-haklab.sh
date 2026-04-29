#!/data/data/com.termux/files/usr/bin/bash
# AI-Haklab Pro v17.5 - Storage & Maintenance Edition
# Tactical Copilot Entry Point

CONFIG_FILE="$HOME/.ai-haklab/config.json"
MOTOR_PATH="$HOME/.ai-haklab/src/motor.py"
REPO_DIR="$HOME/AI-Haklab-Repo"

# COMANDOS DE GESTIÓN
if [ "$1" == "/menu" ]; then
    bash "$HOME/.ai-haklab/src/menu.sh"
    exit 0
elif [ "$1" == "/update" ]; then
    echo -e "\e[1;34m[*] Sincronizando con el cuartel general (GitHub)...\e[0m"
    cd "$REPO_DIR" && git pull origin main && ./install.sh
    echo -e "\e[1;32m[+] Sistema actualizado.\e[0m"
    exit 0
elif [ "$1" == "/clean" ]; then
    echo -e "\e[1;33m[*] Iniciando purga de archivos temporales...\e[0m"
    rm -rf ~/.cache/pip/* ~/.npm/_cacache/*
    rm -f ~/AI-Haklab-Reports/*.tmp
    echo -e "\e[1;32m[+] Limpieza completada. Espacio liberado.\e[0m"
    exit 0
elif [ "$1" == "/backup" ]; then
    echo -e "\e[1;34m[*] Creando respaldo de configuración...\e[0m"
    mkdir -p ~/storage/downloads/AI-Haklab-Backup
    cp "$CONFIG_FILE" ~/storage/downloads/AI-Haklab-Backup/config_bak.json
    echo -e "\e[1;32m[+] Respaldo guardado en Descargas/AI-Haklab-Backup\e[0m"
    exit 1
elif [ "$1" == "/work" ]; then
    cd ~/i-Haklab-Workspace
    echo -e "\e[1;32m[+] Entrando al Espacio de Trabajo Táctico.\e[0m"
    exec $SHELL
fi

# CARGA DE INTELIGENCIA
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "\e[1;31m[!] Error: Configuración no encontrada. Ejecuta: AI-Haklab /menu\e[0m"
    exit 1
fi

PROVIDER=$(jq -r '.current_provider' "$CONFIG_FILE")
API_KEY=$(jq -r ".providers.\"$PROVIDER\".api_key" "$CONFIG_FILE")

# LANZAR MOTOR OODA
proot-distro login debian -- sh -c "export DEEPSEEK_API_KEY=$API_KEY; export GOOGLE_API_KEY=$API_KEY; export PYTHONWARNINGS=ignore; python3 $MOTOR_PATH \"$@\""
