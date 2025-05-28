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

#### Usage:
python -m venv .venv
source .venv/bin/activate
pip install openai==0.28
pip install python-dotenv

OPENAI_API_KEY=sk-... python SystemTune.py
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

# Collect hardware and software diagnostics (enhanced version)
def collect_system_info():
    info = {}
    info['CPU Info'] = run_cmd("lscpu")
    info['Memory Info'] = run_cmd("free -h")
    info['Disk Info'] = run_cmd("lsblk")
    info['PCI Devices'] = run_cmd("lspci")

    import shutil
    if shutil.which("lsusb"):
        info['USB Devices'] = run_cmd("lsusb")
    else:
        info['USB Devices'] = "lsusb not found. Install usbutils to view USB devices."

    info['Kernel Version'] = run_cmd("uname -a")
    info['Distro Info'] = run_cmd("cat /etc/*release")

    # Add precise system model info
    sys_vendor = run_cmd("cat /sys/devices/virtual/dmi/id/sys_vendor")
    product_name = run_cmd("cat /sys/devices/virtual/dmi/id/product_name")
    product_version = run_cmd("cat /sys/devices/virtual/dmi/id/product_version")
    info['System Model'] = f"{sys_vendor} {product_name} ({product_version})"
    info['Is Apple Mac'] = 'Apple' in sys_vendor or 'Mac' in product_name

    if shutil.which("dmidecode"):
        info['DMI Decode Info'] = run_cmd("sudo dmidecode -t system")
    else:
        info['DMI Decode Info'] = "dmidecode not available. Run as root and install dmidecode for hardware manufacturer info."

    if shutil.which("inxi"):
        info['Inxi Full'] = run_cmd("inxi -Fazy")
    else:
        info['Inxi Full'] = "inxi not available. Install with `sudo pacman -Sy inxi` or `sudo apt install inxi`."

    return info

# Collect recent system logs
def collect_logs():
    return run_cmd("journalctl -p 3 -xb")  # Priority 3 = errors

