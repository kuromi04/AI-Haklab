import sys
import os
import json
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

# AI-Haklab Pro v15.4 - AI-Arsenal Awareness
console = Console()

# BANNER CORREGIDO: "AI - Haklab"
BANNER = r"""
    ___    _____         _    _       _    _       _     
   / _ \  |_   _|       | |  | |     | |  | |     | |    
  / /_\ \   | |   ---   | |_| | __ _| | _| | __ _| |__  
 / /   \ \  | |         |  _  |/ _` | |/ / |/ _` | '_ \ 
/_/     \_\_| |_        | | | | (_| |   <| | (_| | |_) |
                   _____|_| |_|\__,_|_|\_\_|\__,_|_.__/ 
                  |______|                             
   [bold blue]AI-HAKLAB - Professional Pentesting Agent v15.4[/bold blue]
"""

CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
TOOLS_LIST_PATH = "/data/data/com.termux/files/home/.local/etc/i-Haklab/Tools/listoftools"

def get_arsenal_stats():
    try:
        if not os.path.exists(TOOLS_LIST_PATH):
            return 0, 0
        with open(TOOLS_LIST_PATH, 'r') as f:
            all_tools = [line.strip() for line in f if line.strip()]
        total = len(all_tools)
        installed = 0
        for tool in all_tools:
            if subprocess.getstatusoutput(f"which {tool}")[0] == 0:
                installed += 1
        return installed, total
    except:
        return 0, 0

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

# Cargar configuración y preparar motor
config = load_config()
p_data = config['providers'][config['current_provider']]
api_key = p_data['api_key']

if p_data['base_url'] == "google":
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(p_data['model'])
    engine_type = "gemini"
elif p_data['base_url'] == "anthropic":
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    engine_type = "anthropic"
else:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=p_data['base_url'])
    engine_type = "openai"

installed, total = get_arsenal_stats()
system_message_path = "/data/data/com.termux/files/home/.ai-haklab/system_message.txt"
with open(system_message_path, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()
    SYSTEM_PROMPT += f"\n\nNOTAS DEL LABORATORIO: Tienes {installed}/{total} herramientas de i-Haklab instaladas. Si falta alguna necesaria, usa 'i-Haklab install <tool>'."

def get_stream(history):
    if engine_type == "gemini":
        return model.generate_content(history[-1]['content'], stream=True)
    elif engine_type == "anthropic":
        return client.messages.create(model=p_data['model'], max_tokens=4096, system=SYSTEM_PROMPT, 
                                    messages=[m for m in history if m['role'] != 'system'], stream=True)
    else:
        return client.chat.completions.create(model=p_data['model'], messages=history, stream=True)

def chat():
    console.print(Text.from_markup(BANNER, justify="center"))
    console.print(Panel(f"[bold cyan]i-Haklab Hub:[/bold cyan] [bold green]{installed}[/bold green] instaladas / [bold blue]{total}[/bold blue] disponibles", border_style="blue"))
    console.print(f"[bold blue][+][/bold blue] [bold white]Motor Activo: {p_data['name']}[/bold white]")
    console.print("[bold dim blue]------------------------------------------------------------[/bold dim blue]")
    
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        try:
            prompt = "\n[bold blue]┌──[[/bold blue][bold white]root@ai-haklab[/bold white][bold blue]]\n└─# [/bold blue]"
            user_input = console.input(prompt)
            if not user_input.strip(): continue
            if user_input.lower() in ['salir', 'exit', 'quit', 'clear']:
                if user_input.lower() == 'clear':
                    os.system('clear')
                    console.print(Text.from_markup(BANNER, justify="center"))
                    continue
                break
            
            history.append({"role": "user", "content": user_input})
            full_response = ""
            with Live(console=console, refresh_per_second=10) as live:
                live.update(Panel(Text("ANALIZANDO ARSENAL...", style="bold cyan"), title="[bold blue]STATUS[/bold blue]", border_style="blue"))
                stream = get_stream(history)
                for chunk in stream:
                    content = ""
                    if engine_type == "gemini":
                        try: content = chunk.text
                        except: pass
                    elif engine_type == "anthropic":
                        if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'): content = chunk.delta.text
                    else:
                        if chunk.choices[0].delta.content: content = chunk.choices[0].delta.content
                    full_response += content
                    live.update(Panel(Text(full_response, style="bold green"), title=f"[bold blue]{p_data['name']}[/bold blue]", border_style="blue"))
            history.append({"role": "assistant", "content": full_response})
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"[bold red][!] ERROR:[/bold red] {str(e)}")

if __name__ == "__main__":
    chat()
