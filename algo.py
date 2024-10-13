import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Capture the current day and time
current_day = datetime.now().strftime('%Y-%m-%d')
current_time = datetime.now().strftime('%H:%M:%S')

# Save the day and time to a CSV file
time_data = {'Day': [current_day], 'Time': [current_time]}
time_df = pd.DataFrame(time_data)
time_csv_path = 'Time.csv'
time_df.to_csv(time_csv_path, index=False)
logging.info(f"Day and time saved to {time_csv_path}")

# Define paths for the datasets
probe_data_path = 'probe_data/Probe-Data-Export.csv'
tmc_data_path = 'probe_data/TMC_Identification.csv'

# Load the datasets
logging.info("Loading datasets...")
probe_data = pd.read_csv(probe_data_path, parse_dates=['measurement_tstamp'])
tmc_data = pd.read_csv(tmc_data_path)
logging.info("Datasets loaded successfully.")

# Remove duplicate columns in the probe data
logging.info("Cleaning probe data by removing duplicate columns...")
columns_to_drop = ['historical_average_speed.1', 'travel_time_minutes.1']
probe_data_cleaned = probe_data.loc[:, ~probe_data.columns.duplicated()].drop(columns=columns_to_drop)

# Rename the column to match for merging
logging.info("Renaming columns for merging...")
probe_data_cleaned.rename(columns={'tmc_code': 'tmc'}, inplace=True)

# Merge probe data with TMC identification data on TMC
logging.info("Merging probe data with TMC identification data...")
data_merged = pd.merge(probe_data_cleaned, tmc_data, on='tmc', how='left')
logging.info("Data merged successfully.")

# Initialize anomaly columns
data_merged['is_anomaly'] = False
data_merged['is_long_window_anomaly'] = False
data_merged['binary_anomaly'] = 0

# Define parameters for anomaly detection
deviation_threshold = -10  # Threshold for speed deviation (negative for significant decrease)
sustained_period = 5  # Number of consecutive minutes for a short window anomaly
long_window_period = 10  # Number of consecutive minutes for a long window anomaly
long_deviation_threshold = -15  # Threshold for significant speed drop in long window
minimum_duration = 5  # Minimum duration in minutes to include the anomaly

# Function to detect and record anomalies
def detect_anomalies(data_segment):
    anomalies = []
    data_segment['speed_deviation'] = data_segment['speed'] - data_segment['historical_average_speed']
    data_segment['is_anomaly'] = (data_segment['speed_deviation'] < deviation_threshold).rolling(window=sustained_period).sum() >= sustained_period
    data_segment['is_long_window_anomaly'] = (data_segment['speed_deviation'] < long_deviation_threshold).rolling(window=long_window_period).sum() >= long_window_period
    
    current_event = None
    for index, row in data_segment.iterrows():
        if row['is_anomaly'] or row['is_long_window_anomaly']:
            if current_event is None:
                current_event = {
                    'start_time': row['measurement_tstamp'],
                    'end_time': row['measurement_tstamp'],
                    'tmc': row['tmc'],
                    'road': row['road'],
                    'intersection': row['intersection'],
                    'type': 'long_window' if row['is_long_window_anomaly'] else 'short_window'
                }
            else:
                current_event['end_time'] = row['measurement_tstamp']
            # Mark this specific minute as an anomaly in binary_anomaly
            data_segment.loc[index, 'binary_anomaly'] = 1
        else:
            if current_event is not None:
                duration = int((current_event['end_time'] - current_event['start_time']).total_seconds() / 60) + 1  # Add 1 minute to include both start and end
                if duration >= minimum_duration:
                    current_event['duration_minutes'] = duration
                    anomalies.append(current_event)
                current_event = None
    
    # If an anomaly was ongoing at the end of the data segment
    if current_event is not None:
        duration = int((current_event['end_time'] - current_event['start_time']).total_seconds() / 60) + 1
        if duration >= minimum_duration:
            current_event['duration_minutes'] = duration
            anomalies.append(current_event)
    
    return anomalies

# Detect anomalies for all TMC segments and save detailed summary
detailed_summary = []

logging.info("Detecting anomalies for all TMC segments...")
for tmc in data_merged['tmc'].unique():
    segment_data = data_merged[data_merged['tmc'] == tmc].copy()
    anomalies = detect_anomalies(segment_data)
    
    # Update flags in the main data for specific minutes
    data_merged.update(segment_data)
    
    # If no anomalies, add a placeholder entry
    if not anomalies:
        detailed_summary.append({
            'tmc': tmc,
            'road': segment_data['road'].iloc[0] if 'road' in segment_data.columns else '',
            'intersection': segment_data['intersection'].iloc[0] if 'intersection' in segment_data.columns else '',
            'start_time': '',
            'end_time': '',
            'type': '',
            'duration_minutes': ''
        })
    else:
        detailed_summary.extend(anomalies)

# Convert the detailed summary to a DataFrame and save it
detailed_summary_df = pd.DataFrame(detailed_summary)

# Ensure that 'start_time' and 'end_time' columns are included in the DataFrame
if 'start_time' not in detailed_summary_df.columns:
    detailed_summary_df['start_time'] = ''
if 'end_time' not in detailed_summary_df.columns:
    detailed_summary_df['end_time'] = ''

# Convert 'duration_minutes' to numeric, replacing non-numeric entries with 0
detailed_summary_df['duration_minutes'] = pd.to_numeric(detailed_summary_df['duration_minutes'], errors='coerce').fillna(0)

detailed_summary_df.to_csv('detailed_summary_of_anomalies.csv', index=False)
logging.info("Detailed summary of anomalies saved to detailed_summary_of_anomalies.csv")

# Save the combined data to a single CSV file
combined_csv_path = 'combined_data.csv'
data_merged.to_csv(combined_csv_path, index=False)
logging.info(f"Combined data saved to {combined_csv_path}")

# Summarize anomalies for each TMC and save summary to CSV
summary = []
for tmc in data_merged['tmc'].unique():
    segment_data = data_merged[data_merged['tmc'] == tmc]
    has_anomalies = segment_data['binary_anomaly'].any()
    
    # Recalculate the total duration of anomalies for this TMC based on detailed events
    total_duration = detailed_summary_df[detailed_summary_df['tmc'] == tmc]['duration_minutes'].sum()
    
    summary.append({
        'tmc': tmc,
        'road': segment_data['road'].iloc[0] if 'road' in segment_data.columns else '',
        'intersection': segment_data['intersection'].iloc[0] if 'intersection' in segment_data.columns else '',
        'has_anomalies': has_anomalies,
        'total_anomaly_duration_minutes': total_duration if total_duration > 0 else 0  # Ensure duration is set properly
    })

summary_df = pd.DataFrame(summary)
summary_df.to_csv('summary_of_anomalies.csv', index=False)
logging.info("Summary of anomalies saved to summary_of_anomalies.csv")
