#!/data/data/com.termux/files/usr/bin/bash
# AI-Haklab Pro v15.0 - Universal Engine
# Agente de Pentesting de Élite para i-Haklab

CONFIG_FILE="$HOME/.ai-haklab/config.json"
MENU_SCRIPT="$HOME/.ai-haklab/menu.sh"

# Si se pide el menú o no hay config, lanzarlo
if [ "$1" == "/menu" ] || [ ! -f "$CONFIG_FILE" ]; then
    bash "$MENU_SCRIPT"
    exit 0
fi

# Cargar configuración para el motor
PROVIDER=$(jq -r '.current_provider' "$CONFIG_FILE")
API_KEY=$(jq -r ".providers.\"$PROVIDER\".api_key" "$CONFIG_FILE")

if [ -z "$API_KEY" ] || [ "$API_KEY" == "null" ]; then
    echo -e "\e[1;31m[!] Error: No hay API KEY para $PROVIDER. Ejecuta: ./ai-haklab.sh /menu\e[0m"
    exit 1
fi

# Ejecutar motor en Debian
proot-distro login debian -- sh -c "export DEEPSEEK_API_KEY=$API_KEY; export GOOGLE_API_KEY=$API_KEY; export PYTHONWARNINGS=ignore; python3 ~/.ai-haklab-motor.py \"$@\""
