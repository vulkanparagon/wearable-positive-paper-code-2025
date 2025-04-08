import pandas as pd

from Official_ACC_to_E4 import header

# Load the systolic peaks data
systolic_peaks_data = pd.read_csv('Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/systolic_peaks.csv')

# Convert systolic_peak_timestamp from nanoseconds to milliseconds and calculate IBI
systolic_peaks_data['systolic_peak_timestamp_ms'] = systolic_peaks_data['systolic_peak_timestamp'] / 1e6
systolic_peaks_data['IBI'] = systolic_peaks_data['systolic_peak_timestamp_ms'].diff() / 1e3  # Convert IBI from ms to seconds

# Drop the first row since it will have a NaN value for IBI (no previous peak to compare)
systolic_peaks_data_filtered = systolic_peaks_data.dropna(subset=['IBI'])  # Convert IBI to seconds

# Calculate initial timestamp for relative time
initial_timestamp = systolic_peaks_data_filtered['systolic_peak_timestamp'].iloc[0]

# Create a new DataFrame for output in the required format
ibi_output = pd.DataFrame({
    'Time (s)': (systolic_peaks_data_filtered['systolic_peak_timestamp'] - initial_timestamp) / 1e9,  # Convert to seconds
    'IBI Duration (s)': systolic_peaks_data_filtered['IBI']  # IBI already in seconds
})

header_time = initial_timestamp / 1e9 # Convert to seconds for header

# Update the column name to include the initial timestamp as the header
ibi_output.columns = [f"{int(header_time)}", "IBI"]

# Save the output to a CSV file if needed
ibi_output.to_csv('Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/IBI.csv', index=False)

# Display output
ibi_output.head()