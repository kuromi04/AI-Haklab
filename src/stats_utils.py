import subprocess
import json
import os

def check_ip_leak():
    """Returns '[SECURED]' or '[EXPOSED]' by checking if the public IP is masked."""
    # Check if VPN interface (tun0) is up
    vpn_check = subprocess.getstatusoutput("ip addr show tun0")[0]
    is_vpn_active = (vpn_check == 0)
    
    try:
        # Get public IP with a short timeout
        public_ip = subprocess.check_output(
            ["curl", "-s", "--connect-timeout", "2", "ifconfig.me/ip"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        public_ip = "Unknown"

    if is_vpn_active:
        # Simple heuristic: if VPN is on, we assume we are secured unless we want to 
        # compare against a known "home" IP (which we don't have yet).
        # For this onboarding, SECURED if VPN is on.
        return "[bold green]SECURED[/bold green]"
    else:
        return f"[bold red]EXPOSED ({public_ip})[/bold red]"

def get_stats():
    TOOLS_LIST_PATH = "/data/data/com.termux/files/home/.local/etc/i-Haklab/Tools/listoftools"
    try:
        with open(TOOLS_LIST_PATH, 'r') as f:
            tools = [l.strip() for l in f if l.strip()]
        inst = sum(1 for t in tools if subprocess.getstatusoutput(f"which {t}")[0] == 0)
        
        # Check Engram
        engram_online = subprocess.getstatusoutput("which engram")[0] == 0
        engram_status = "[bold green]ONLINE[/bold green]" if engram_online else "[bold red]OFFLINE[/bold red]"
        
        # Check Battery (Termux-API)
        try:
            batt_data = json.loads(subprocess.getoutput("termux-battery-status"))
            batt_pct = batt_data.get('percentage', 0)
            batt_color = "green" if batt_pct > 30 else "yellow" if batt_pct > 15 else "red"
            batt_status = f"[bold {batt_color}]{batt_pct}%[/bold {batt_color}]"
        except: 
            batt_status = "[bold yellow]N/A[/bold yellow]"
        
        # Check VPN & IP Leak
        vpn_status = check_ip_leak()
        
        return inst, len(tools), engram_status, batt_status, vpn_status
    except Exception as e:
        return 0, 0, "[bold red]ERR[/bold red]", "[bold red]ERR[/bold red]", f"[bold red]ERR: {str(e)}[/bold red]"
