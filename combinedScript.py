import subprocess
import sys
import time

def run_scripts():
    # Step 1: Run the probeRawData.py script
    result = subprocess.run([sys.executable, "probeRawData.py"])
    if result.returncode != 0:
        print("probeRawData.py failed. Exiting.")
        return  # Exit the loop if this script fails

    # Step 2: Run the extractData.py script to unzip the file
    result = subprocess.run([sys.executable, "extractData.py"])
    if result.returncode != 0:
        print("extractData.py failed. Exiting.")
        return  # Exit the loop if this script fails

    # Step 3: Run the algo.py script to analyze the data
    result = subprocess.run([sys.executable, "algo.py"])
    if result.returncode != 0:
        print("algo.py failed. Exiting.")
        return  # Exit the loop if this script fails

    # Step 4: Run the send_email.py script to send the results
    result = subprocess.run([sys.executable, "send_email.py"])
    if result.returncode != 0:
        print("send_email.py failed. Exiting.")
        return  # Exit the loop if this script fails

while True:
    run_scripts()
    print("Waiting for 5 minutes before running the scripts again...")
    time.sleep(300)  # Wait for 300 seconds (5 minutes) before running again
