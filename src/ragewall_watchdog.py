import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ip_blocker import block_ip

HONEYPOT_LOG = "honeypot_logs.json"
blocked_ips = set()

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_size = 0

    def on_modified(self, event):
        if event.src_path.endswith(HONEYPOT_LOG):
            with open(HONEYPOT_LOG, "r") as f:
                f.seek(self.last_size)
                for line in f:
                    data = json.loads(line)
                    ip = data.get("ip")
                    if ip and ip not in blocked_ips:
                        block_ip(ip)
                        blocked_ips.add(ip)
                self.last_size = f.tell()

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
