import pandas as pd

df = pd.read_csv("traffic_data.csv")

ip_counts = df['src_ip'].value_counts()
print("Source IP counts:\n", ip_counts)

# Set a minimum number of packets to consider as attacker
min_packets = 10  # Adjust this based on your data size

suspected_attackers = ip_counts[ip_counts > min_packets].index.tolist()
print("Suspected Attacker IPs:", suspected_attackers)

df['label'] = df['src_ip'].apply(lambda x: 1 if x in suspected_attackers else 0)

print("\nLabeled Data (first 5 rows):")
print(df.head())

print("\nSummary of Labeled Data:")
print(df['label'].value_counts())
print("\nDistribution of Labels:")
print(df['label'].value_counts(normalize=True))

print("\nUnique Source IPs and their Counts:")
print(df['src_ip'].value_counts().head(10))

print("\nUnique Destination IPs and their Counts:")
print(df['dst_ip'].value_counts().head(10))

df.to_csv("traffic_data_labeled.csv", index=False)
print("Labeled data saved to traffic_data_labeled.csv")
