import requests
import uuid
import datetime
import pandas as pd
import certifi

# Hardcoded API key
API_key = "80e7fd1270444f1ca112cba3fc4c836e"

def request_directory(mode):
    if mode == "Network":
        return f"https://pda-api.ritis.org/v2/segment/search/tmcs?key={API_key}"
    elif mode == "Bottleneck":
        return f"https://pda-api.ritis.org/v2/get_bottlenecks?key={API_key}"

def Request_Network(data_source="HERE", seg_type="tmc"):
    url = request_directory("Network")
    json_content = requests.post(url, json={
        "dataSourceId": f"{data_source.lower()}_{seg_type}",
        "state": ["GA"]
    }, verify=certifi.where())
    return json_content.json()

def Request_Bottleneck(start_date, end_date, tmc_list, data_source="here_tmc"):
    url = request_directory("Bottleneck")
    RITIS_uuid = str(uuid.uuid4())

    tmc_list = [str(tmc).strip() for tmc in tmc_list if str(tmc).strip()]
    
    if not tmc_list:
        print("Error: TMC list is empty.")
        return []

    json_request = {
        "startDate": start_date,
        "endDate": end_date,
        "matchFullTmcQueue": True,
        "maxCount": 50000,
        "provider": data_source,
        "timeZone": "America/New_York",
        "tmcs": tmc_list,
        "uuid": RITIS_uuid
    }

    print(f"Requesting bottleneck data from {url} with parameters:")
    print(json_request)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=json_request, headers=headers, verify=certifi.where())
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    return response.json()

def BR_Result_Generator(tmc_list, date):
    tmc_group = tmc_partition(tmc_list)
    print(f"TMC Group: {tmc_group}")

    date_suffix = date.strftime("%Y%m%d")
    out_data = pd.DataFrame(columns=['TMC', 'Date', 'Volume Estimate', 'Base Impact', 'Congestion', 'Total Delay'])

    for k, v in tmc_group.items():
        date_text = date.strftime("%Y-%m-%d")
        print(f"Processing data for Group {k} on {date_text}")
        print(f"TMC List for Group {k}: {v}")
        br_data = Request_Bottleneck(date_text, date_text, v)
        print(f"Data for Group {k} of {date_text} is loaded.")

        for item in br_data:
            if isinstance(item, dict):
                try:
                    total_delay = float(item.get('volumeWeightedDelay', 0))
                    dataline = {
                        "TMC": item["tmcs"][0] if "tmcs" in item else "",
                        "Date": date_text,
                        "Volume Estimate": int(total_delay / float(item.get('delay', 1))),
                        "Base Impact": int(item.get('impact', 0)),
                        "Congestion": int(item.get("impactPercent", 0)),
                        "Total Delay": int(total_delay)
                    }
                    out_data = pd.concat([out_data, pd.DataFrame([dataline])], ignore_index=True)
                except Exception as e:
                    print(f"Error processing item: {item}, Error: {e}")

    out_path = f"RITIS_BR_{date_suffix}.csv"
    out_data.to_csv(out_path, index=False)
    print(f"Data saved locally as {out_path}")

    print(out_data)

    return out_data

def tmc_partition(tmc_list, subgroup_size=1400):
    tmc_group = {}
    for i, tmc in enumerate(tmc_list):
        group_num = (i // subgroup_size) + 1
        if group_num not in tmc_group:
            tmc_group[group_num] = []
        tmc_group[group_num].append(tmc)
    return tmc_group

def tmc_list_request():
    return ['101N13828', '101N13829']

def main(start_date=None):
    tmc_list = tmc_list_request()
    print(f"TMC List: {tmc_list}")

    if start_date is None:
        start_date = datetime.datetime(2019, 10, 21)
        end_date = datetime.datetime(2019, 10, 23)
    elif start_date.lower() == "now":
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=1)
    else:
        print("Invalid input: " + start_date)
        return

    current_date = start_date
    while (end_date - current_date).days >= 0:
        print(f"Generating bottleneck data for {current_date.strftime('%Y-%m-%d')}")
        BR_Result_Generator(tmc_list, current_date)
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main("now")
