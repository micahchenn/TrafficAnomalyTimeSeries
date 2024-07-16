import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import mplcursors

# Load the JSON data
with open('pm_data.json') as f:
    data = json.load(f)

# Convert JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the DataFrame to understand its structure
print(df.head())

# Convert interval to datetime if necessary (assuming interval represents minutes from a start date)
start_date = datetime.strptime("2024-05-08", "%Y-%m-%d")  # assuming the start date as May 8, 2024
df['time'] = df['interval'].apply(lambda x: start_date + timedelta(minutes=x))

# Calculate the difference between congestion and averageCongestion
df['congestion_diff'] = df['congestion'] - df['averageCongestion']

# Calculate the mean and standard deviation of the congestion difference
mean_diff = df['congestion_diff'].mean()
std_diff = df['congestion_diff'].std()

# Define a threshold for anomaly detection (mean ± 2 * standard deviation)
threshold_upper = mean_diff + 2 * std_diff
threshold_lower = mean_diff - 2 * std_diff

# Identify anomalies
df['anomaly'] = np.where((df['congestion_diff'] > threshold_upper) | (df['congestion_diff'] < threshold_lower), True, False)

# Plot the congestion using a scatter plot and highlight anomalies
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(df['time'], df['congestion'], label='Current Congestion', alpha=0.5, color='blue')
ax.scatter(df[df['anomaly']]['time'], df[df['anomaly']]['congestion'], label='Anomalies', color='red')
ax.scatter(df['time'], df['averageCongestion'], label='Historical Average Congestion', color='green', alpha=0.5)
ax.axhline(y=threshold_upper, color='r', linestyle='--', label='Anomaly Threshold Upper (Difference)')
ax.axhline(y=threshold_lower, color='r', linestyle='--', label='Anomaly Threshold Lower (Difference)')
ax.set_xlabel('Time')
ax.set_ylabel('Congestion')
ax.set_title('Traffic Congestion Over Time with Anomalies')
ax.legend()
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
fig.autofmt_xdate()

# Enable zooming and panning
mplcursors.cursor(ax, hover=True)

plt.show()

# Print anomalies
anomalies = df[df['anomaly']]
print("Identified anomalies:")
print(anomalies[['time', 'congestion', 'averageCongestion', 'congestion_diff']])

# Calculate the average historical congestion
historical_avg_congestion = df['averageCongestion'].mean()

# Calculate the current average congestion
current_avg_congestion = df['congestion'].mean()

# Print the results
print(f"Historical Average Congestion: {historical_avg_congestion:.2f}")
print(f"Current Average Congestion: {current_avg_congestion:.2f}")

# Determine if current congestion is worse
if current_avg_congestion > historical_avg_congestion:
    print("Current congestion is worse compared to historical average.")
else:
    print("Current congestion is better or similar compared to historical average.")
