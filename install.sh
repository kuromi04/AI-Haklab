#!/data/data/com.termux/files/usr/bin/bash

echo -e "\e[1;34m[*] Iniciando instalación de AI-Haklab Pro...\e[0m"

# Directorios necesarios
mkdir -p ~/.ai-haklab
mkdir -p ~/.local/bin

# Copiar archivos al sistema
cp .ai-haklab-motor.py ~/.ai-haklab-motor.py
cp ai-haklab.sh ~/ai-haklab.sh
cp system_message.txt ~/.ai-haklab/system_message.txt
cp menu.sh ~/.ai-haklab/menu.sh
[ ! -f ~/.ai-haklab/config.json ] && cp config.json ~/.ai-haklab/config.json

# Permisos
chmod +x ~/ai-haklab.sh
chmod +x ~/.ai-haklab/menu.sh

# Crear comando universal
ln -sf ~/ai-haklab.sh ~/.local/bin/AI-Haklab

# Detectar shell y agregar PATH
if [[ "$SHELL" == *"fish"* ]]; then
    mkdir -p ~/.config/fish/conf.d
    echo "set -gx PATH \$HOME/.local/bin \$PATH" > ~/.config/fish/conf.d/ai-haklab_path.fish
else
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc 2>/dev/null
fi

echo -e "\e[1;32m[+] Instalación completada con éxito.\e[0m"
echo -e "\e[1;36m[!] Ejecuta 'AI-Haklab /menu' para configurar tu API Key.\e[0m"
