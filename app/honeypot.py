import socket
import threading
import json
from datetime import datetime
from .utils import log_honeypot_hit

def honeypot_server(host='0.0.0.0', port=2222):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"[HONEYPOT] Listening on {host}:{port}")

    while True:
        client, addr = s.accept()
        ip = addr[0]
        log_honeypot_hit(ip)
        print(f"[HONEYPOT] Connection attempt from {ip}")
        client.close()

def run_honeypot():
    threading.Thread(target=honeypot_server, daemon=True).start()
