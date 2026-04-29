import json
import os
import sys
from rich.console import Console

console = Console()

class ConfigValidator:
    def __init__(self, config_path):
        self.config_path = config_path

    def validate(self):
        """Checks for required keys in config.json and returns the config if valid."""
        if not os.path.exists(self.config_path):
            console.print(f"[bold red]CRITICAL ERROR:[/bold red] Configuration file not found at {self.config_path}")
            sys.exit(1)

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            console.print(f"[bold red]CRITICAL ERROR:[/bold red] Failed to parse config.json: {str(e)}")
            sys.exit(1)

        # Check for mandatory top-level keys
        required_keys = ['current_provider', 'providers']
        for key in required_keys:
            if key not in config:
                console.print(f"[bold red]CRITICAL ERROR:[/bold red] Missing mandatory key '{key}' in config.json")
                sys.exit(1)

        # Check if current provider exists in providers list
        current = config['current_provider']
        if current not in config['providers']:
            console.print(f"[bold red]CRITICAL ERROR:[/bold red] Selected provider '{current}' is not defined in 'providers'")
            sys.exit(1)

        # Check for API key of the current provider
        provider_data = config['providers'][current]
        if 'api_key' not in provider_data or not provider_data['api_key']:
            # Exception for free models if they don't need keys, but usually they do in this config
            if "free" not in provider_data.get('model', '').lower():
                console.print(f"[bold red]CRITICAL ERROR:[/bold red] API Key missing for provider '{current}'")
                sys.exit(1)

        return config
