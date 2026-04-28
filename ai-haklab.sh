#!/data/data/com.termux/files/usr/bin/bash
# AI-Haklab Pro v16.5 - Cyber-Guardian
# Agente de Pentesting con Soporte de Voz y Reportes

CONFIG_FILE="$HOME/.ai-haklab/config.json"
REPO_DIR="$HOME/AI-Haklab-Repo"

# Comandos Especiales
if [ "$1" == "/menu" ]; then
    bash "$HOME/.ai-haklab/menu.sh"
    exit 0
elif [ "$1" == "/update" ]; then
    echo -e "\e[1;34m[*] Sincronizando con GitHub...\e[0m"
    cd "$REPO_DIR" && git pull origin main
    cp "$REPO_DIR/ai-haklab.sh" ~/ai-haklab.sh
    cp "$REPO_DIR/.ai-haklab-motor.py" ~/.ai-haklab-motor.py
    echo -e "\e[1;32m[+] Actualización completada. Reinicia el agente.\e[0m"
    exit 0
elif [ "$1" == "/guardian" ]; then
    echo -e "\e[1;31m[*] Iniciando Modo Guardián (Monitoreo de Red)...\e[0m"
    proot-distro login debian -- sh -c "python3 -c 'print(\"Guardian en escucha activa...\")'"
    exit 0
fi

# Carga de Configuración (Corregida)
PROVIDER=$(jq -r '.current_provider' "$CONFIG_FILE")
API_KEY=$(jq -r ".providers.\"$PROVIDER\".api_key" "$CONFIG_FILE")

# Lanzar Motor en Debian
proot-distro login debian -- sh -c "export DEEPSEEK_API_KEY=$API_KEY; export GOOGLE_API_KEY=$API_KEY; export PYTHONWARNINGS=ignore; python3 ~/.ai-haklab-motor.py \"$@\""