# Query OpenAI for optimization suggestions
def get_ai_suggestions(system_info, logs):
    system_model = system_info.get('System Model', 'Unknown system')
    mac_hint = ""
    if system_info.get('Is Apple Mac'):
        mac_hint = (
            "\nNOTE: This system is Apple Mac hardware. It may require Broadcom Wi-Fi support (broadcom-wl), "
            "the hid_apple kernel module for keyboard mappings, and macfanctld for fan control. "
            "Apple-specific drivers and EFI nuances should be considered.\n"
        )

    # Truncate logs to last 100 lines
    logs = "\n".join(logs.splitlines()[-100:])

    # Trim large system info values
    trimmed_info = {}
    for i, (k, v) in enumerate(system_info.items()):
        if i > 8:  # Limit to first 9 items
            break
        if isinstance(v, str) and len(v) > 500:
            trimmed_info[k] = v[:500] + "\n...[truncated]"
        else:
            trimmed_info[k] = v

    prompt = f"""
You are a Linux performance tuning assistant. The system is running on a {system_model}.
{mac_hint}
Use the following partial system details and recent logs to suggest optimizations and flag any unstable hardware-specific issues.

System Info (trimmed):
{json.dumps(trimmed_info, indent=2)[:1500]}  # Safely limit string length

Logs (last 100 lines only):
{logs[:2500]}  # Cap log length

Keep suggestions concise and actionable.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response['choices'][0]['message']['content']

# Ask user to approve suggestions
import shutil

# Ask user to approve suggestions
def confirm_and_execute(suggestions):
    print("\n\033[96m===== AI Suggestions =====\033[0m")
    print(suggestions)

    while True:
        print("\n\033[93mDo you want to apply any of the above suggestions manually or automatically? (manual/auto/skip/select): \033[0m", end="")
        choice = input().strip().lower()

        if choice == 'auto':
            print(">> \033[91mAutomation logic not implemented. You should manually review suggestions.\033[0m")
            break
        elif choice == 'manual':
            print(">> \033[92mPlease apply the suggestions manually.\033[0m")
            break
        elif choice == 'select':
            print("\n\033[94mAvailable issue numbers:\033[0m\n1 = Add swapfile\n2 = Install network firmware\n3 = Apply Mac hardware fixes")
            while True:
                print("\033[94mWhich issue number would you like to address?: \033[0m", end="")
                issue_number = input().strip()
                if issue_number == '1':
                    print("🛠️  \033[93mCreating a 4GB swapfile...\033[0m")
                    try:
                        if not shutil.which("swapon"):
                            print("❌ \033[91mSwap utilities not found on system.\033[0m")
                            return

                        run_cmd("sudo fallocate -l 4G /swapfile")
                        run_cmd("sudo chmod 600 /swapfile")
                        run_cmd("sudo mkswap /swapfile")
                        run_cmd("sudo swapon /swapfile")
                        with open("/etc/fstab", "a") as fstab:
                            fstab.write("\n/swapfile none swap sw 0 0\n")
                        print("✅ \033[92mSwap enabled and added to /etc/fstab.\033[0m")
                    except Exception as e:
                        print(f"❌ \033[91mFailed to create swapfile: {e}\033[0m")
                elif issue_number == '2':
                    print("🛠️  \033[93mAttempting to detect network chipset and install missing firmware...\033[0m")
                    try:
                        chipset_output = run_cmd("lspci -knn | grep -A3 -i net")
                        print(f"\033[96mDetected Network Chipset:\033[0m\n{chipset_output}")

                        # Try to determine distro and install firmware
                        distro_info = run_cmd("cat /etc/os-release")
                        if "Arch" in distro_info:
                            print("🔧 \033[93mDetected Arch-based system. Installing linux-firmware...\033[0m")
                            run_cmd("sudo pacman -Sy --noconfirm linux-firmware")
                        elif "Debian" in distro_info or "Ubuntu" in distro_info:
                            print("🔧 \033[93mDetected Debian-based system. Installing firmware-linux...\033[0m")
                            run_cmd("sudo apt update && sudo apt install -y firmware-linux firmware-linux-nonfree")
                        elif "Fedora" in distro_info:
                            print("🔧 \033[93mDetected Fedora-based system. Installing linux-firmware...\033[0m")
                            run_cmd("sudo dnf install -y linux-firmware")
                        else:
                            print("⚠️  \033[91mUnsupported or unknown distribution. Please install firmware manually.\033[0m")
                    except Exception as e:
                        print(f"❌ \033[91mFirmware installation failed: {e}\033[0m")
                elif issue_number == '3':
                    print("🛠️  \033[93mApplying Apple-specific hardware optimizations...\033[0m")
                    try:
                        run_cmd("sudo pacman -Sy --noconfirm broadcom-wl-dkms linux-headers")
                        run_cmd("echo 'options hid_apple fnmode=2' | sudo tee /etc/modprobe.d/hid_apple.conf")
                        run_cmd("yay -S --noconfirm macfanctld")
                        print("✅ \033[92mMac-specific packages installed.\033[0m")
                    except Exception as e:
                        print(f"❌ \033[91mFailed to apply Mac-specific fixes: {e}\033[0m")
                else:
                    print("⚠️  \033[91mIssue not implemented for auto-fix. Please apply manually.\033[0m")

                print("\n\033[93mWould you like to address another issue? (yes/no): \033[0m", end="")
                again = input().strip().lower()
                if again != "yes":
                    return
        else:
            print(">> \033[90mSkipping execution.\033[0m")
            break

# Main function
def main():
    print("[*] Gathering system diagnostics...")
    sys_info = collect_system_info()

    print("\033[95m\n=== System Summary ===\033[0m")
    import shutil
    if shutil.which("neofetch"):
        os.system("neofetch --off")
    else:
        print(run_cmd("hostnamectl"))
        print(run_cmd("uname -r"))
        print(run_cmd("lscpu | grep 'Model name'"))

    print("[*] Collecting logs...")
    logs = collect_logs()

    print("[*] Querying AI for suggestions...")
    suggestions = get_ai_suggestions(sys_info, logs)

    confirm_and_execute(suggestions)

if __name__ == "__main__":
    main()