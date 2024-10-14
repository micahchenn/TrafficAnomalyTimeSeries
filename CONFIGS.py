# -------------------------------------------------- -------------------------------------------------- 
# Configuration Section 
# -------------------------------------------------- -------------------------------------------------- 

# Note: Please modify the following variables as needed. I have provided a list of possible values for each variable. 

# Variable to toggle between Atlanta and Texas
CITY = "Atlanta"  # Change this to "Atlanta" when needed

# Variable to hold the time range for data export
TIME_RANGE = "day"  # Change this to "day", "week", "month", or "year"

# Variable to hold Email to send the updates to
EMAIL_LIST = ['sarahpalmer127@gmail.com', 'micah.chen@arcadis.com', 'sushihero73@gmail.com'] # Weimin's email is weimin.jin@arcadis.com

# -------------------------------------------------- -------------------------------------------------- 


# -------------------------------------------------- --------------------------------------------------
# Overview of the Program
# -------------------------------------------------- --------------------------------------------------

# 1. Run the combinedScript.py script to start the anomaly detection process.
# 2. The script will run the following scripts sequentially:
#     - probeRawData.py: Fetches raw traffic data from the API.
#     - extractData.py: Extracts the downloaded data.
#     - algo.py: Analyzes the data to detect anomalies.
#     - send_email.py: Sends an email with the anomaly summary.
# 3. The process will repeat every 5 minutes to check for new anomalies.

# Note: Make sure to update the configuration variables as needed before running the script and make it specific to the city you are working on.
#       Also you can run each individual script with the same command as running the combinedScript.py script.


# -------------------------------------------------- --------------------------------------------------
# Instructions on Running the Scripts
# -------------------------------------------------- --------------------------------------------------

# 1. Open a terminal or command prompt.
# 2. Navigate to the TrafficAnomalyTimeSeries directory.
        # use the command: cd TrafficAnomalyTimeSeries (cd means change directory)
        #  PS C:\Users\chenm4031\OneDrive - ARCADIS\DEBUG\TASharePoint\
        #  cd .\TrafficAnomalyTimeSeries\
# 3. Run the following command to start the anomaly detection process:
        # python combinedScript.py

# Full command
# cd .\TrafficAnomalyTimeSeries 
# python combinedScript.py
