import os
import pandas as pd
import zipfile

def detect_anomalies(file_path, window_size=30, threshold=3):
    # Read the data
    data = pd.read_csv(file_path)
    print(f"Columns in the CSV file: {data.columns}")
    
    # Check for required columns
    required_columns = ['measurement_tstamp', 'speed']
    if not all(column in data.columns for column in required_columns):
        print(f"Skipping {file_path}: Missing required columns")
        return pd.DataFrame()  # Return empty DataFrame for files without required columns
    
    # Ensure proper data types
    data['measurement_tstamp'] = pd.to_datetime(data['measurement_tstamp'])
    data.sort_values('measurement_tstamp', inplace=True)
    data['rolling_mean'] = data['speed'].rolling(window=window_size).mean()
    data['rolling_std'] = data['speed'].rolling(window=window_size).std()
    data['anomaly_score'] = (data['speed'] - data['rolling_mean']) / data['rolling_std']
    anomalies = data[abs(data['anomaly_score']) > threshold]
    return anomalies

def process_directory(directory, metadata_file):
    metadata = pd.read_csv(metadata_file)
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and "anomalies" not in filename:
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}")
            anomalies = detect_anomalies(file_path)
            if not anomalies.empty:
                anomalies = anomalies.merge(metadata, left_on='tmc_code', right_on='tmc', how='left')
                anomalies_output_path = os.path.join(directory, filename.replace(".csv", "_anomalies.csv"))
                anomalies.to_csv(anomalies_output_path, index=False)
                print(f"Anomalies saved to {anomalies_output_path}")

# Extract zip file
def extract_zip(file_path, extract_to):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Files extracted to {extract_to}")

# Define paths
zip_file_path = 'probe_data.zip'
extract_to = 'extracted_data'
metadata_file = 'extracted_data/TMC_Identification.csv'  # Path to the metadata CSV

# Ensure that previous files are not blocking the process
if os.path.exists(extract_to):
    for filename in os.listdir(extract_to):
        file_path = os.path.join(extract_to, filename)
        try:
            os.remove(file_path)
        except PermissionError:
            print(f"Skipping deletion of {file_path} due to permission error.")

# Extract files
extract_zip(zip_file_path, extract_to)

# Process extracted files
process_directory(extract_to, metadata_file)
