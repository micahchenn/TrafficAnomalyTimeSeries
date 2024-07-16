import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
traffic_data = pd.read_csv('Probe-Data-Export.csv')
tmc_info = pd.read_csv('TMC_Identification.csv')

# Convert the timestamp to a datetime object
traffic_data['measurement_tstamp'] = pd.to_datetime(traffic_data['measurement_tstamp'])

# Calculate the deviation from the historical average
traffic_data['deviation'] = traffic_data['speed'] - traffic_data['historical_average_speed']

# Define a threshold for anomaly detection
threshold = 10  # You can adjust this value

# Identify anomalies
traffic_data['anomaly'] = np.abs(traffic_data['deviation']) > threshold

# Merge with TMC information for better understanding
traffic_data = traffic_data.merge(tmc_info, left_on='tmc_code', right_on='tmc')

def plot_anomalies(traffic_data):
    plt.figure(figsize=(15, 10))
    for tmc_code in traffic_data['tmc_code'].unique():
        subset = traffic_data[traffic_data['tmc_code'] == tmc_code]
        plt.plot(subset['measurement_tstamp'], subset['speed'], label=f"{tmc_code} Speed")
        plt.plot(subset['measurement_tstamp'], subset['historical_average_speed'], label=f"{tmc_code} Historical Avg Speed", linestyle='--')
        
        anomalies = subset[subset['anomaly']]
        plt.scatter(anomalies['measurement_tstamp'], anomalies['speed'], color='red', label=f"{tmc_code} Anomaly")

    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Traffic Speed Anomalies')
    plt.legend()
    plt.show()

plot_anomalies(traffic_data)
