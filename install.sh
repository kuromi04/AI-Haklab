#!/data/data/com.termux/files/usr/bin/bash
echo -e "\e[1;34m[*] Instalando Estructura AI-Haklab Pro...\e[0m"

mkdir -p ~/.ai-haklab/src
mkdir -p ~/.ai-haklab/config
mkdir -p ~/.local/bin

cp src/* ~/.ai-haklab/src/
cp config/system_prompt.txt ~/.ai-haklab/config/
cp ai-haklab.sh ~/ai-haklab.sh
[ ! -f ~/.ai-haklab/config.json ] && cp config/config.json.example ~/.ai-haklab/config.json

chmod +x ~/ai-haklab.sh
ln -sf ~/ai-haklab.sh ~/.local/bin/AI-Haklab

echo -e "\e[1;32m[+] Proyecto reestructurado y listo.\e[0m"
