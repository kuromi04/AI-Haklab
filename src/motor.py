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
   [bold blue]AI-HAKLAB - Tactical Copilot v17.0 [Gentle-AI Powered][/bold blue]
"""

CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
REPORTS_DIR = "/data/data/com.termux/files/home/AI-Haklab-Reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def speak(text):
    try:
        clean = text.replace('`', '').replace('*', '').replace('[', '').replace(']', '')
        subprocess.run(['termux-tts-speak', clean], stderr=subprocess.DEVNULL)
    except: pass

def get_stats():
    TOOLS_LIST_PATH = "/data/data/com.termux/files/home/.local/etc/i-Haklab/Tools/listoftools"
    try:
        with open(TOOLS_LIST_PATH, 'r') as f:
            tools = [l.strip() for l in f if l.strip()]
        inst = sum(1 for t in tools if subprocess.getstatusoutput(f"which {t}")[0] == 0)
        
        # Check Engram
        engram_status = "[bold green]ON[/bold green]" if subprocess.getstatusoutput("which engram")[0] == 0 else "[bold red]OFF[/bold red]"
        
        return inst, len(tools), engram_status
    except: return 0, 0, "[bold red]ERR[/bold red]"

# Cargar Configuración
with open(CONFIG_PATH, 'r') as f: config = json.load(f)
p_data = config['providers'][config['current_provider']]
api_key = p_data['api_key']

from openai import OpenAI
client = OpenAI(api_key=api_key, base_url=p_data['base_url'])

def chat():
    # Proactive Backup (Gentle-AI style)
    create_backup("/data/data/com.termux/files/home/.ai-haklab", "/data/data/com.termux/files/home/.ai-haklab/backups")
    
    inst, tot, engram = get_stats()
    console.print(Text.from_markup(BANNER, justify="center"))
    console.print(Panel(f"[bold cyan]i-Haklab Hub:[/bold cyan] [bold green]{inst}[/bold green]/[bold blue]{tot}[/bold blue] | [bold yellow]OODA Loop: ACTIVO[/bold yellow] | [bold magenta]Engram:[/bold magenta] {engram}", border_style="blue"))
    speak("Iniciando Copiloto Táctico AI Haklab. Ciclo O O D A activado. Sistema Engram detectado.")
    
    with open("/data/data/com.termux/files/home/.ai-haklab/system_message.txt", "r") as f:
        sys_msg = f.read()
    history = [{"role": "system", "content": sys_msg}]
    
    while True:
        try:
            # Prompt de nivel Piloto
            prompt = "\n[bold blue]┌──[[/bold blue][bold white]pilot@ai-haklab[/bold white][bold blue]]\n└─# [/bold blue]"
            user_input = console.input(prompt)
            
            if not user_input.strip(): continue
            if user_input.lower() in ['salir', 'exit', 'quit']:
                speak("Operación finalizada. Generando reporte de misión.")
                break
                
            history.append({"role": "user", "content": user_input})
            full_response = ""
            
            with Live(console=console, refresh_per_second=12) as live:
                live.update(Spinner("dots", text="[bold cyan] ANALIZANDO VECTOR OODA...[/bold cyan]", style="cyan"))
                stream = client.chat.completions.create(model=p_data['model'], messages=history, stream=True)
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        live.update(Panel(Text(full_response, style="bold green"), title=f"[bold blue]Tactic: {p_data['name']}[/bold blue]", border_style="blue"))
            
            history.append({"role": "assistant", "content": full_response})
            if len(full_response) < 200: speak(full_response)
            else: speak("Análisis táctico completado. Piloto, proceda con la ejecución.")
            
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"[bold red][!] ERROR:[/bold red] {str(e)}")

if __name__ == "__main__":
    chat()
