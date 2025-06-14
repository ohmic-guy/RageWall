import os
import platform
from utils import log_blocked_ip

WHITELIST = {"127.0.0.1", "192.168.1.1"}  # Add your trusted IPs here

def block_ip(ip):
    if ip in WHITELIST:
        print(f"[BLOCK] Skipped whitelisted IP: {ip}")
        return
    system = platform.system()
    print(f"[BLOCK] Blocking IP: {ip}")

    try:
        if system == "Windows":
            os.system(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in interface=any action=block remoteip={ip}')
        elif system == "Linux":
            os.system(f'sudo iptables -A INPUT -s {ip} -j DROP')
        else:
            print("[ERROR] Unsupported OS")
    except Exception as e:
        print(f"[ERROR] Failed to block IP: {e}")

    log_blocked_ip(ip)
