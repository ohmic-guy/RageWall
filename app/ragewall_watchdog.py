import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

blocked_ips = set()

HONEYPOT_LOG = "honeypot_logs.json"

def is_malicious(entry):
    # Basic rule-based heuristic
    return entry["endpoint"] in ["/admin", "/login"]

def block_ip(ip):
    if ip in blocked_ips:
        return
    blocked_ips.add(ip)
    print(f"[RAGEWALL] Blocking IP: {ip}")

    if os.name == 'nt':
        os.system(f'netsh advfirewall firewall add rule name="RageWall Block {ip}" dir=in action=block remoteip={ip}')
    else:
        os.system(f'sudo iptables -A INPUT -s {ip} -j DROP')

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(HONEYPOT_LOG):
            with open(HONEYPOT_LOG, "r") as f:
                lines = f.readlines()[-10:]  # Read only last 10 lines to avoid overload
                for line in lines:
                    try:
                        data = json.loads(line)
                        if is_malicious(data):
                            block_ip(data["ip"])
                    except:
                        continue

if __name__ == "__main__":
    print("[RAGEWALL] Watchdog started...")
    observer = Observer()
    event_handler = LogHandler()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
