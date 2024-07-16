import subprocess
import sys

# Step 1: Run the probeRawData.py script
result = subprocess.run([sys.executable, "probeRawData.py"])
if result.returncode != 0:
    print("probeRawData.py failed. Exiting.")
    exit(1)

# Step 2: Run the extractData.py script to unzip the file
result = subprocess.run([sys.executable, "extractData.py"])
if result.returncode != 0:
    print("extractData.py failed. Exiting.")
    exit(1)

# Step 3: Run the algo.py script to analyze the data
result = subprocess.run([sys.executable, "algo.py"])
if result.returncode != 0:
    print("algo.py failed.")
    exit(1)
