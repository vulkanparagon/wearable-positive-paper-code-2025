import pandas as pd

from Official_EDA_to_E4 import initial_time

# Load the original CSV file
file_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_pulse-rate.csv'
data = pd.read_csv(file_path)

# Extract the initial timestamp (first non-NaN in 'timestamp_unix' column)
initial_timestamp = data['timestamp_unix'].dropna().iloc[0]

initial_timestamp = int(initial_timestamp / 1e3)  # Convert to integer for consistent formatting
print(f"Initial timestamp: {initial_timestamp}")

# Define the sampling rate
sampling_rate = 1

# Get all non-NaN heart rate values from 'pulse_rate_bpm' and reset index
hr_values = data['pulse_rate_bpm'].dropna().reset_index(drop=True)

# Construct the new DataFrame with the specified format
hr_df = pd.DataFrame([initial_timestamp, sampling_rate] + hr_values.tolist(), columns=['HR'])

# Save the result to a CSV file
output_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/HR.csv'
hr_df.to_csv(output_path, index=False, header=False)

print(f"The CSV file has been saved at {output_path}")
