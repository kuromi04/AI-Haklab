# Skill: Termux Oracle Knowledge Base
# Description: Rules, architecture, and commands for operating inside the i-Haklab hacking lab on Termux, including Android platform limitations and the Ivam3 community guidelines.

## Rules
- Always verify VPN and network encryption status before launching any network activity inside Termux. If status is EXPOSED, alert the operator.
- Align all penetration testing, vulnerability discovery, and scanning activities with the MITRE ATT&CK methodology.
- Ensure all custom commands conform to Termux limitations (specifically the 39-bit Virtual Address limitation on Android kernels and glibc linking).
- When resolving failures with external Linux ARM64 binaries, refer to `termux-va39-patcher` guidelines to patch memory limits.

## Workflow
1. **Target Analysis**: Query the system state (IP, battery, vpn) before beginning.
2. **Consult Knowledge**: For evasion or bypass operations, refer to `waf-bypass.md` in the knowledge directory.
3. **Execution**: Run tools (like `nmap`, `sqlmap`, `msfconsole`) via the Debian container when native environment limitations prevent execution.
4. **Intrusion Reporting**: Generate standard markdown reports detailing findings, chronological logs, and MITRE mapping upon session termination.

## Tools
- `proot-distro login debian` for running complex Linux binaries.
- `termux-tts-speak` for voice guidance notifications to the operator.
- `engram` CLI for saving and loading cross-session OODA loop states.
