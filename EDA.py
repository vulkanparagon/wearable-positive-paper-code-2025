import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# File paths for the uploaded data
eda_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_eda.csv'
pulse_rate_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_pulse-rate.csv'
respiratory_rate_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_respiratory-rate.csv'
prv_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_prv.csv'
accelerometers_std_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_accelerometers-std.csv'
activity_intensity_file = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/digital_biomarkers/aggregated_per_minute/1-1-10_2024-03-19_activity-intensity.csv'

# Load each dataset
eda_data = pd.read_csv(eda_file)
pulse_rate_data = pd.read_csv(pulse_rate_file)
respiratory_rate_data = pd.read_csv(respiratory_rate_file)
prv_data = pd.read_csv(prv_file)
accelerometers_std_data = pd.read_csv(accelerometers_std_file)
activity_intensity_data = pd.read_csv(activity_intensity_file)

# Display the first few rows of each dataframe to understand their structure
eda_data.head(), pulse_rate_data.head(), respiratory_rate_data.head(), prv_data.head(), accelerometers_std_data.head(), activity_intensity_data.head()

# Merge all datasets on 'timestamp_unix' and 'participant_full_id' to form a combined dataset
combined_data = eda_data[['timestamp_unix', 'participant_full_id', 'eda_scl_usiemens']].merge(
    pulse_rate_data[['timestamp_unix', 'pulse_rate_bpm']], on='timestamp_unix', how='outer').merge(
    respiratory_rate_data[['timestamp_unix', 'respiratory_rate_brpm']], on='timestamp_unix', how='outer').merge(
    prv_data[['timestamp_unix', 'prv_rmssd_ms']], on='timestamp_unix', how='outer').merge(
    accelerometers_std_data[['timestamp_unix', 'accelerometers_std_g']], on='timestamp_unix', how='outer').merge(
    activity_intensity_data[['timestamp_unix', 'activity_intensity']], on='timestamp_unix', how='outer')

# Handle missing values: Use forward fill to impute missing data, assuming physiological metrics are continuous
combined_data.fillna(method='ffill', inplace=True)

# Display the cleaned and merged data
# import ace_tools as tools;
#
# tools.display_dataframe_to_user(name="Combined Data for Stress and Anxiety Analysis", dataframe=combined_data)

# Output the first few rows to verify the combined dataset
combined_data.head()

# Ensure that the 'timestamp_unix' and other feature columns are properly cast as numeric
combined_data['timestamp_unix'] = pd.to_numeric(combined_data['timestamp_unix'], errors='coerce')
combined_data['eda_scl_usiemens'] = pd.to_numeric(combined_data['eda_scl_usiemens'], errors='coerce')
combined_data['pulse_rate_bpm'] = pd.to_numeric(combined_data['pulse_rate_bpm'], errors='coerce')
combined_data['respiratory_rate_brpm'] = pd.to_numeric(combined_data['respiratory_rate_brpm'], errors='coerce')
combined_data['prv_rmssd_ms'] = pd.to_numeric(combined_data['prv_rmssd_ms'], errors='coerce')
combined_data['accelerometers_std_g'] = pd.to_numeric(combined_data['accelerometers_std_g'], errors='coerce')
combined_data['activity_intensity'] = pd.to_numeric(combined_data['activity_intensity'], errors='coerce')

# Convert 'timestamp_unix' to a readable datetime format (24-hour)
combined_data['timestamp_readable'] = combined_data['timestamp_unix'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%H:%M'))

# Define a function to reduce the number of x-ticks displayed
def reduce_ticks(ax, n=10):
    """Reduces the number of ticks shown on the x-axis to every nth tick."""
    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::n])

# Plot all relevant modalities in one figure
plt.figure(figsize=(15, 10))

# Plot EDA (Electrodermal Activity)
ax1 = plt.subplot(3, 2, 1)
ax1.plot(combined_data['timestamp_readable'], combined_data['eda_scl_usiemens'], label='EDA (µS)')
ax1.set_xlabel('Time')
ax1.set_ylabel('EDA (µS)')
ax1.set_title('Electrodermal Activity')
ax1.grid(True)
reduce_ticks(ax1, n=60)
plt.xticks(rotation=45)

# Plot Pulse Rate
ax2 = plt.subplot(3, 2, 2)
ax2.plot(combined_data['timestamp_readable'], combined_data['pulse_rate_bpm'], label='Pulse Rate (BPM)', color='orange')
ax2.set_xlabel('Time')
ax2.set_ylabel('Pulse Rate (BPM)')
ax2.set_title('Pulse Rate')
ax2.grid(True)
reduce_ticks(ax2, n=60)
plt.xticks(rotation=45)

# Plot Respiratory Rate
ax3 = plt.subplot(3, 2, 3)
ax3.plot(combined_data['timestamp_readable'], combined_data['respiratory_rate_brpm'], label='Respiratory Rate (Breaths/min)', color='green')
ax3.set_xlabel('Time')
ax3.set_ylabel('Respiratory Rate (Breaths/min)')
ax3.set_title('Respiratory Rate')
ax3.grid(True)
reduce_ticks(ax3, n=60)
plt.xticks(rotation=45)

# Plot PRV (Pulse Rate Variability)
ax4 = plt.subplot(3, 2, 4)
ax4.plot(combined_data['timestamp_readable'], combined_data['prv_rmssd_ms'], label='PRV (RMSSD ms)', color='red')
ax4.set_xlabel('Time')
ax4.set_ylabel('PRV (RMSSD ms)')
ax4.set_title('Pulse Rate Variability')
ax4.grid(True)
reduce_ticks(ax4, n=60)
plt.xticks(rotation=45)

# Plot Accelerometers STD
ax5 = plt.subplot(3, 2, 5)
ax5.plot(combined_data['timestamp_readable'], combined_data['accelerometers_std_g'], label='Accelerometers STD (g)', color='purple')
ax5.set_xlabel('Time')
ax5.set_ylabel('Accelerometers STD (g)')
ax5.set_title('Accelerometers STD')
ax5.grid(True)
reduce_ticks(ax5, n=60)
plt.xticks(rotation=45)

# # Plot Activity Intensity
# ax6 = plt.subplot(3, 2, 6)
# ax6.plot(combined_data['timestamp_readable'], combined_data['activity_intensity'], label='Activity Intensity', color='brown')
# ax6.set_xlabel('Time')
# ax6.set_ylabel('Activity Intensity')
# ax6.set_title('Activity Intensity')
# ax6.grid(True)
# reduce_ticks(ax6, n=60)
# plt.xticks(rotation=45)

plt.tight_layout()

# Create a directory for saving the plot if it doesn't exist
save_dir = 'Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Save the plot to the folder
save_path = os.path.join(save_dir, 'stress_anxiety_modality_analysis.png')
plt.savefig(save_path)

# Show the plot
plt.show()

# Print the save path for confirmation
print(f"Plot saved to: {save_path}")

