import pandas as pd
import numpy as np
import os

def detect_anomalies(file_path):
    data = pd.read_csv(file_path)
    # Assuming 'speed' column exists in each CSV file
    window_size = 60
    threshold = 3

    data['rolling_mean'] = data['speed'].rolling(window=window_size).mean()
    data['rolling_std'] = data['speed'].rolling(window=window_size).std()
    data['z_score'] = (data['speed'] - data['rolling_mean']) / data['rolling_std']

    anomalies = data[(data['z_score'] > threshold) | (data['z_score'] < -threshold)]
    return anomalies

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            anomalies = detect_anomalies(file_path)
            anomalies_file_path = file_path.replace('.csv', '_anomalies.csv')
            anomalies.to_csv(anomalies_file_path, index=False)
            print(f"Anomalies saved to {anomalies_file_path}")

if __name__ == "__main__":
    extracted_data_dir = 'extracted_data'  # Directory where files are extracted
    process_directory(extracted_data_dir)
