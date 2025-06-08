import pandas as pd

df = pd.read_csv("../data/traffic_data.csv")


ip_counts = df['src_ip'].value_counts()

print("🔍 Analyzing traffic data for potential attackers...")
threshold_percent = 0.01
num_attackers = max(1, int(len(ip_counts) * threshold_percent))


suspected_attackers = ip_counts.head(num_attackers).index.tolist()
print("🔍 Analyzing traffic data for potential attackers...")


print("🔍 Suspected Attacker IPs:")
print(suspected_attackers)


df['label'] = df['src_ip'].apply(lambda x: 1 if x in suspected_attackers else 0)


print("\n🔍 Labeled Data (first 5 rows):")
print(df.head())

print("\n🔍 Summary of Labeled Data:")
print(df['label'].value_counts())
print("\n🔍 Distribution of Labels:")
print(df['label'].value_counts(normalize=True))

print("\n🔍 Unique Source IPs and their Counts:")
print(df['src_ip'].value_counts().head(10))

print("\n🔍 Unique Destination IPs and their Counts:")

print(df['dst_ip'].value_counts().head(10))



df.to_csv("traffic_data_labeled.csv", index=False)

print("Labeled data saved to traffic_data_labeled.csv")
