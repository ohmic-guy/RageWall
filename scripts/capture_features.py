from scapy.all import sniff, IP
import pandas as pd

data = []

def extract_features(packet):
    if IP in packet:
        ip_layer = packet[IP]
        data.append({
            'src_ip': ip_layer.src,
            'dst_ip': ip_layer.dst,
            'length': len(packet),
            'ttl': ip_layer.ttl,
            'proto': ip_layer.proto
        })

sniff(prn=extract_features, count=500)

df = pd.DataFrame(data)
df.to_csv("traffic_data.csv", index=False)
print("Captured and saved to traffic_data.csv")
