import pandas as pd

# Load the original temperature data
file_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/temperature.csv'  # Update this path as necessary
temperature_data = pd.read_csv(file_path)

# Extract the initial timestamp and define the sampling rate
t0 = temperature_data['unix_timestamp'].iloc[0] / 1e6 # Convert from nanoseconds to seconds
sampling_rate = 4  # Provided sampling rate
t0 = int(t0)  # Convert to integer for consistent formatting
print(f"Initial timestamp: {t0}")

# Create a list with the formatted data
output_data_list = [
    f"{t0}",
    f"{sampling_rate}"
] + temperature_data['temperature'].astype(str).tolist()

# Convert the list to a DataFrame in a single-column format
output_data_fixed = pd.DataFrame(output_data_list)

# Save the reformatted data to a new file
output_file_path_fixed = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/formatted_temperature_data.csv'  # Specify your desired output path
output_data_fixed.to_csv(output_file_path_fixed, index=False, header=False)

print(f"Reformatted data saved to {output_file_path_fixed}")
