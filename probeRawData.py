import requests
import uuid
import time
from datetime import datetime, timedelta

API_key = "80e7fd1270444f1ca112cba3fc4c836e"


Atlanta = ['101+07819', '101P53309', '101+51797', '101+53205', '101+53216', '101+53227', '101+53238', '101+53249', '101+20106', '101+53139', '101-53207', '101-53218', '101N53318', '101N53208', '101N20109', '101+51798', '101+53316', '101+53206', '101+53228', '101+53239', '101+53129', '101+20107', '101-53318', '101-53208', '101-53219', '101N53308', '101N53319', '101N53209', '101-20109', '101+51799', '101+53207', '101-53308', '101N53309', '101+53208', '101+53219', '101P18190', '101+53319', '101+53209', '101P18180', '101N18190', '101+53309', '101P18170', '101P18181', '101N18180', '101N18170', '101N18181', '101P18172', '101P18183', '101-18180', '101P18173', '101P18184', '101+18190', '101-18170', '101N18183', '101+18180', '101-18171', '101N18173', '101N18184', '101P18186', '101+18170', '101+18181', '101-18172', '101-18183', '101P18187', '101+18171', '101N18186', '101+18172', '101P20091', '101N18187', '101P07134', '101P18178', '101P18189', '101+18173', '101P20092', '101+18184', '101P14350', '101P14372', '101-18186', '101-20090', '101P07135', '101N20091', '101P18179', '101P53060', '101-14370', '101P53181', '101P14340', '101P14351', '101P14362', '101P14373', '101-18176', '101N18178', '101N18189', '101-20091', '101N20092', '101-14360', '101P53171', '101P53061', '101-14371', '101N14350', '101N14372', '101-05153', '101P14330', '101P14341', '101P14352', '101-18177', '101N07134', '101N18179', '101N53060', '101+14370', '101N53181', '101P53150', '101-14350', '101P53161', '101P53062', '101N14340', '101P20051', '101N14351', '101N14362', '101P20194', '101N14373', '101+18176', '101+18187', '101P14331', '101P14342', '101P14353', '101-07134', '101-18178', '101N07135', '101-18189', '101-53180', '101+14360', '101N53171', '101N53061', '101+14371', '101-14351', '101P53173', '101N14330', '101-14373', '101P53184', '101N14341', '101N14352', '101+18177', '101P14332', '101P14343', '101P14354', '101P07820', '101-07135', '101+20091', '101P14376', '101-18179', '101-53170', '101-53060', '101N53150', '101+14350', '101N53161', '101+14361', '101N53062', '101+14372', '101N20051', '101N20194', '101P53251', '101-14330', '101P53141', '101-14341', '101P53152', '101-14352', '101N14331', '101P53064', '101-14374', '101P53185', '101N14342', '101N14353', '101+07134', '101P20196', '101+18178', '101+53180', '101P14333', '101P14344', '101+20092', '101P14377', '101-18169', '101-53061', '101+14340', '101+14351', '101N53173', '101-20194', '101N53184', '101P53230', '101P53241', '101P53252', '101P53131', '101-14331', '101P53142', '101-14342', '101P53153', '101-14353', '101P53054', '101P53175', '101N14332', '101P53065', '101-14375', '101P53186', '101P20043', '101N07820', '101N14354', '101+07135', '101P20197', '101N14376', '101+18179', '101+53170', '101+53181', '101P05622', '101P06953', '101P14334', '101-53161', '101N53152', '101+14352', '101-20195', '101N53064', '101+14374', '101N53185', '101P53220', '101P53231', '101P53242', '101N20196', '101-11186', '101P20110', '101-14332', '101-14343', '101P53055', '101P53176', '101N14333', '101-14376', '101N14344', '101N14377', '101+53171', '101+53061', '101P06954', '101P14335', '101P14346', '101P14379', '101P51790', '101-53162', '101N53251', '101-53173', '101N53141', '101-53184', '101+14342', '101N53153', '101+14353', '101N53054', '101N53175', '101-20196', '101N53065', '101+14375', '101N53186', '101N20043', '101N20197', '101P53133', '101-14333', '101P53144', '101-14344', '101P53166', '101P53056', '101N05622', '101N06953', '101N14334', '101-14377', '101P20045', '101P20199', '101+53150', '101+53062', '101P05624', '101P06955', '101P14347', '101P14358', '101-53130', '101-53251', '101-53141', '101N53230', '101-53152', '101N53241', '101-53163', '101N53131', '101N53252', '101-53174', '101+14331', '101N53142', '101-53064', '101-53185', '101+14343', '101+07820', '101+14354', '101N53055', '101N53176', '101+14376', '101P53211', '101P53222', '101P53233', '101P53244', '101-05622', '101-14334', '101P53145', '101-14345', '101P53156', '101P53167', '101P53057', '101P53178', '101N06954', '101-19944', '101N14335', '101-14378', '101P53189', '101N14346', '101N14379', '101N51790', '101+53162', '101P06956', '101P14337', '101-53230', '101+20195', '101P14359', '101-53241', '101N53220', '101N53231', '101-53153', '101N53242', '101-53164', '101-53054', '101-53175', '101N20110', '101+14332', '101+14344', '101N53166', '101P53311', '101P53201', '101+14377', '101P53212', '101N20045']
Houston = ['112P09580', '112P09581', '112N09580', '112P09582', '112N09581', '112-09580', '112N09582', '112-09581', '112+09580', '112-09582', '112P09575', '112P09586', '112+09581', '112-09583', '112P09576', '112+09582', '112-09584', '112N09575', '112N09586', '112+09583', '112-09585', '112N09576', '112P09578', '112+09584', '112-09575', '112P09579', '112+09585', '112-09576', '112N09578', '112+09586', '112-09577', '112N09579', '112+09576', '112-09578', '112+09577', '112-09579', '112+09578', '112+09579', '112P15844', '112N15844', '112-15844', '112-15845', '112+15844', '112+15845']

