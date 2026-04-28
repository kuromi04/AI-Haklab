import sys
import os
import json
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

# AI-Haklab Pro v15.6 - Minimalist Hacker Edition
console = Console()

BANNER = r"""
    ___    _____         _    _       _    _       _     
   / _ \  |_   _|       | |  | |     | |  | |     | |    
  / /_\ \   | |   ---   | |_| | __ _| | _| | __ _| |__  
 / /   \ \  | |         |  _  |/ _` | |/ / |/ _` | '_ \ 
/_/     \_\_| |_        | | | | (_| |   <| | (_| | |_) |
                   _____|_| |_|\__,_|_|\_\_|\__,_|_.__/ 
                  |______|                             
   [bold blue]AI-HAKLAB - Professional Pentesting Agent v15.6[/bold blue]
"""

CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
TOOLS_LIST_PATH = "/data/data/com.termux/files/home/.local/etc/i-Haklab/Tools/listoftools"

def get_stats():
    try:
        with open(TOOLS_LIST_PATH, 'r') as f:
            all_tools = [l.strip() for l in f if l.strip()]
        inst = sum(1 for t in all_tools if subprocess.getstatusoutput(f"which {t}")[0] == 0)
        return inst, len(all_tools)
    except: return 0, 0

def load_config():
    with open(CONFIG_PATH, 'r') as f: return json.load(f)

config = load_config()
p_data = config['providers'][config['current_provider']]
api_key = p_data['api_key']

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
    SYSTEM_PROMPT += f"\n\nArsenal: {inst}/{tot}. Si falta algo: 'i-Haklab install <tool>'."

def chat():
    console.print(Text.from_markup(BANNER, justify="center"))
    console.print(Panel(f"[bold cyan]i-Haklab Hub:[/bold cyan] [bold green]{inst}[/bold green]/[bold blue]{tot}[/bold blue]", border_style="blue", padding=(0, 2)))
    
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
            
            # Animación de carga minimalista y "pro"
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
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"[bold red][!] ERROR:[/bold red] {str(e)}")

if __name__ == "__main__":
    chat()
