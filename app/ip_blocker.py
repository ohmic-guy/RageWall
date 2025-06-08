import os
import platform
from .utils import log_blocked_ip

def block_ip(ip):
    system = platform.system()
    print(f"[BLOCK] Blocking IP: {ip}")

    if system == "Windows":
        os.system(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in interface=any action=block remoteip={ip}')
    elif system == "Linux":
        os.system(f'sudo iptables -A INPUT -s {ip} -j DROP')
    else:
        print("[ERROR] Unsupported OS")

    log_blocked_ip(ip)
