import fastavro

file_path = 'participant data/2024-03-18/20-3YK3J151H3/raw_data/v6/1-1-20_1710772454.avro'

# Open the AVRO file in binary mode
with open(file_path, 'rb') as file:
    # Load the AVRO reader
    reader = fastavro.reader(file)

    # Iterate through the records
    for record in reader:
        print(record)
