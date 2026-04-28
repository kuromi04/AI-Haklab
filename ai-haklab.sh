#!/data/data/com.termux/files/usr/bin/bash
# Lanzador oficial de AI-Haklab
export COPIED_INTERPRETER_SYSTEM_MESSAGE="Eres AI-Haklab, un experto en ciberseguridad..."
proot-distro login debian -- sh -c "interpreter --model gemini/gemini-1.5-flash"
