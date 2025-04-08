import pandas as pd

# Load the file
file_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/bvp.csv'
bvp_data = pd.read_csv(file_path)

# Convert the unix timestamp to seconds by dividing by 10^6
bvp_data['unix_timestamp'] = bvp_data['unix_timestamp'] / 1_000_000  # Convert to seconds



# Determine the initial time t0
t0 = bvp_data['unix_timestamp'].iloc[0]

t0 = int(t0) # Convert to integer

print(t0)

# Set the fixed sampling rate
sampling_rate = 64

# Reformat the data into a single-column format as requested
reformatted_data = pd.DataFrame()
reformatted_data['BVP'] = [f"{t0}", str(sampling_rate)] + bvp_data['bvp'].astype(str).tolist()

# Save the reformatted data to a new file
output_path = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/bvp_reformatted.csv'
reformatted_data.to_csv(output_path, header=False, index=False)
