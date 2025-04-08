import pandas as pd

# Load the file
file_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/eda.csv'
eda_data = pd.read_csv(file_path)

# Extract the initial timestamp (in seconds) and EDA values
initial_time = eda_data['unix_timestamp'].iloc[0] / 1e6  # Convert from microseconds to seconds
sampling_rate = 4  # Given fixed sampling rate

initial_time = int(initial_time)  # Convert to integer for consistent formatting
print(f"Initial timestamp: {initial_time}")

# Prepare data in the required format
formatted_data = [f"{initial_time}", f"{sampling_rate}"]
formatted_data.extend(eda_data['eda'].round(6).astype(str).tolist())

# Convert to single-column DataFrame for easier export
formatted_df = pd.DataFrame(formatted_data)

# Save to file
output_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/formatted_eda.csv'
formatted_df.to_csv(output_path, header=False, index=False)

# Output file path
print(output_path)
