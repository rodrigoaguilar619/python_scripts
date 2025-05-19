import csv
import pandas as pd
import os

# Write to CSV
def write_to_csv(data_list, data_header, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_header.keys())
        writer.writeheader()
        #writer.writerows(data_list)

        for row in data_list:
            # Filter the dictionary to include only the fieldnames
            filtered_row = {key: row[key] for key in data_header if key in row}
            writer.writerow(filtered_row)

        output_file

def merge_csv(path_files, source_path):
    ##folder_path_files = 'path_to_your_csv_folder'

    # List to hold data from each file
    data_frames = []

    # Loop through all CSV files in the folder
    for file_name in os.listdir(path_files):
        if file_name.endswith('.csv'):
            file_path = os.path.join(path_files, file_name)
            df = pd.read_csv(file_path)
            data_frames.append(df)

    # Concatenate all dataframes
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Save to a new CSV file
    output_file = source_path + ".csv"
    combined_df.to_csv(output_file, index=False)