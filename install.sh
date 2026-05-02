#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  AI-Haklab Pro — Professional Installer
# ============================================================

set -e # Salir en caso de error

# ── Colores ──────────────────────────────────────────────────
BLUE='\033[0;34m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${BLUE}[*] Iniciando instalación de AI-Haklab Pro v2.0...${NC}"

# ── PASO 1: Crear estructura ──────────────────────────────────
mkdir -p ~/.ai-haklab/src
mkdir -p ~/.ai-haklab/config
mkdir -p ~/.local/bin
mkdir -p ~/AI-Haklab-Reports

# ── PASO 2: Copiar archivos ───────────────────────────────────
echo -e "${BLUE}[*] Sincronizando scripts y recursos...${NC}"
cp src/*.py ~/.ai-haklab/src/
cp src/menu.sh ~/.ai-haklab/src/
cp config/* ~/.ai-haklab/config/ 2>/dev/null || true
cp ai-haklab.sh ~/ai-haklab.sh

# Configuración base si no existe
if [ ! -f ~/.ai-haklab/config.json ]; then
    cp config/config.json.example ~/.ai-haklab/config.json 2>/dev/null || \
    echo '{"current_provider": "gemini", "providers": {"gemini": {"name": "Google Gemini", "api_key": "", "model": "gemini-1.5-flash", "base_url": "google"}}}' > ~/.ai-haklab/config.json
fi

# ── PASO 3: Permisos y Enlaces ───────────────────────────────
chmod +x ~/ai-haklab.sh
ln -sf ~/ai-haklab.sh ~/.local/bin/AI-Haklab

# ── PASO 4: Instalar Dependencias Python ──────────────────────
echo -e "${BLUE}[*] Instalando dependencias de Python...${NC}"
pip install -r requirements.txt --quiet

echo -e "${GREEN}[+] Instalación completada exitosamente.${NC}"
echo -e "    Usa el comando: ${BLUE}AI-Haklab${NC} para empezar."
