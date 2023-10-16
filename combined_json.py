import pandas as pd
import json
import os

# Directory where CSV files are located
input_directory = '/Users/oscaryu/Downloads/mp2-data'

# Initialize an empty dictionary to store data grouped by 'id'
data_by_id = {}

# List CSV files in the directory
csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]

# Process each CSV file and group data by 'id'
for csv_file in csv_files:
    file_path = os.path.join(input_directory, csv_file)
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        id_value = row['id']
        data = row.drop('id').to_dict()
        
        if id_value not in data_by_id:
            data_by_id[id_value] = data
        else:
            data_by_id[id_value].update(data)

# Convert the grouped data to a list of dictionaries
json_data = [{'id': id_value, **data} for id_value, data in data_by_id.items()]

# Save the JSON data to a file
output_file = 'combined_data.json'
with open(output_file, 'w') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)

print(f"Combined data saved to '{output_file}'")

