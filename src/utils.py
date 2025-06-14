import json
from datetime import datetime
import logging

HONEYPOT_LOG = "honeypot_logs.json"
BLOCKED_IP_LOG = "blocked_ips.json"

logging.basicConfig(
    filename="ragewall.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def log_event(msg):
    logging.info(msg)

def log_honeypot_hit(ip, endpoint):
    entry = {
        "ip": ip,
        "endpoint": endpoint,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(HONEYPOT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log_event(f"Honeypot hit: {entry}")

def log_blocked_ip(ip):
    entry = {
        "ip": ip,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(BLOCKED_IP_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log_event(f"Blocked IP: {entry}")
