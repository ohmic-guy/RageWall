import streamlit as st
import json
import matplotlib.pyplot as plt
from collections import Counter

def load_logs():
    with open("honeypot_logs.json", "r") as f:
        logs = [json.loads(line) for line in f.readlines()]
    return logs

def main():
    st.title("🔥 RageWall Live Dashboard")
    logs = load_logs()

    ips = [entry["ip"] for entry in logs]
    endpoints = [entry["endpoint"] for entry in logs]

    st.subheader("Blocked IPs (Top 10)")
    st.write(Counter(ips).most_common(10))

    st.subheader("Most Targeted Endpoints")
    st.bar_chart(Counter(endpoints))

    st.subheader("Total Unique Attackers")
    st.write(len(set(ips)))

    # Pie chart
    fig, ax = plt.subplots()
    endpoint_counts = Counter(endpoints)
    ax.pie(endpoint_counts.values(), labels=endpoint_counts.keys(), autopct='%1.1f%%')
    st.pyplot(fig)

if __name__ == "__main__":
    main()

