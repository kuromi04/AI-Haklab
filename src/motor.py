import sys
import os
import json
import subprocess
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from backup import create_backup
from stats_utils import get_stats
from validation_utils import ConfigValidator

# AI-Haklab Pro v17.0 - OODA Tactical Edition
console = Console()

BANNER = r"""
    ___    _____         _    _       _    _       _     
   / _ \  |_   _|       | |  | |     | |  | |     | |    
  / /_\ \   | |   ---   | |_| | __ _| | _| | __ _| |__  
 / /   \ \  | |         |  _  |/ _` | |/ / |/ _` | '_ \ 
/_/     \_\_| |_        | | | | (_| |   <| | (_| | |_) |
                   _____|_| |_|\__,_|_|\_\_|\__,_|_.__/ 
                  |______|                             
   [bold blue]AI-HAKLAB - Tactical Hacker Engine v17.5 [Gentle-AI Powered][/bold blue]
"""

CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
REPORTS_DIR = "/data/data/com.termux/files/home/AI-Haklab-Reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Session Metadata
SESSION_START = datetime.now()

def speak(text):
    try:
        clean = text.replace('`', '').replace('*', '').replace('[', '').replace(']', '')
        subprocess.run(['termux-tts-speak', clean], stderr=subprocess.DEVNULL)
    except: pass

# Cargar y Validar Configuración
validator = ConfigValidator(CONFIG_PATH)
config = validator.validate()

def get_client(provider_key):
    p_data = config['providers'][provider_key]
    api_key = p_data['api_key']
    if not api_key and "free" not in p_data['model']:
        return None, None
    
    from openai import OpenAI
    # Handle non-OpenAI standard libraries if needed
    if p_data['base_url'] == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return "google", p_data
    elif p_data['base_url'] == "anthropic":
        import anthropic
        return "anthropic", p_data
    else:
        return OpenAI(api_key=api_key, base_url=p_data['base_url']), p_data

def select_brain(user_input):
    """SDD Logic: Selects the best brain for the task."""
    recon_keywords = ['scan', 'nmap', 'enum', 'whois', 'recon', 'reconocimiento', 'buscas', 'encuentra', 'dig', 'subfinder']
    is_recon = any(k in user_input.lower() for k in recon_keywords)
    
    if is_recon:
        # Prefer Gemini Flash for Recon (Fast/Lite)
        client, data = get_client('gemini')
        if client: return client, data, "RECON (Gemini)"
        # Fallback to OpenRouter Free
        client, data = get_client('openrouter')
        if client: return client, data, "RECON (Llama-Free)"
    
    # Default/Exploit mode (DeepSeek or current)
    client, data = get_client(config['current_provider'])
    if client: return client, data, f"STRATEGY ({data['name']})"
    
    # Last resort fallback
    client, data = get_client('gemini')
    return client, data, "FALLBACK (Gemini)"

def generate_report(history):
    """Generates a professional tactical report at the end of the session."""
    session_end = datetime.now()
    timestamp = session_end.strftime("%Y%m%d_%H%M%S")
    report_file = f"{REPORTS_DIR}/intrusion_report_{timestamp}.md"
    
    # Metadata and Header
    report_content = f"""# 🛡️ Reporte Táctico de Intrusión
**Operador:** @kuromi04
**Inicio:** {SESSION_START.strftime("%Y-%m-%d %H:%M:%S")}
**Fin:** {session_end.strftime("%Y-%m-%d %H:%M:%S")}
**Duración:** {str(session_end - SESSION_START).split('.')[0]}
**Proveedor:** {config['current_provider']}
**Modelo:** {config['providers'][config['current_provider']]['model']}
**Laboratorio:** i-Haklab (Ivam3)
**Comunidad:** ivam3bycinderella

---

## 📝 Resumen de la Operación
"""
    # Create a summary prompt for the AI
    summary_history = history + [{"role": "user", "content": "Genera un resumen técnico de nuestra sesión de hoy para un reporte profesional. Clasifica las acciones según la metodología MITRE ATT&CK vista en nuestros conocimientos. Sé quirúrgico y breve."}]
    
    # We use the current strategy brain to generate the report
    client, p_data, _ = select_brain("generar reporte")
    
    try:
        if p_data['base_url'] == "google":
            import google.generativeai as genai
            model = genai.GenerativeModel(p_data['model'])
            messages = [{"role": "user", "parts": [m['content']]} for m in summary_history if m['role'] != 'system']
            response = model.generate_content(messages)
            report_content += response.text
        else:
            response = client.chat.completions.create(model=p_data['model'], messages=summary_history, stream=False)
            report_content += response.choices[0].message.content
        
        # Append Full History Logs
        report_content += "\n\n---\n\n## 📋 Registro Cronológico (Logs)\n"
        for msg in history:
            if msg['role'] == 'system': continue
            role_label = "🟢 [OPERADOR]" if msg['role'] == 'user' else "⚪ [ASISTENTE]"
            report_content += f"\n### {role_label}\n{msg['content']}\n"

        with open(report_file, "w") as f:
            f.write(report_content)
        return report_file
    except Exception as e:
        return f"Error al generar reporte: {str(e)}"

