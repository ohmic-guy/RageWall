import streamlit as st
import pandas as pd
import json
from collections import Counter
import plotly.express as px

def load_logs():
    try:
        with open("honeypot_logs.json", "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
        return logs
    except FileNotFoundError:
        st.warning("No honeypot logs found.")
        return []

def main():
    st.title("🔥 RageWall Live Dashboard")
    logs = load_logs()
    if not logs:
        return

    df = pd.DataFrame(logs)
    st.subheader("Top 10 Attacker IPs")
    st.write(df['ip'].value_counts().head(10))

    st.subheader("Attack Timeline")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    timeline = df.groupby(df['timestamp'].dt.floor('min')).size()
    st.line_chart(timeline)

    st.subheader("Endpoint Heatmap")
    endpoint_counts = df['endpoint'].value_counts()
    fig = px.bar(x=endpoint_counts.index, y=endpoint_counts.values, labels={'x':'Endpoint', 'y':'Hits'})
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

