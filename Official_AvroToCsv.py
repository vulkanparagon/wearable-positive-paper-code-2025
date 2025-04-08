from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import csv
import os

## Define the location of the Avro file and output folder.
# macOS example:
# avro_file_path = "/Users/timmytommy/Data/Avros/1-1-100_1707311064.avro"
# output_dir = "/Users/timmytommy/Data/Output/"
#
# Windows example:
# avro_file_path = "C:/Data/Avros/1-1-100_1707311064.avro"
# output_dir = "C:/Data/Output/"
avro_file_path = "Participant data (participant id,time)/10-3YK3H151PR/2024-03-19/raw_data/v6/1-1-10_1710855484.avro"
output_dir = "Participant data (participant id,time)/10-3YK3H151PR/2024-03-19"


## Read Avro file
reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
data= next(reader)

## Uncomment the below 2 lines to print the Avro schema
# print(schema)
# print(" ")

## Export sensors data to csv files
# Accelerometer
acc = data["rawData"]["accelerometer"]
timestamp = [round(acc["timestampStart"] + i * (1e6 / acc["samplingFrequency"]))
	for i in range(len(acc["x"]))]
# Convert ADC counts in g
delta_physical = acc["imuParams"]["physicalMax"] - acc["imuParams"]["physicalMin"]
delta_digital = acc["imuParams"]["digitalMax"] - acc["imuParams"]["digitalMin"]
x_g = [val * delta_physical / delta_digital for val in acc["x"]]
y_g = [val * delta_physical / delta_digital for val in acc["y"]]
z_g = [val * delta_physical / delta_digital for val in acc["z"]]
with open(os.path.join(output_dir, 'accelerometer.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "x", "y", "z"])
    writer.writerows([[ts, x, y, z] for ts, x, y, z in zip(timestamp, x_g, y_g, z_g)])

# Gyroscope
gyro = data["rawData"]["gyroscope"]
timestamp = [round(gyro["timestampStart"] + i * (1e6 / gyro["samplingFrequency"]))
    for i in range(len(gyro["x"]))]
# Convert ADC counts in dps (degree per second)
delta_physical = gyro["imuParams"]["physicalMax"] - gyro["imuParams"]["physicalMin"]
delta_digital = gyro["imuParams"]["digitalMax"] - gyro["imuParams"]["digitalMin"]
x_dps = [val * delta_physical / delta_digital for val in gyro["x"]]
y_dps = [val * delta_physical / delta_digital for val in gyro["y"]]
z_dps = [val * delta_physical / delta_digital for val in gyro["z"]]
with open(os.path.join(output_dir, 'gyroscope.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "x", "y", "z"])
    writer.writerows([[ts, x, y, z] for ts, x, y, z in zip(timestamp, x_dps, y_dps, z_dps)])

    # Eda
eda = data["rawData"]["eda"]
timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
    for i in range(len(eda["values"]))]
with open(os.path.join(output_dir, 'eda.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "eda"])
    writer.writerows([[ts, eda] for ts, eda in zip(timestamp, eda["values"])])

# Temperature
tmp = data["rawData"]["temperature"]
timestamp = [round(tmp["timestampStart"] + i * (1e6 / tmp["samplingFrequency"]))
    for i in range(len(tmp["values"]))]
with open(os.path.join(output_dir, 'temperature.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "temperature"])
    writer.writerows([[ts, tmp] for ts, tmp in zip(timestamp, tmp["values"])])

# Tags
tags = data["rawData"]["tags"]
with open(os.path.join(output_dir, 'tags.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["tags_timestamp"])
    writer.writerows([[tag] for tag in tags["tagsTimeMicros"]])

# BVP
bvp = data["rawData"]["bvp"]
timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"]))
    for i in range(len(bvp["values"]))]
with open(os.path.join(output_dir, 'bvp.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "bvp"])
    writer.writerows([[ts, bvp] for ts, bvp in zip(timestamp, bvp["values"])])

# Systolic peaks
sps = data["rawData"]["systolicPeaks"]
with open(os.path.join(output_dir, 'systolic_peaks.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["systolic_peak_timestamp"])
    writer.writerows([[sp] for sp in sps["peaksTimeNanos"]])

# Steps
steps = data["rawData"]["steps"]
timestamp = [round(steps["timestampStart"] + i * (1e6 / steps["samplingFrequency"]))
    for i in range(len(steps["values"]))]
with open(os.path.join(output_dir, 'steps.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["unix_timestamp", "steps"])
    writer.writerows([[ts, step] for ts, step in zip(timestamp, steps["values"])])