def chat():
    # Proactive Backup (Gentle-AI style)
    create_backup("/data/data/com.termux/files/home/.ai-haklab", "/data/data/com.termux/files/home/.ai-haklab/backups")
    
    inst, tot, engram, batt, vpn = get_stats()
    console.print(Text.from_markup(BANNER, justify="center"))
    
    stats_table = f"[bold cyan]Arsenal:[/bold cyan] {inst}/{tot} | [bold magenta]Engram:[/bold magenta] {engram} | [bold yellow]Bat:[/bold yellow] {batt} | [bold blue]VPN:[/bold blue] {vpn}"
    console.print(Panel(stats_table, title="[bold yellow]OODA NODE STATUS[/bold yellow]", border_style="blue"))
    
    speak(f"Nodo activo. Batería al {batt.split(']')[1].split('%')[0] if '%' in batt else 'desconocido'} por ciento. Red {'protegida' if 'SECURED' in vpn else 'expuesta'}. Esperando órdenes.")
    
    with open("/data/data/com.termux/files/home/.ai-haklab/system_message.txt", "r") as f:
        sys_msg = f.read()
    history = [{"role": "system", "content": sys_msg}]
    
    while True:
        try:
            # Prompt de nivel Operador
            prompt = "\n[bold blue]┌──[[/bold blue][bold white]hacker@ai-haklab[/bold white][bold blue]]\n└─# [/bold blue]"
            user_input = console.input(prompt)
            
            if not user_input.strip(): continue
            if user_input.lower() in ['salir', 'exit', 'quit']:
                speak("Operación terminada. Generando reporte táctico basado en MITRE ATT&CK.")
                with console.status("[bold cyan]Compilando inteligencia...[/bold cyan]"):
                    path = generate_report(history)
                console.print(f"[bold green][+] Reporte guardado en:[/bold green] {path}")
                break
            
            # SDD: Selección dinámica del cerebro
            client, p_data, mode_name = select_brain(user_input)
            
            history.append({"role": "user", "content": user_input})
            full_response = ""
            
            with Live(console=console, refresh_per_second=12) as live:
                live.update(Spinner("dots", text=f"[bold cyan] {mode_name.upper()} ANALIZANDO VECTOR...[/bold cyan]", style="cyan"))
                
                if p_data['base_url'] == "google":
                    import google.generativeai as genai
                    model = genai.GenerativeModel(p_data['model'])
                    # Simple conversion for system message
                    messages = [{"role": "user", "parts": [m['content']]} for m in history if m['role'] != 'system']
                    response = model.generate_content(messages, stream=True)
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            live.update(Panel(Text(full_response, style="bold green"), title=f"[bold blue]Brain: {mode_name}[/bold blue]", border_style="blue"))
                else:
                    stream = client.chat.completions.create(model=p_data['model'], messages=history, stream=True)
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            live.update(Panel(Text(full_response, style="bold green"), title=f"[bold blue]Brain: {mode_name}[/bold blue]", border_style="blue"))
            
            history.append({"role": "assistant", "content": full_response})
            if len(full_response) < 200: speak(full_response)
            else: speak(f"Análisis con {p_data['name']} completado. Operador, proceda.")
            
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"[bold red][!] ERROR:[/bold red] {str(e)}")

if __name__ == "__main__":
    chat()
