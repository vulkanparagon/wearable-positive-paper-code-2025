import fastavro
import numpy as np
import pandas as pd
import os
from datetime import datetime


# Function to extract participant ID from the folder structure
def extract_participant_id(avro_file):
    filename = os.path.basename(avro_file)
    participant_id = filename.split('_')[0]  # Extract the participant ID, e.g., '1-1-10'
    return participant_id


# Function to read Avro file and extract systolic peaks
def extract_systolic_peaks_from_avro(avro_file):
    try:
        with open(avro_file, 'rb') as f:
            avro_reader = fastavro.reader(f)
            avro_data = [record for record in avro_reader]

        systolic_peaks = avro_data[0]['rawData']['systolicPeaks']['peaksTimeNanos']
        return systolic_peaks
    except Exception as e:
        print(f"Error reading {avro_file}: {e}")
        return None


# Function to calculate IBI from systolic peaks
def calculate_ibi(systolic_peaks):
    systolic_peaks_seconds = [peak * 1e-9 for peak in systolic_peaks]  # Convert from nanoseconds to seconds
    ibi = np.diff(systolic_peaks_seconds)  # Calculate Inter-Beat Interval (IBI)
    timestamp_unix = systolic_peaks[1:]  # Start from the second systolic peak for IBI
    timestamp_iso = [datetime.utcfromtimestamp(ts * 1e-9).replace(microsecond=0).isoformat() for ts in timestamp_unix]
    return timestamp_unix, timestamp_iso, ibi


# Function to aggregate IBI data by minute
def aggregate_ibi_by_minute(df):
    df['minute'] = df['timestamp_iso'].dt.floor('min')  # Round the timestamps to the nearest minute
    df_agg = df.groupby('minute').agg({
        'timestamp_unix': 'first',  # Keep the first timestamp in that minute
        'timestamp_iso': 'first',  # Keep the first timestamp in that minute
        'participant_full_id': 'first',  # Keep the participant ID
        'ibi': 'mean',  # Average the IBI for each minute
        'missing_value_reason': 'first'  # Keep the first missing value reason (should be None)
    }).reset_index(drop=True)
    return df_agg


# Main function to process all Avro files and save aggregated IBI data for each participant and date
def process_all_participants_and_dates(base_directory):
    # Iterate through all participant directories
    for participant_dir in os.listdir(base_directory):
        participant_path = os.path.join(base_directory, participant_dir)

        if not os.path.isdir(participant_path):
            continue  # Skip if not a directory

        # Iterate through all date directories under the participant
        for date_dir in os.listdir(participant_path):
            date_path = os.path.join(participant_path, date_dir)

            if not os.path.isdir(date_path):
                continue  # Skip if not a directory

            # Process all Avro files for this participant and date
            process_all_avro_files(participant_path, date_path, participant_dir, date_dir)


# Process Avro files for a specific participant and date
def process_all_avro_files(participant_path, date_path, participant_id, date_dir):
    avro_files = []

    # Recursively find all Avro files under the 'raw_data' directory for the date
    for root, dirs, files in os.walk(os.path.join(date_path, "raw_data", "v6")):
        for file in files:
            if file.endswith(".avro"):
                avro_files.append(os.path.join(root, file))

    if not avro_files:
        print(f"No Avro files found for {participant_id} on {date_dir}")
        return

    all_data = []

    for avro_file in sorted(avro_files):
        print(f"Processing file: {avro_file}")
        # Extract systolic peaks from the Avro file
        systolic_peaks = extract_systolic_peaks_from_avro(avro_file)

        if systolic_peaks is None:
            print(f"Skipping file due to errors: {avro_file}")
            continue

        # Calculate IBI and generate timestamps
        timestamp_unix, timestamp_iso, ibi_data = calculate_ibi(systolic_peaks)

        if len(ibi_data) == 0:
            print(f"No IBI data found in file: {avro_file}")
            continue

        # Create a DataFrame for this file's data
        df = pd.DataFrame({
            'timestamp_unix': pd.to_numeric(timestamp_unix),
            'timestamp_iso': pd.to_datetime(timestamp_iso),
            'participant_full_id': participant_id,
            'ibi': pd.to_numeric(ibi_data),
            'missing_value_reason': [None] * len(ibi_data)
        })

        all_data.append(df)

    if not all_data:
        print(f"No valid data to concatenate for {participant_id} on {date_dir}")
        return

    # Concatenate all DataFrames from all Avro files
    combined_df = pd.concat(all_data)

    # Aggregate the data by minute
    aggregated_df = aggregate_ibi_by_minute(combined_df)

    # Define the output path for saving the aggregated CSV file
    output_dir = os.path.join(participant_path, date_dir, "digital_biomarkers", "aggregated_per_minute")
    os.makedirs(output_dir, exist_ok=True)

    output_csv_file = os.path.join(output_dir, f"{participant_id}_{date_dir}_ibi.csv")
    aggregated_df.to_csv(output_csv_file, index=False)

    print(f"Aggregated IBI data saved to {output_csv_file}")


# Main entry point for the script
if __name__ == "__main__":
    base_directory = r'Participant data (participant id,time)'
    process_all_participants_and_dates(base_directory)
