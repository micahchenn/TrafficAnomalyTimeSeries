import pandas as pd
import numpy as np
import datetime
import uuid
import requests
import certifi

API_KEY = "80e7fd1270444f1ca112cba3fc4c836e"
BASE_URL = "https://pda-api.ritis.org/v2/get_bottlenecks"

def get_bottleneck_data(tmc_list, date):
    url = f"{BASE_URL}?key={API_KEY}"
    start_date = date.strftime("%Y-%m-%d")
    end_date = date.strftime("%Y-%m-%d")
    json_request = {
        "startDate": start_date,
        "endDate": end_date,
        "matchFullTmcQueue": True,
        "maxCount": 50000,
        "provider": "here_tmc",
        "timeZone": "America/New_York",
        "tmcs": tmc_list,
        "uuid": str(uuid.uuid4())
    }
    response = requests.post(url, json=json_request, verify=certifi.where())
    if response.status_code == 200:
        data = response.json()
        for item in data:
            item['Date'] = date.strftime("%Y-%m-%d")  # Add the 'Date' field manually
        return data
    else:
        print(f"Error: Received status code {response.status_code}")
        return []

def fetch_and_save_data(dates):
    tmc_list = ['101N13828', '101N13829']
    all_data = []
    for date in dates:
        print(f"Fetching data for {date}")
        data = get_bottleneck_data(tmc_list, date)
        all_data.extend(data)
    return pd.DataFrame(all_data)

# Generate a list of dates for the past year
start_date = datetime.date(2024, 5, 2)
end_date = datetime.date(2024, 7, 1)
dates = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]

bottleneck_data = fetch_and_save_data(dates)

# Save to a file
bottleneck_data.to_csv('/mnt/data/bottleneck_data.csv', index=False)

# Read the data back from the saved csv file
bottleneck_data = pd.read_csv('/mnt/data/bottleneck_data.csv')

# Ensure proper data types
bottleneck_data['Date'] = pd.to_datetime(bottleneck_data['Date'])
bottleneck_data['Impact'] = bottleneck_data['impact'].astype(float)

def detect_anomalies(df, window_size=30, threshold=3):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df['Rolling_Mean'] = df['Impact'].rolling(window=window_size).mean()
    df['Rolling_Std'] = df['Impact'].rolling(window=window_size).std()
    df['Anomaly_Score'] = (df['Impact'] - df['Rolling_Mean']) / df['Rolling_Std']
    anomalies = df[np.abs(df['Anomaly_Score']) > threshold]
    return anomalies

# Detect anomalies
anomalies = detect_anomalies(bottleneck_data, window_size=30, threshold=3)
anomalies.to_csv('/mnt/data/anomalies.csv', index=False)

anomalies.head(), '/mnt/data/anomalies.csv'
