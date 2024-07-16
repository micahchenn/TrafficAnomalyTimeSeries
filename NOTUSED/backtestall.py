import requests
import pandas as pd
import datetime
import uuid
import certifi
import numpy as np
import zipfile
import io

API_KEY = "80e7fd1270444f1ca112cba3fc4c836e"
BASE_URL = "https://pda-api.ritis.org/v2/get_bottlenecks"

def submit_job():
    url = f"{BASE_URL}?key={API_KEY}"
    json_request = {
        "dataSourceId": "here_tmc",
        "startDate": "2023-01-01",
        "endDate": "2023-12-31",
        "tmcs": ["101N13828", "101N13829"],
        "timeZone": "America/New_York",
        "uuid": str(uuid.uuid4()),
        "description": "My data export job"
    }
    response = requests.post(url, json=json_request, verify=certifi.where())
    if response.status_code == 200:
        return response.json()["uuid"]
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.content)
        return None

def download_data(uuid):
    url = f"{BASE_URL}/results/export?key={API_KEY}&uuid={uuid}"
    response = requests.get(url, verify=certifi.where())
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("downloaded_data")
        print("Data downloaded and extracted successfully.")
        return "downloaded_data/data.csv"
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.content)
        return None

def detect_anomalies(df, window_size=7, threshold=3):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df['Rolling_Mean'] = df['Impact'].rolling(window=window_size).mean()
    df['Rolling_Std'] = df['Impact'].rolling(window=window_size).std()
    df['Anomaly_Score'] = (df['Impact'] - df['Rolling_Mean']) / df['Rolling_Std']
    anomalies = df[np.abs(df['Anomaly_Score']) > threshold]
    return anomalies

def main():
    uuid = submit_job()
    print(f"Submitted job with UUID: {uuid}")
    
    if uuid:
        file_path = download_data(uuid)
        if file_path:
            bottleneck_data = pd.read_csv(file_path)
            bottleneck_data['Date'] = pd.to_datetime(bottleneck_data['Date'])
            bottleneck_data['Impact'] = bottleneck_data['volumeWeightedDelay'].astype(float)
            
            anomalies = detect_anomalies(bottleneck_data, window_size=30, threshold=3)
            print("Detected anomalies:")
            print(anomalies)

if __name__ == "__main__":
    main()
