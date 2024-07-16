import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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

# Create directory for saving plots
output_dir = 'pictures'
os.makedirs(output_dir, exist_ok=True)

# Plot the speed vs historical average speed and reference speed for each TMC segment
print("Plotting data for TMC segments...")

for tmc in data_merged['tmc'].unique():
    print(f"Plotting data for TMC segment {tmc}...")
    segment_data = data_merged[data_merged['tmc'] == tmc]

    road = segment_data['road'].iloc[0]
    direction = segment_data['direction'].iloc[0]
    intersection = segment_data['intersection'].iloc[0]
    state = segment_data['state'].iloc[0]

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(segment_data['measurement_tstamp'], segment_data['speed'], label='Current Speed', color='blue')
    ax.plot(segment_data['measurement_tstamp'], segment_data['historical_average_speed'], label='Historical Average Speed', color='green')
    ax.plot(segment_data['measurement_tstamp'], segment_data['reference_speed'], label='Reference Speed', color='red')

    # Plot anomalies
    anomalies = all_anomalies[all_anomalies['tmc'] == tmc]
    ax.scatter(anomalies['measurement_tstamp'], anomalies['speed'], color='orange', label='Anomalies', zorder=5)

    ax.set_xlabel('Time')
    ax.set_ylabel('Speed (mph)')
    ax.set_title(f'{road} {direction} at {intersection}, {state}')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    plt.tight_layout()

    # Save plot as an image
    plot_filename = f'{tmc}_{road}_{direction}_{intersection}_{state}.png'.replace('/', '_')
    plt.savefig(os.path.join(output_dir, plot_filename))

    # Display the plot in a new window
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
