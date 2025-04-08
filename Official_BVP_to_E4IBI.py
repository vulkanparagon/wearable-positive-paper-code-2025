# import pandas as pd
# import numpy as np
#
# # Load the BVP data
# bvp_file_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/bvp.csv'
# bvp_data = pd.read_csv(bvp_file_path)
#
# # Function to detect peaks - simple threshold method
# def detect_peaks(bvp_values, threshold=0.05):
#     peaks = []
#     for i in range(1, len(bvp_values) - 1):
#         # Check if current value is a peak
#         if bvp_values[i] > threshold and bvp_values[i] > bvp_values[i - 1] and bvp_values[i] > bvp_values[i + 1]:
#             peaks.append(i)
#     return peaks
#
# # Detect peaks in the BVP data
# peaks_indices = detect_peaks(bvp_data['bvp'])
#
# # Extract corresponding timestamps of these peaks
# peak_timestamps = bvp_data['unix_timestamp'].iloc[peaks_indices].values
#
# # Calculate IBI by taking the difference between consecutive peak timestamps and convert to seconds
# ibi_values = np.diff(peak_timestamps) / 1_000_000  # Convert from microseconds to seconds
#
# # Calculate elapsed time from the initial timestamp for each IBI
# elapsed_time = (peak_timestamps[1:] - peak_timestamps[0]) / 1_000_000  # Convert from microseconds to seconds
#
# # Create a DataFrame matching the original IBI.csv format with header and arrangement
# ibi_df = pd.DataFrame({
#     'Time': elapsed_time,  # Elapsed time from start in seconds
#     'IBI': ibi_values      # IBI in seconds
# })
#
# # Save the generated IBI data to a CSV file with no index and matching header
# output_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/generated_ibi.csv'
# ibi_df.to_csv(output_path, index=False)
#
# print(f"IBI data saved to {output_path}")
