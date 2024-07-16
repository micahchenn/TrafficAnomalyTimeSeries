import requests
import uuid
import time
import certifi

API_key = "80e7fd1270444f1ca112cba3fc4c836e"

def request_directory(mode):
    if mode == "PM_Export":
        return f"https://pda-api.ritis.org/v2/submit/pm?key={API_key}"
    elif mode == "PM_Result":
        return f"https://pda-api.ritis.org/v2/results/pm?key={API_key}&uuid="

def submit_pm_job():
    url = request_directory("PM_Export")
    job_uuid = str(uuid.uuid4())

    params = {
        "uuid": job_uuid,
        "groupSegments": [
            {
                "alias": "SegmentGroup1",
                "segments": {
                    "type": "tmc",
                    "ids": ['112+05857']
                }
            }
        ],
        "dataSourceId": "inrix_tmc",
        "requestIntervals": [
            {
                "dateRange": {"start": "2024-05-08", "end": "2024-07-09"},
                "dow": [0, 1, 2, 3, 4, 5, 6],
                "granularity": {"type": "minutes", "value": 1}
            }
        ],
        "metrics": [
            "bufferIndex", "planningTimeIndex", "travelTimeIndex", "congestion",
            "averageCongestion", "averageSpeed"
        ],
        "title": "Performance Metrics Job",
        "description": "Job for calculating performance metrics",
        "timeZone": "America/New_York",
        "country": "USA"
    }

    print(f"Submitting performance metrics job to {url} with parameters:")
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

def fetch_pm_result(job_uuid):
    url = request_directory("PM_Result") + job_uuid
    response = requests.get(url, verify=certifi.where())
    print("PM result response status code:", response.status_code)
    if response.status_code == 200:
        with open("pm_data.json", "w") as f:
            f.write(response.text)
        print("Data saved as pm_data.json")
    else:
        print(f"Error fetching PM result: {response.status_code}")

def main():
    job_uuid, job_id = submit_pm_job()
    if not job_uuid or not job_id:
        return
    while True:
        job_status = poll_job_status(job_id)
        if job_status.get("state") == "SUCCEEDED":
            fetch_pm_result(job_uuid)
            break
        elif job_status.get("state") == "FAILED":
            print("Job failed.")
            break

if __name__ == "__main__":
    main()
