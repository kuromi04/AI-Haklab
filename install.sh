#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  AI-Haklab Pro — Professional Installer
# ============================================================

set -e # Salir en caso de error

# ── Colores ──────────────────────────────────────────────────
BLUE='\033[0;34m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${BLUE}[*] Iniciando instalación y actualización de AI-Haklab Pro v17.5...${NC}"

# ── PASO 1: Crear estructura ──────────────────────────────────
mkdir -p ~/.ai-haklab/src
mkdir -p ~/.ai-haklab/config
mkdir -p ~/.ai-haklab/skills
mkdir -p ~/.ai-haklab/knowledge
mkdir -p ~/.ai-haklab/playbooks
mkdir -p ~/.local/bin
mkdir -p ~/AI-Haklab-Reports

# ── PASO 2: Sincronizar archivos y módulos ────────────────────
echo -e "${BLUE}[*] Sincronizando scripts, skills y base de conocimientos...${NC}"
cp -r src/* ~/.ai-haklab/src/ 2>/dev/null || true
cp -r config/* ~/.ai-haklab/config/ 2>/dev/null || true
cp -r skills/* ~/.ai-haklab/skills/ 2>/dev/null || true
if [ -d "knowledge" ] && [ "$(ls -A knowledge 2>/dev/null)" ]; then
    cp -r knowledge/* ~/.ai-haklab/knowledge/ 2>/dev/null || true
fi
cp ai-haklab.sh ~/ai-haklab.sh

# Configuración base si no existe
if [ ! -f ~/.ai-haklab/config.json ]; then
    if [ -f config/config.json.example ]; then
        cp config/config.json.example ~/.ai-haklab/config.json
    else
        echo '{"current_provider": "gemini", "providers": {"gemini": {"name": "Google Gemini", "api_key": "", "model": "gemini-2.0-flash-lite", "base_url": "google"}}}' > ~/.ai-haklab/config.json
    fi
fi

# ── PASO 3: Permisos y Enlaces ───────────────────────────────
chmod +x ~/Projects/AI-Haklab-Repo/ai-haklab.sh 2>/dev/null || chmod +x ~/ai-haklab.sh
ln -sf ~/Projects/AI-Haklab-Repo/ai-haklab.sh ~/.local/bin/AI-Haklab

# ── PASO 4: Instalar Dependencias Python ──────────────────────
echo -e "${BLUE}[*] Instalando dependencias de Python...${NC}"
if [ -f requirements.txt ]; then
    pip install -r requirements.txt --quiet 2>/dev/null || true
fi

if ! command -v termux-speech-to-text &>/dev/null; then
    echo -e "${BLUE}[i] Nota: Para usar la entrada por voz (/voice), instala el paquete en Termux: pkg install termux-api${NC}"
fi

echo -e "${GREEN}[+] Instalación y actualización completadas exitosamente.${NC}"
echo -e "    Usa el comando: ${BLUE}AI-Haklab${NC} para empezar."

