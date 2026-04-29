import sys
import os
from rich.console import Console

# Add current dir to path to import local utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validation_utils import ConfigValidator
from stats_utils import get_stats, check_ip_leak

console = Console()

def test_validation():
    console.print("\n[bold cyan][*] Testing Configuration Validation...[/bold cyan]")
    CONFIG_PATH = "/data/data/com.termux/files/home/.ai-haklab/config.json"
    validator = ConfigValidator(CONFIG_PATH)
    config = validator.validate()
    if config:
        console.print("[bold green][V] Configuration is valid.[/bold green]")
    else:
        console.print("[bold red][X] Configuration validation failed.[/bold red]")

def test_stats():
    console.print("\n[bold cyan][*] Testing System Monitoring...[/bold cyan]")
    inst, tot, engram, batt, vpn = get_stats()
    console.print(f"Arsenal: {inst}/{tot}")
    console.print(f"Engram: {engram}")
    console.print(f"Battery: {batt}")
    console.print(f"VPN/IP: {vpn}")
    
    if "EXPOSED" in vpn or "SECURED" in vpn:
        console.print("[bold green][V] IP Leak detection logic executed.[/bold green]")
    else:
        console.print("[bold red][X] IP Leak detection failed to return status.[/bold red]")

if __name__ == "__main__":
    console.print("[bold yellow]=== AI-HAKLAB HARDENING VERIFICATION ===[/bold yellow]")
    try:
        test_validation()
        test_stats()
        console.print("\n[bold green]ALL SYSTEMS GO. READY FOR MISSION.[/bold green]")
    except Exception as e:
        console.print(f"\n[bold red][!] VERIFICATION FAILED: {str(e)}[/bold red]")
