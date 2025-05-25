

#!/usr/bin/env python3

"""
SystemTune.py
-------------
A Linux system diagnostic and tuning script using OpenAI for intelligent recommendations.

This script performs:
1. Hardware and software diagnostics
2. System log analysis
3. AI-driven optimization suggestions
4. User confirmation before applying changes

Requires:
- Python 3.7+
- OpenAI Python SDK (`pip install openai`)
- Root access for some operations
"""

import os
import subprocess
import openai
import json
from dotenv import load_dotenv

load_dotenv()  # Load .env file into environment

# CONFIGURATION
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key in the environment

# Run a shell command and return output
def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running command '{cmd}': {e.stderr.strip()}"

# Collect hardware and software diagnostics
def collect_system_info():
    info = {}
    info['CPU Info'] = run_cmd("lscpu")
    info['Memory Info'] = run_cmd("free -h")
    info['Disk Info'] = run_cmd("lsblk")
    info['PCI Devices'] = run_cmd("lspci")
    info['USB Devices'] = run_cmd("lsusb")
    info['Kernel Version'] = run_cmd("uname -a")
    info['Distro Info'] = run_cmd("cat /etc/*release")
    return info

# Collect recent system logs
def collect_logs():
    return run_cmd("journalctl -p 3 -xb")  # Priority 3 = errors

# Query OpenAI for optimization suggestions
def get_ai_suggestions(system_info, logs):
    prompt = f"""
You are a Linux performance tuning assistant. Given the following system details and logs, suggest optimizations:

System Info:
{json.dumps(system_info, indent=2)}

System Logs:
{logs}

Return concise, actionable suggestions. If anything looks critical or unstable, flag it clearly.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response['choices'][0]['message']['content']

# Ask user to approve suggestions
def confirm_and_execute(suggestions):
    print("\n===== AI Suggestions =====")
    print(suggestions)
    print("\nDo you want to apply any of the above suggestions manually or automatically? (manual/auto/skip): ", end="")
    choice = input().strip().lower()

    if choice == 'auto':
        print(">> Automation logic not implemented. You should manually review suggestions.")
        # Placeholder: logic for automation can be implemented here
    elif choice == 'manual':
        print(">> Please apply the suggestions manually.")
    else:
        print(">> Skipping execution.")

# Main function
def main():
    print("[*] Gathering system diagnostics...")
    sys_info = collect_system_info()

    print("[*] Collecting logs...")
    logs = collect_logs()

    print("[*] Querying AI for suggestions...")
    suggestions = get_ai_suggestions(sys_info, logs)

    confirm_and_execute(suggestions)

if __name__ == "__main__":
    main()