# TrafficAnomalyTimeSeries
TrafficAnomalyTimeSeries is a Python-based project designed to detect and analyze anomalies in traffic data over time. By leveraging time series analysis, this tool identifies unusual patterns or deviations in traffic flow, which can be crucial for traffic management and urban planning.


### Purpose
The primary goal of TrafficAnomalyTimeSeries is to provide a robust tool for Arcadis to monitor and analyze traffic conditions. By detecting anomalies in traffic data, such as sudden drops in speed or unexpected congestion, this tool can help identify potential issues like broken traffic lights or accidents, allowing for timely intervention.

## Data Acquisition
The data for this project is obtained through the RITIS PDA API. Specifically, we submit a request for traffic data, specifying the desired time range, granularity, and data fields. The data is then fetched, processed, and analyzed to detect anomalies.

## Anomaly Detection Algorithm
The core algorithm behind TrafficAnomalyTimeSeries involves the following steps:


- **Data Submission**: Using the requests library, we submit a job to the RITIS PDA API to export traffic data for a specified time range and granularity.
- **Polling for Job Completion**: The script polls the API at regular intervals to check the status of the submitted job. Once the job is complete, the data is downloaded.
- **Data Extraction**: The downloaded data, usually in a compressed format, is extracted for analysis.
- **Data Cleaning and Preparation**: The extracted data is cleaned to remove duplicates and merged with Traffic Message Channel (TMC) identification data.
- **Deviation Calculation**: Calculate the deviation of current traffic metrics (e.g., speed) from historical averages. This is done using the following steps:
  - Compute the difference between the current speed and the historical average speed for each time interval.
  - Apply a rolling window to smooth out short-term fluctuations and identify sustained deviations.
- **Anomaly Identification**: Identify anomalies by detecting significant deviations beyond a predefined threshold. Specifically:
  - An anomaly is flagged if the deviation exceeds a negative threshold (indicating a significant decrease in speed) for a sustained period.
  - The threshold and sustained period can be adjusted based on the specific requirements and sensitivity needed.
- **Visualization**: The results are visualized using matplotlib, highlighting detected anomalies for easy interpretation.


### Detailed Steps for Anomaly Detection
Deviation Threshold: A negative threshold is set to identify significant decreases in speed. For example, a threshold of -10 mph means that any sustained speed drop greater than 10 mph below the historical average will be flagged as an anomaly.
Sustained Period: To avoid false positives from short-term fluctuations, a sustained period (e.g., 5 minutes) is used. This means the speed must remain below the threshold for at least 5 consecutive minutes to be considered an anomaly.
Rolling Window: A rolling window is applied to calculate the sum of deviations over the sustained period. If the sum exceeds the threshold for the entire period, it is flagged as an anomaly.