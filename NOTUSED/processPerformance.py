import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the JSON data
with open('performance_metrics.json', 'r') as file:
    data = json.load(file)

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Define thresholds for anomalies
speed_threshold = 45  # Speed below which is considered an anomaly
congestion_threshold = 90  # Congestion above which is considered an anomaly
planning_time_index_threshold = 1.2  # Planning Time Index above which is considered an anomaly

# Detect anomalies
df['speed_anomaly'] = df['speed'] < speed_threshold
df['congestion_anomaly'] = df['congestion'] > congestion_threshold
df['planning_time_index_anomaly'] = df['planningTimeIndex'] > planning_time_index_threshold

# Combine anomalies into a single column
df['anomaly'] = df['speed_anomaly'] | df['congestion_anomaly'] | df['planning_time_index_anomaly']

# Print the number of anomalies detected
print("Number of speed anomalies detected:", df['speed_anomaly'].sum())
print("Number of congestion anomalies detected:", df['congestion_anomaly'].sum())
print("Number of planning time index anomalies detected:", df['planning_time_index_anomaly'].sum())

# Plot the data
plt.figure(figsize=(14, 8))

# Plot speed
plt.subplot(3, 1, 1)
plt.plot(df['interval'], df['speed'], label='Speed')
plt.scatter(df[df['speed_anomaly']]['interval'], df[df['speed_anomaly']]['speed'], color='red', label='Speed Anomaly')
plt.axhline(y=speed_threshold, color='r', linestyle='--', label='Speed Threshold')
plt.xlabel('Interval')
plt.ylabel('Speed')
plt.title('Speed and Anomalies')
plt.legend()

# Plot congestion
plt.subplot(3, 1, 2)
plt.plot(df['interval'], df['congestion'], label='Congestion')
plt.scatter(df[df['congestion_anomaly']]['interval'], df[df['congestion_anomaly']]['congestion'], color='red', label='Congestion Anomaly')
plt.axhline(y=congestion_threshold, color='r', linestyle='--', label='Congestion Threshold')
plt.xlabel('Interval')
plt.ylabel('Congestion')
plt.title('Congestion and Anomalies')
plt.legend()

# Plot planning time index
plt.subplot(3, 1, 3)
plt.plot(df['interval'], df['planningTimeIndex'], label='Planning Time Index')
plt.scatter(df[df['planning_time_index_anomaly']]['interval'], df[df['planning_time_index_anomaly']]['planningTimeIndex'], color='red', label='Planning Time Index Anomaly')
plt.axhline(y=planning_time_index_threshold, color='r', linestyle='--', label='Planning Time Index Threshold')
plt.xlabel('Interval')
plt.ylabel('Planning Time Index')
plt.title('Planning Time Index and Anomalies')
plt.legend()

plt.tight_layout()
plt.savefig('performance_metrics_anomalies.png')
plt.show()
