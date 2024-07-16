import requests
import uuid
import time
import certifi

API_key = "80e7fd1270444f1ca112cba3fc4c836e"

def request_directory(mode):
    if mode == "Network":
        return f"https://pda-api.ritis.org/v2/segment/search/tmcs?key={API_key}"
    elif mode == "Export":
        return f"https://pda-api.ritis.org/v2/submit/export?key={API_key}"
    elif mode == "Result":
        return f"https://pda-api.ritis.org/v2/results/export?key={API_key}&uuid="

def submit_export_job():
    url = request_directory("Export")
    job_uuid = str(uuid.uuid4())

    all_columns = [
        "speed", "historical_average_speed", "average_speed",
        "reference_speed", "travel_time_minutes", "travel_time",
        "confidence_score", "confidence", "data_quality", "cvalue"
    ]

    params = {
        "uuid": job_uuid,
        "segments": {"type": "tmc", "ids": ['112P09580', '112P09581', '112N09580', '112P09582', '112N09581', '112-09580', '112N09582', '112-09581', '112+09580', '112-09582', '112P09575', '112P09586', '112+09581', '112-09583', '112P09576', '112+09582', '112-09584', '112N09575', '112N09586', '112+09583', '112-09585', '112N09576', '112P09578', '112+09584', '112-09575', '112P09579', '112+09585', '112-09576', '112N09578', '112+09586', '112-09577', '112N09579', '112+09576', '112-09578', '112+09577', '112-09579', '112+09578', '112+09579', '112P15844', '112N15844', '112-15844', '112-15845', '112+15844', '112+15845']},
        "dates": [{"start": "2024-01-01", "end": "2024-07-16"}],
        "dow": [0, 1, 2, 3, 4, 5, 6],
        "dsFields": [{"id": "inrix_tmc", "columns": all_columns}],
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
    response = requests.post(url, json=params, headers=headers, verify=certifi.where())
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
        response = requests.get(url, verify=certifi.where())
        print("Job status response status code:", response.status_code)
        response_json = response.json()
        print("Job status response content:", response_json)
        if response_json.get("state") in ["SUCCEEDED", "FAILED"]:
            return response_json
        print("Job not yet complete. Waiting...")
        time.sleep(60)  # Wait for 1 minute before polling again

def fetch_export_result(job_uuid):
    url = request_directory("Result") + job_uuid
    response = requests.get(url, verify=certifi.where())
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
