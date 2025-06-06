# Python script to display detailed Wi-Fi information (SSID, signal strength, channel, etc.)
# Works on Windows, Linux, and macOS. Run in terminal/command prompt.

import platform
import subprocess
import os

def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode(errors='ignore')
    except Exception as e:
        return f"Error running command: {e}"

def get_wifi_info_windows():
    return run_command("netsh wlan show interfaces")

def get_wifi_info_linux():
    # Try nmcli first (preferred)
    nmcli_output = run_command("nmcli -f all dev wifi show")
    if "Error" not in nmcli_output:
        return nmcli_output

    # Fall back to iwconfig
    return run_command("iwconfig")

def get_wifi_info_mac():
    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    if not os.path.exists(airport_path):
        return "macOS airport utility not found."
    return run_command(f"{airport_path} -I")

if __name__ == "__main__":
    system = platform.system().lower()
    
    print(f"Detected OS: {system.capitalize()}")
    print("\nWi-Fi Information:\n" + "-"*50)

    if 'windows' in system:
        print(get_wifi_info_windows())
    elif 'linux' in system:
        print(get_wifi_info_linux())
    elif 'darwin' in system:  # macOS
        print(get_wifi_info_mac())
    else:
        print("Unsupported OS.")
