import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# Load the data
probe_file_path = 'Probe-Data-Export.csv'
tmc_file_path = 'TMC_Identification.csv'

# Check if files exist
if not os.path.exists(probe_file_path):
    print(f"Error: {probe_file_path} does not exist.")
else:
    # Print the first few lines of the file
    with open(probe_file_path, 'r') as file:
        print("Content of Probe-Data-Export.csv:")
        for _ in range(10):
            print(file.readline().strip())

if not os.path.exists(tmc_file_path):
    print(f"Error: {tmc_file_path} does not exist.")
else:
    # Print the first few lines of the file
    with open(tmc_file_path, 'r') as file:
        print("Content of TMC_Identification.csv:")
        for _ in range(10):
            print(file.readline().strip())

# Load the data
probe_data = pd.read_csv(probe_file_path)
tmc_identification = pd.read_csv(tmc_file_path)

# Debug: Print the first few rows of the data
print("Probe Data:")
print(probe_data.head())
print("\nTMC Identification Data:")
print(tmc_identification.head())

# Ensure proper data types
if not probe_data.empty:
    probe_data['measurement_tstamp'] = pd.to_datetime(probe_data['measurement_tstamp'])
    probe_data['speed'] = probe_data['speed'].astype(float)
    probe_data['historical_average_speed'] = probe_data['historical_average_speed'].astype(float)

    # Function to detect anomalies based on Z-score, focusing on lower speeds
    def detect_anomalies(df, window_size=30, threshold=-3):
        df['rolling_mean'] = df['speed'].rolling(window=window_size).mean()
        df['rolling_std'] = df['speed'].rolling(window=window_size).std()
        df['anomaly_score'] = (df['speed'] - df['rolling_mean']) / df['rolling_std']
        anomalies = df[df['anomaly_score'] < threshold]
        return anomalies

    # Process the first TMC only
    tmc_list = probe_data['tmc_code'].unique()

    # Debug: Print the unique TMC list
    print("Unique TMC List:")
    print(tmc_list)

    # Check if the TMC list is empty
    if len(tmc_list) == 0:
        print("Error: No TMC codes found in the data.")
    else:
        first_tmc = tmc_list[0]
        print(f"Processing first TMC: {first_tmc}")

        tmc_data = probe_data[probe_data['tmc_code'] == first_tmc].copy()

        # Detect anomalies for the first TMC
        anomalies = detect_anomalies(tmc_data)

        # Create output directories if they don't exist
        if not os.path.exists('anomalies'):
            os.makedirs('anomalies')
        if not os.path.exists('plots'):
            os.makedirs('plots')

        # Save anomalies to a CSV file
        anomalies.to_csv(f'anomalies/{first_tmc}_anomalies.csv', index=False)

        # Plot the data and anomalies
        plt.figure(figsize=(14, 7))
        plt.plot(tmc_data['measurement_tstamp'], tmc_data['speed'], label='Speed')
        plt.plot(tmc_data['measurement_tstamp'], tmc_data['historical_average_speed'], label='Historical Average Speed', linestyle='--')
        plt.scatter(anomalies['measurement_tstamp'], anomalies['speed'], color='red', label='Anomalies')
        plt.xlabel('Timestamp')
        plt.ylabel('Speed')
        plt.title(f'Traffic Speed and Anomalies for TMC {first_tmc}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'plots/{first_tmc}_anomalies_plot.png')
        plt.show()

        print("Processing complete. Anomalies and plot saved in 'anomalies' and 'plots' directories.")
else:
    print("Error: The probe data is empty.")
