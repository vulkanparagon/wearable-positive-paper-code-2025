import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm  # Progress bar library

# Define the base directory where all participants' data is stored
base_dir = 'Participant data (participant id,time)'


# Function to process data and create plots for each participant and date
def process_participant_data(participant_id, date):
    # Define the paths for each data file
    base_path = os.path.join(base_dir, participant_id, date, 'digital_biomarkers', 'aggregated_per_minute')

    # Extract the participant-specific numeric part from participant_id (e.g., '10' from '10-3YK3H151PR')
    participant_prefix = participant_id.split('-')[0]  # '10' in '10-3YK3H151PR'

    # Replace '1-1-10' with dynamic participant-specific ID in the file paths
    eda_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_eda.csv')
    pulse_rate_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_pulse-rate.csv')
    respiratory_rate_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_respiratory-rate.csv')
    prv_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_prv.csv')
    accelerometers_std_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_accelerometers-std.csv')
    activity_intensity_file = os.path.join(base_path, f'1-1-{participant_prefix}_{date}_activity-intensity.csv')

    # Check if all necessary files exist
    if not all(os.path.exists(f) for f in
               [eda_file, pulse_rate_file, respiratory_rate_file, prv_file, accelerometers_std_file,
                activity_intensity_file]):
        print(f"Some files are missing for participant {participant_id} on {date}, skipping this date.")
        return

    # Load datasets
    eda_data = pd.read_csv(eda_file)
    pulse_rate_data = pd.read_csv(pulse_rate_file)
    respiratory_rate_data = pd.read_csv(respiratory_rate_file)
    prv_data = pd.read_csv(prv_file)
    accelerometers_std_data = pd.read_csv(accelerometers_std_file)
    activity_intensity_data = pd.read_csv(activity_intensity_file)

    # Merge datasets on 'timestamp_unix'
    combined_data = eda_data[['timestamp_unix', 'participant_full_id', 'eda_scl_usiemens']].merge(
        pulse_rate_data[['timestamp_unix', 'pulse_rate_bpm']], on='timestamp_unix', how='outer').merge(
        respiratory_rate_data[['timestamp_unix', 'respiratory_rate_brpm']], on='timestamp_unix', how='outer').merge(
        prv_data[['timestamp_unix', 'prv_rmssd_ms']], on='timestamp_unix', how='outer').merge(
        accelerometers_std_data[['timestamp_unix', 'accelerometers_std_g']], on='timestamp_unix', how='outer').merge(
        activity_intensity_data[['timestamp_unix', 'activity_intensity']], on='timestamp_unix', how='outer')

    # Handle missing values
    combined_data.fillna(method='ffill', inplace=True)

    # Ensure 'timestamp_unix' and other feature columns are numeric
    combined_data['timestamp_unix'] = pd.to_numeric(combined_data['timestamp_unix'], errors='coerce')
    combined_data['eda_scl_usiemens'] = pd.to_numeric(combined_data['eda_scl_usiemens'], errors='coerce')
    combined_data['pulse_rate_bpm'] = pd.to_numeric(combined_data['pulse_rate_bpm'], errors='coerce')
    combined_data['respiratory_rate_brpm'] = pd.to_numeric(combined_data['respiratory_rate_brpm'], errors='coerce')
    combined_data['prv_rmssd_ms'] = pd.to_numeric(combined_data['prv_rmssd_ms'], errors='coerce')
    combined_data['accelerometers_std_g'] = pd.to_numeric(combined_data['accelerometers_std_g'], errors='coerce')
    combined_data['activity_intensity'] = pd.to_numeric(combined_data['activity_intensity'], errors='coerce')

    # Convert 'timestamp_unix' to readable datetime format (24-hour)
    combined_data['timestamp_readable'] = combined_data['timestamp_unix'].apply(
        lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%H:%M'))

    # Function to reduce number of x-ticks
    def reduce_ticks(ax, n=10):
        """Reduces the number of ticks shown on the x-axis."""
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::n])

    # Create the plot
    plt.figure(figsize=(15, 10))

    # Plot each modality
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(combined_data['timestamp_readable'], combined_data['eda_scl_usiemens'], label='EDA (µS)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('EDA (µS)')
    ax1.set_title('Electrodermal Activity')
    ax1.grid(True)
    reduce_ticks(ax1, n=60)
    plt.xticks(rotation=45)

    ax2 = plt.subplot(3, 2, 2)
    ax2.plot(combined_data['timestamp_readable'], combined_data['pulse_rate_bpm'], label='Pulse Rate (BPM)',
             color='orange')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Pulse Rate (BPM)')
    ax2.set_title('Pulse Rate')
    ax2.grid(True)
    reduce_ticks(ax2, n=60)
    plt.xticks(rotation=45)

    ax3 = plt.subplot(3, 2, 3)
    ax3.plot(combined_data['timestamp_readable'], combined_data['respiratory_rate_brpm'],
             label='Respiratory Rate (Breaths/min)', color='green')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Respiratory Rate (Breaths/min)')
    ax3.set_title('Respiratory Rate')
    ax3.grid(True)
    reduce_ticks(ax3, n=60)
    plt.xticks(rotation=45)

    ax4 = plt.subplot(3, 2, 4)
    ax4.plot(combined_data['timestamp_readable'], combined_data['prv_rmssd_ms'], label='PRV (RMSSD ms)', color='red')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('PRV (RMSSD ms)')
    ax4.set_title('Pulse Rate Variability')
    ax4.grid(True)
    reduce_ticks(ax4, n=60)
    plt.xticks(rotation=45)

    ax5 = plt.subplot(3, 2, 5)
    ax5.plot(combined_data['timestamp_readable'], combined_data['accelerometers_std_g'], label='Accelerometers STD (g)',
             color='purple')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Accelerometers STD (g)')
    ax5.set_title('Accelerometers STD')
    ax5.grid(True)
    reduce_ticks(ax5, n=60)
    plt.xticks(rotation=45)

    # ax6 = plt.subplot(3, 2, 6)
    # ax6.plot(combined_data['timestamp_readable'], combined_data['activity_intensity'], label='Activity Intensity',
    #          color='brown')
    # ax6.set_xlabel('Time')
    # ax6.set_ylabel('Activity Intensity')
    # ax6.set_title('Activity Intensity')
    # ax6.grid(True)
    # reduce_ticks(ax6, n=60)
    # plt.xticks(rotation=45)

    plt.tight_layout()

    # Save the plot to a directory
    save_dir = os.path.join(base_dir, participant_id, date, 'plots')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, f'stress_anxiety_modality_analysis_{date}.png')
    plt.savefig(save_path)

    print(f"Plot saved to: {save_path}")
    plt.close()


# Loop through all participants and dates
participants = [p for p in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, p))]
print(f"Total Participants: {len(participants)}")

# Processing participants with progress bar
for participant_id in tqdm(participants, desc="Processing Participants"):
    participant_path = os.path.join(base_dir, participant_id)
    dates = [d for d in os.listdir(participant_path) if os.path.isdir(os.path.join(participant_path, d))]

    for date in tqdm(dates, desc=f"Processing {participant_id}", leave=False):
        process_participant_data(participant_id, date)
