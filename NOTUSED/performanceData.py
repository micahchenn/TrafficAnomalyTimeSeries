import requests
import uuid
import time
import certifi
import json

API_key = "80e7fd1270444f1ca112cba3fc4c836e"

def request_directory(mode):
    if mode == "Network":
        return f"https://pda-api.ritis.org/v2/segment/search/tmcs?key={API_key}"
    elif mode == "Export":
        return f"https://pda-api.ritis.org/v2/submit/export?key={API_key}"
    elif mode == "PerformanceMetrics":
        return f"https://pda-api.ritis.org/v2/submit/pm?key={API_key}"
    elif mode == "Result":
        return f"https://pda-api.ritis.org/v2/results/pm?key={API_key}&uuid="

def submit_performance_metrics_job():
    url = request_directory("PerformanceMetrics")
    job_uuid = str(uuid.uuid4())

    params = {
        "uuid": job_uuid,
        "dataSourceId": "inrix_tmc",
        "country": "USA",
        "groupSegments": [{
            "alias": "SEGMENT_GROUP_1",
            "segments": {
                "type": "tmc",
                "ids": ['112N18004', '112-04980', '112N18006']
            }
        }],
        "percentiles": [50, 95],
        "requestIntervals": [{
            "dateRange": {
                "start": "2024-06-17",
                "end": "2024-06-24"
            },
            "dow": [0, 1, 2, 3, 4, 5, 6],
            "granularity": {
                "type": "minutes",
                "value": 1
            },
            "intervalName": "weekdays",
            "periodId": 0,
            "useDayOfWeekIntervalName": False
        }],
        "times": [{
            "start": "00:00:00",
            "end": "23:59:59"
        }]
    }

    print(f"Submitting performance metrics job to {url} with parameters:")
    print(json.dumps(params, indent=4))

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

def fetch_performance_metrics_result(job_uuid):
    url = request_directory("Result") + job_uuid
    response = requests.get(url, verify=certifi.where())
    print("Export result response status code:", response.status_code)
    if response.status_code == 200:
        with open("performance_metrics.json", "w") as f:
            json.dump(response.json(), f, indent=4)
        print("Data saved as performance_metrics.json")
    else:
        print(f"Error fetching export result: {response.status_code}")

def main():
    job_uuid, job_id = submit_performance_metrics_job()
    if not job_uuid or not job_id:
        return
    while True:
        job_status = poll_job_status(job_id)
        if job_status.get("state") == "SUCCEEDED":
            fetch_performance_metrics_result(job_uuid)
            break
        elif job_status.get("state") == "FAILED":
            print("Job failed.")
            break

if __name__ == "__main__":
    main()
