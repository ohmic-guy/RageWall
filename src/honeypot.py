import socket
import threading
from utils import log_honeypot_hit

def honeypot_server(host='0.0.0.0', port=2222):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"[HONEYPOT] Listening on {host}:{port}")

    while True:
        client, addr = s.accept()
        ip = addr[0]
        endpoint = "/admin"
        log_honeypot_hit(ip, endpoint)
        print(f"[HONEYPOT] Connection attempt from {ip} to {endpoint}")
        client.close()

def run_honeypot():
    threading.Thread(target=honeypot_server, daemon=True).start()

if __name__ == "__main__":
    honeypot_server()
