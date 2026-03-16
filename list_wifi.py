import subprocess
import platform
import re

def get_band(channel_or_freq):
    """Helper to determine band based on channel or frequency string."""
    try:
        # If it's a frequency in MHz (e.g., 2412 or 5180)
        val = int(re.sub(r'[^0-9]', '', str(channel_or_freq)))
        if val < 100:  # It's likely a channel number
            return "2.4GHz" if val <= 14 else "5GHz"
        else:  # It's likely a frequency in MHz
            return "2.4GHz" if 2400 <= val <= 2500 else "5GHz"
    except:
        return "Unknown"

def list_wifi_with_bands():
    os_name = platform.system()
    
    if os_name == "Windows":
        # Windows 'netsh' shows 'Channel' in 'show networks mode=bssid'
        cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        output = subprocess.check_output(cmd, encoding='ascii', errors='ignore')
        
        current_ssid = ""
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                current_ssid = line.split(":")[1].strip()
            if "Channel" in line:
                channel = line.split(":")[1].strip()
                print(f"SSID: {current_ssid:20} | Channel: {channel:3} | Band: {get_band(channel)}")

    elif os_name == "Linux":
        # Linux 'nmcli' provides a clean table with the 'FREQ' column
        cmd = ["nmcli", "-f", "SSID,FREQ,CHAN", "device", "wifi", "list"]
        output = subprocess.check_output(cmd, encoding='utf-8')
        print(output)

    elif os_name == "Darwin": # macOS
        # macOS 'airport -s' shows 'CHANNEL'
        path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        output = subprocess.check_output([path, "-s"], encoding='utf-8')
        
        lines = output.splitlines()
        header = lines[0]
        for line in lines[1:]:
            # Simple split by whitespace; SSID can have spaces, but channel is usually second to last
            parts = line.split()
            if len(parts) > 3:
                channel = parts[-3].split(',')[0] # Handles '36,+1' format
                ssid = " ".join(parts[:-6])
                print(f"SSID: {ssid:20} | Channel: {channel:3} | Band: {get_band(channel)}")

if __name__ == "__main__":
    list_wifi_with_bands()