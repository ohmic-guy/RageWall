import json
import os
from datetime import datetime

HONEYPOT_LOG = 'data/honeypot_logs.json'
BLOCKED_LOG = 'data/blocked_ips.json'

def log_honeypot_hit(ip):
    entry = {"ip": ip, "timestamp": str(datetime.now())}
    append_json(HONEYPOT_LOG, entry)

def log_blocked_ip(ip):
    entry = {"ip": ip, "timestamp": str(datetime.now())}
    append_json(BLOCKED_LOG, entry)

def append_json(path, entry):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([entry], f, indent=4)
    else:
        with open(path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)
