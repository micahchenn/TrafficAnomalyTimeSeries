import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the datasets
print("Loading datasets...")
probe_data_path = 'probe_data/Probe-Data-Export.csv'
tmc_data_path = 'probe_data/TMC_Identification.csv'

probe_data = pd.read_csv(probe_data_path, parse_dates=['measurement_tstamp'])
tmc_data = pd.read_csv(tmc_data_path)

print("Datasets loaded successfully.")

# Remove duplicate columns in the probe data
print("Cleaning probe data by removing duplicate columns...")
columns_to_drop = ['historical_average_speed.1', 'travel_time_minutes.1']
probe_data_cleaned = probe_data.loc[:, ~probe_data.columns.duplicated()].drop(columns=columns_to_drop)

# Rename the column to match for merging
print("Renaming columns for merging...")
probe_data_cleaned.rename(columns={'tmc_code': 'tmc'}, inplace=True)

# Merge probe data with TMC identification data on TMC
print("Merging probe data with TMC identification data...")
data_merged = pd.merge(probe_data_cleaned, tmc_data, on='tmc', how='left')

print("Data merged successfully.")
print("Merged DataFrame columns:", data_merged.columns)

# Set parameters for anomaly detection
deviation_threshold = -10  # Threshold for speed deviation (negative for significant decrease)
sustained_period = 5  # Number of consecutive minutes for an anomaly

# Function to detect anomalies for each TMC segment
def detect_anomalies(data_segment):
    print(f"Detecting anomalies for TMC segment {data_segment['tmc'].iloc[0]}...")
    data_segment['date'] = data_segment['measurement_tstamp'].dt.date
    anomalies = []

    for date, group in data_segment.groupby('date'):
        group['speed_deviation'] = group['speed'] - group['historical_average_speed']
        group['is_anomaly'] = (group['speed_deviation'] < deviation_threshold).rolling(window=sustained_period).sum() >= sustained_period
        anomalies.extend(group[group['is_anomaly']].to_dict(orient='records'))
    
    print(f"Anomalies detected for TMC segment {data_segment['tmc'].iloc[0]}.")
    return pd.DataFrame(anomalies)

# Analyze each TMC segment
print("Analyzing each TMC segment...")
all_anomalies = pd.DataFrame()

for tmc in data_merged['tmc'].unique():
    print(f"Processing TMC segment {tmc}...")
    segment_data = data_merged[data_merged['tmc'] == tmc]
    anomalies_df = detect_anomalies(segment_data)
    all_anomalies = pd.concat([all_anomalies, anomalies_df], ignore_index=True)

print("Anomaly detection completed.")

# Plot the speed vs historical average speed and reference speed for each TMC segment
print("Plotting data for TMC segments...")

for tmc in data_merged['tmc'].unique():
    print(f"Plotting data for TMC segment {tmc}...")
    segment_data = data_merged[data_merged['tmc'] == tmc]

    plt.figure(figsize=(14, 7))
    plt.plot(segment_data['measurement_tstamp'], segment_data['speed'], label='Current Speed', color='blue')
    plt.plot(segment_data['measurement_tstamp'], segment_data['historical_average_speed'], label='Historical Average Speed', color='green')
    plt.plot(segment_data['measurement_tstamp'], segment_data['reference_speed'], label='Reference Speed', color='red')

    # Plot anomalies
    anomalies = all_anomalies[all_anomalies['tmc'] == tmc]
    plt.scatter(anomalies['measurement_tstamp'], anomalies['speed'], color='orange', label='Anomalies', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Speed (mph)')
    plt.title(f'Speed vs Historical Average Speed and Reference Speed for TMC {tmc}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

print("Plotting completed.")

# Output anomaly time ranges to a .txt file
print("Writing anomaly times to a text file...")
with open('anomaly_times.txt', 'w') as f:
    f.write('Anomalies detected at the following times:\n')
    for index, row in all_anomalies.iterrows():
        f.write(f"{row['measurement_tstamp']} (TMC: {row['tmc']})\n")

print("Anomaly times written to anomaly_times.txt.")

# Show the first few rows of the anomalies
print("First few rows of detected anomalies:")
print(all_anomalies.head())
