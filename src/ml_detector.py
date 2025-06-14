from scapy.all import sniff, IP
import joblib
import pandas as pd
import os
import numpy as np


try:
    artifacts = joblib.load("models/ragewall_model.pkl")
    if not isinstance(artifacts, dict):
        raise ValueError("Loaded model is not a dictionary containing the expected keys.")
    clf = artifacts['model']
    scaler = artifacts['scaler']
    feature_columns = artifacts['feature_columns']
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

blocked_ips = set()

def extract_features(pkt):
    if IP in pkt:
        ip_layer = pkt[IP]
        length = len(pkt)
        ttl = ip_layer.ttl
        proto = ip_layer.proto

        length_log = np.log1p(length)
        ttl_bins = pd.qcut([ttl], q=5, labels=False, duplicates='drop')[0]
        length_bin = pd.qcut([length], q=5, labels=False, duplicates='drop')[0]
        # For live traffic, you may not have global frequency info, so set to 1 or 0
        src_ip_freq = 1
        dst_ip_freq = 1
        ttl_outlier = int((ttl < 32) or (ttl > 128))

        features = pd.DataFrame(
            [[length, ttl, proto, length_log, ttl_bins, length_bin, src_ip_freq, dst_ip_freq, ttl_outlier]],
            columns=feature_columns
        )

        scaled_features = scaler.transform(features)
        return pd.DataFrame(scaled_features, columns=feature_columns), ip_layer.src
    return None, None

def process_packet(pkt):
    data, src_ip = extract_features(pkt)
    if data is None:
        return

    prediction = clf.predict(data)[0]

    if prediction == 1:
        if src_ip not in blocked_ips:
            print(f"Blocked malicious packet from: {src_ip}")
            os.system(f'netsh advfirewall firewall add rule name="Block {src_ip}" dir=in action=block remoteip={src_ip}')
            blocked_ips.add(src_ip)
        else:
            print(f"(Already blocked) Malicious packet from: {src_ip}")
    else:
        print(f"Legit packet from: {src_ip}")

print("RageWall is live. Watching traffic...")
sniff(filter="ip", prn=process_packet, store=0)
