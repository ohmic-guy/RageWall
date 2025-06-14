import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scapy.all import sniff, IP
from collections import deque
import time
import threading


window_size = 60
packet_counts = deque([0]*window_size, maxlen=window_size)
time_labels = deque([time.strftime('%H:%M:%S')] * window_size, maxlen=window_size)


def process_packet(pkt):
    if IP in pkt:
        packet_counts[-1] += 1


def update_plot(frame):
    current_time = time.strftime('%H:%M:%S')
    packet_counts.append(0)
    time_labels.append(current_time)
    
    ax.clear()
    ax.plot(list(time_labels), list(packet_counts), color='red', linewidth=2)
    ax.set_title("📡 Real-Time Network Traffic (pkts/sec)", fontsize=14)
    ax.set_ylabel("Packet Count")
    ax.set_xlabel("Time (HH:MM:SS)")
    ax.set_xticks(list(time_labels)[::5])
    ax.set_ylim(0, max(max(packet_counts), 10))
    ax.grid(True)

def start_sniffing():
    sniff(filter="ip", prn=process_packet, store=0)


fig, ax = plt.subplots(figsize=(10, 4))
ani = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)


print("Watching traffic... close the plot window to stop.")
sniff_thread = threading.Thread(target=start_sniffing, daemon=True)
sniff_thread.start()


plt.tight_layout()
plt.show()
