#!/data/data/com.termux/files/usr/bin/bash
# AI-Haklab Pro v17.0 - Tactical Engine
# Entry point

CONFIG_FILE="$HOME/.ai-haklab/config.json"
MOTOR_PATH="$HOME/.ai-haklab/src/motor.py"

if [ "$1" == "/menu" ]; then
    bash "$HOME/.ai-haklab/src/menu.sh"
    exit 0
fi

# Cargar Configuración
PROVIDER=$(jq -r '.current_provider' "$CONFIG_FILE")
API_KEY=$(jq -r ".providers.\"$PROVIDER\".api_key" "$CONFIG_FILE")

# Lanzar Motor
proot-distro login debian -- sh -c "export DEEPSEEK_API_KEY=$API_KEY; export GOOGLE_API_KEY=$API_KEY; export PYTHONWARNINGS=ignore; python3 $MOTOR_PATH \"$@\""
