import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the accelerometer data
accelerometer_df = pd.read_csv("Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/accelerometer.csv")

# Remove the timestamp column and retain x, y, z columns
acc_formatted_df = accelerometer_df[['x', 'y', 'z']].copy()

# Convert data from 1/64g units to g units
acc_formatted_df[['x', 'y', 'z']] = acc_formatted_df[['x', 'y', 'z']] * (1/64)

# Set up the scaler to transform data to the range [-128, 127]
scaler = MinMaxScaler(feature_range=(-128, 127))
acc_formatted_df[['x', 'y', 'z']] = scaler.fit_transform(acc_formatted_df[['x', 'y', 'z']])

# Round and convert to integers to match ACC.csv format
acc_formatted_df = acc_formatted_df.round().astype(int)

# Prepare header and sample rate row
initial_timestamp = accelerometer_df['unix_timestamp'].iloc[0]

initial_timestamp = initial_timestamp / 1_000_000  # Convert to seconds
initial_timestamp = int(initial_timestamp)  # Convert to integer
print(initial_timestamp)

header = [initial_timestamp] * 3
sample_rate_row = [64] * 3

# Save the transformed data with header and sample rate row
output_path = "Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/transformed_ACC.csv"
with open(output_path, "w", newline='') as f:
    # Write header (initial timestamp)
    f.write(",".join(map(str, header)) + "\n")
    # Write sample rate row (32 Hz for each channel)
    f.write(",".join(map(str, sample_rate_row)) + "\n")
    # Manually write each row to avoid compatibility issues
    for _, row in acc_formatted_df.iterrows():
        f.write(",".join(map(str, row)) + "\n")

print("Transformation complete. The data has been saved to 'transformed_ACC.csv'.")
