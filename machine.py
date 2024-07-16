import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Load the datasets
print("Loading datasets...")
probe_data_path = 'Probe-Data-Export.csv'
tmc_data_path = 'TMC_Identification.csv'

probe_data = pd.read_csv(probe_data_path)
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
contamination = 0.01  # Proportion of anomalies in the data

# Function to detect anomalies using Isolation Forest for each TMC segment
def detect_anomalies(data_segment):
    print(f"Detecting anomalies for TMC segment {data_segment['tmc'].iloc[0]}...")
    
    # Isolation Forest Model
    model = IsolationForest(contamination=contamination, random_state=42)
    
    # We use 'speed' and 'historical_average_speed' as features
    features = data_segment[['speed', 'historical_average_speed']]
    model.fit(features)
    
    # Predict anomalies
    data_segment['anomaly'] = model.predict(features)
    
    # Anomalies are the rows where 'anomaly' is -1
    anomalies = data_segment[data_segment['anomaly'] == -1]
    
    print(f"Anomalies detected for TMC segment {data_segment['tmc'].iloc[0]}.")
    return anomalies

# Analyze each TMC segment
print("Analyzing each TMC segment...")
all_anomalies = pd.DataFrame()

for tmc in data_merged['tmc'].unique():
    print(f"Processing TMC segment {tmc}...")
    segment_data = data_merged[data_merged['tmc'] == tmc]
    segment_data = segment_data.copy()  # To avoid SettingWithCopyWarning
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
