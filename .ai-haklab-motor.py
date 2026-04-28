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

# AI-Haklab Pro v16.0 - Cyber-Guardian Edition
console = Console()

BANNER = r"""
    ___    _____         _    _       _    _       _     
   / _ \  |_   _|       | |  | |     | |  | |     | |    
  / /_\ \   | |   ---   | |_| | __ _| | _| | __ _| |__  
 / /   \ \  | |         |  _  |/ _` | |/ / |/ _` | '_ \ 
/_/     \_\_| |_        | | | | (_| |   <| | (_| | |_) |
                   _____|_| |_|\__,_|_|\_\_|\__,_|_.__/ 
                  |______|                             
   [bold blue]AI-HAKLAB - Advanced Cyber-Guardian v16.0[/bold blue]
"""

CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
REPORTS_DIR = "/data/data/com.termux/files/home/AI-Haklab-Reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def speak(text):
    """Integración con Termux TTS"""
    try:
        clean_text = text.replace('`', '').replace('*', '')
        subprocess.run(['termux-tts-speak', clean_text], stderr=subprocess.DEVNULL)
    except: pass

def save_report(history):
    """Genera reporte en Markdown"""
    filename = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, 'w') as f:
        f.write(f"# AI-Haklab Audit Report\nDate: {datetime.now()}\n\n")
        for msg in history:
            role = msg['role'].upper()
            f.write(f"### {role}\n{msg['content']}\n\n")
    return path

def get_stats():
    TOOLS_LIST_PATH = "/data/data/com.termux/files/home/.local/etc/i-Haklab/Tools/listoftools"
    try:
        with open(TOOLS_LIST_PATH, 'r') as f:
            all_tools = [l.strip() for l in f if l.strip()]
        inst = sum(1 for t in all_tools if subprocess.getstatusoutput(f"which {t}")[0] == 0)
        return inst, len(all_tools)
    except: return 0, 0

# Cargar Config
with open(CONFIG_PATH, 'r') as f: config = json.load(f)
p_data = config['providers'][config['current_provider']]
api_key = p_data['api_key']

# Motores
if p_data['base_url'] == "google":
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(p_data['model'])
    engine_type = "gemini"
else:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=p_data['base_url'])
    engine_type = "openai"

inst, tot = get_stats()
system_message_path = "/data/data/com.termux/files/home/.ai-haklab/system_message.txt"
with open(system_message_path, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

def chat():
    console.print(Text.from_markup(BANNER, justify="center"))
    console.print(Panel(f"[bold cyan]i-Haklab Hub:[/bold cyan] [bold green]{inst}[/bold green]/[bold blue]{tot}[/bold blue] | [bold yellow]Voz: Activa[/bold yellow]", border_style="blue"))
    speak("Sistema AI Haklab iniciado. Arsenal de ivam tres cargado.")
    
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        try:
            prompt = "\n[bold blue]┌──[[/bold blue][bold white]root@ai-haklab[/bold white][bold blue]]\n└─# [/bold blue]"
            user_input = console.input(prompt)
            
            if not user_input.strip(): continue
            if user_input.lower() in ['salir', 'exit', 'quit']:
                path = save_report(history)
                speak("Sesión finalizada. Reporte guardado.")
                console.print(f"[bold green][+] Reporte generado en: {path}[/bold green]")
                break
                
            history.append({"role": "user", "content": user_input})
            full_response = ""
            
            with Live(console=console, refresh_per_second=12) as live:
                live.update(Spinner("dots", text="[bold cyan] ENCRIPTANDO...[/bold cyan]", style="cyan"))
                
                if engine_type == "gemini":
                    stream = model.generate_content(history[-1]['content'], stream=True)
                else:
                    stream = client.chat.completions.create(model=p_data['model'], messages=history, stream=True)
                
                for chunk in stream:
                    content = ""
                    if engine_type == "gemini":
                        try: content = chunk.text
                        except: pass
                    else:
                        if chunk.choices[0].delta.content: content = chunk.choices[0].delta.content
                    
                    full_response += content
                    live.update(Panel(Text(full_response, style="bold green"), title=f"[bold blue]{p_data['name']}[/bold blue]", border_style="blue"))
            
            history.append({"role": "assistant", "content": full_response})
            # Dictar puntos clave si la respuesta es corta o resumirla
            if len(full_response) < 300: speak(full_response)
            else: speak("Análisis completado. Revise los resultados en pantalla.")
            
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"[bold red][!] ERROR:[/bold red] {str(e)}")

if __name__ == "__main__":
    chat()