Data_Source = 'inrix_tmc'

def request_directory(mode):
    if mode == "Network":
        return f"https://pda-api.ritis.org/v2/segment/search/tmcs?key={API_key}"
    elif mode == "Export":
        return f"https://pda-api.ritis.org/v2/submit/export?key={API_key}"
    elif mode == "Result":
        return f"https://pda-api.ritis.org/v2/results/export?key={API_key}&uuid="

def get_today_dates():
    today = datetime.now()
    start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = start_of_today + timedelta(days=1)
    return start_of_today.strftime('%Y-%m-%d'), end_of_today.strftime('%Y-%m-%d')

def submit_export_job():
    url = request_directory("Export")
    job_uuid = str(uuid.uuid4())

    all_columns = [
        "speed", "historical_average_speed", "average_speed",
        "reference_speed", "travel_time_minutes", "travel_time",
        "confidence_score", "confidence", "data_quality", "cvalue"
    ]

    start_date, end_date = get_today_dates()

    params = {
        "uuid": job_uuid,
        "segments": {"type": "tmc", "ids": Atlanta},
        "dates": [{"start": start_date, "end": end_date}],
        "dow": [0, 1, 2, 3, 4, 5, 6],
        "dsFields": [{"id": "here_tmc", "columns": all_columns}], # Here TMC is the unique identifier for the TMC HOUSTON USES INRIX
        "title": "Probe Data Export",
        "description": "Export job for raw probe data",
        "granularity": {"type": "minutes", "value": 1},
        "includeIsoTzd": False,
        "timeZone": "America/New_York",
        "country": "USA",
        "outputFormat": "csv"
    }

    print(f"Submitting export job to {url} with parameters:")
    print(params)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=params, headers=headers, verify=False)  # Disable SSL verification here
    print("Response status code:", response.status_code)
    print("Response content:", response.content)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None, None

    response_json = response.json()
    job_id = response_json.get("id")
    return job_uuid, job_id

def poll_job_status(job_id):
    url = f"https://pda-api.ritis.org/v2/jobs/status?key={API_key}&jobId={job_id}"
    while True:
        response = requests.get(url, verify=False)  # Disable SSL verification here
        print("Job status response status code:", response.status_code)
        response_json = response.json()
        print("Job status response content:", response_json)
        if response_json.get("state") in ["SUCCEEDED", "FAILED"]:
            return response_json
        print("Job not yet complete. Waiting...")
        time.sleep(30)  # Wait for 30s before polling again

def fetch_export_result(job_uuid):
    url = request_directory("Result") + job_uuid
    response = requests.get(url, verify=False)  # Disable SSL verification here
    print("Export result response status code:", response.status_code)
    if response.status_code == 200:
        with open("probe_data.zip", "wb") as f:
            f.write(response.content)
        print("Data saved as probe_data.zip")
    else:
        print(f"Error fetching export result: {response.status_code}")

def main():
    job_uuid, job_id = submit_export_job()
    if not job_uuid or not job_id:
        return
    while True:
        job_status = poll_job_status(job_id)
        if job_status.get("state") == "SUCCEEDED":
            fetch_export_result(job_uuid)
            break
        elif job_status.get("state") == "FAILED":
            print("Job failed.")
            break

if __name__ == "__main__":
    main()