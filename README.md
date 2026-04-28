# 🕵️ AI-Haklab
**AI-Haklab** es un agente de pentesting autónomo diseñado para correr en dispositivos móviles mediante Termux. Utiliza el motor de **Shell-GPT** potenciado por **Google Gemini 1.5 Flash** e integrado profundamente con la suite **i-Haklab**.

## 🚀 Características
- **Ejecución Autónoma:** Capacidad para realizar escaneos, análisis y reportes sin intervención manual constante.
- **Integración Nativa:** Acceso directo a `nmap`, `metasploit`, `sqlmap` y más herramientas de i-Haklab.
- **Optimizado para Móvil:** Configurado para manejar las limitaciones de recursos y renderizado de Android.
- **Inteligencia Gemini:** Basado en el modelo más rápido y eficiente de Google para respuestas técnicas precisas.

## 🛠️ Requisitos
- Termux (última versión).
- i-Haklab suite instalada.
- API Key de Google Gemini.
- Proot-Distro (Debian).

## 📥 Instalación
1. Descarga el lanzador:
   ```bash
   curl -O https://raw.githubusercontent.com/[TU-USUARIO]/AI-Haklab/main/ai-haklab.sh
   chmod +x ai-haklab.sh
   ```
2. Ejecuta:
   ```bash
   ./ai-haklab.sh
   ```

## 📖 Uso
Habla con AI-Haklab en lenguaje natural:
- *"Escanea mi red local en busca de puertos 80 y 443."*
- *"Analiza este binario en busca de vulnerabilidades de buffer overflow."*

---
Desarrollado con ❤️ para la comunidad de seguridad móvil.
