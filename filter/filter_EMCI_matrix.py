# File to find the universally common parts of the brain for each type of patient (NL and EMCI)
# Can change the input csv files for each different type of patient

# unfamiliar with sets but used geeksforgeeks and w3 schools for help with the functions:
# https://www.geeksforgeeks.org/sets-in-python/
# https://www.w3schools.com/python/ref_set_intersection_update.asp

# os help:
# https://docs.python.org/3/library/os.html

import csv
import os

EMCI_csv_files = [
            'EMCI_data/Patient1_connectivity_matrix.csv', 'EMCI_data/Patient2_connectivity_matrix.csv', 'EMCI_data/Patient3_connectivity_matrix.csv', 
            'EMCI_data/Patient4_connectivity_matrix.csv', 'EMCI_data/Patient5_connectivity_matrix.csv', 'EMCI_data/Patient6_connectivity_matrix.csv', 
            'EMCI_data/Patient7_connectivity_matrix.csv', 'EMCI_data/Patient8_connectivity_matrix.csv', 'EMCI_data/Patient9_connectivity_matrix.csv', 
            'EMCI_data/Patient10_connectivity_matrix.csv', 'EMCI_data/Patient11_connectivity_matrix.csv', 'EMCI_data/Patient12_connectivity_matrix.csv', 
            'EMCI_data/Patient13_connectivity_matrix.csv', 'EMCI_data/Patient14_connectivity_matrix.csv', 'EMCI_data/Patient15_connectivity_matrix.csv', 
            'EMCI_data/Patient16_connectivity_matrix.csv', 'EMCI_data/Patient17_connectivity_matrix.csv', 'EMCI_data/Patient18_connectivity_matrix.csv', 
            'EMCI_data/Patient19_connectivity_matrix.csv', 'EMCI_data/Patient20_connectivity_matrix.csv', 'EMCI_data/Patient21_connectivity_matrix.csv', 
            'EMCI_data/Patient22_connectivity_matrix.csv', 'EMCI_data/Patient23_connectivity_matrix.csv', 'EMCI_data/Patient24_connectivity_matrix.csv', 
            'EMCI_data/Patient25_connectivity_matrix.csv', 'EMCI_data/Patient26_connectivity_matrix.csv', 'EMCI_data/Patient27_connectivity_matrix.csv', 
            'EMCI_data/Patient28_connectivity_matrix.csv', 'EMCI_data/Patient29_connectivity_matrix.csv', 'EMCI_data/Patient30_connectivity_matrix.csv'
            ]

# another way of doing whats above
# csv_folder = 'path the to google drive folder with csv files'

# creates folder for NL data
filtered_EMCI_data = 'filtered_EMCI_matrices'

# creates the folder if it doesn't exist
if not os.path.exists(filtered_EMCI_data):
    os.makedirs(filtered_EMCI_data)

def read_first_column(file_path):
    brain_part_set = set() # used set because it doesn't allow for duplicate values

    if file_path.endswith('.csv'): # checks if the input is csv file
        with open (file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row: # make sure row isn't empty
                    brain_part_set.add(row[0]) # adds the first column to the set

    return brain_part_set

def filter_brain_parts(file_path, universal_brain_parts):
    filtered_data = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) # reads the first line

        # filters out the columns with universally common names
        columns_to_keep = []
        for i in range(len(header)):
            if header[i] in universal_brain_parts:
                columns_to_keep.append(i)
        
        # adds the header / first row
        filtered_first_row = []
        for i in columns_to_keep:
            filtered_first_row.append(header[i])
        filtered_data.append(filtered_first_row)
        
        # adds the rest of the rows
        for row in reader:
            if row[0] in universal_brain_parts:
                filtered_row = []
                for i in columns_to_keep:
                    filtered_row.append(row[i])
                filtered_data.append(filtered_row)
        
        return filtered_data
                

if EMCI_csv_files:
    universal_brain_parts = read_first_column(EMCI_csv_files[0]) # gets the first column of the first csv file

    for file in EMCI_csv_files[1:]: # loops through all files until the end - want to start at 1 because of line above
        current_column = read_first_column(file)
        universal_brain_parts.intersection_update(current_column) # removes the uncommon parts of the brain - intersection_update returns the values present in both sets

    # prints universal brain parts
    # for item in universal_brain_parts:
    #     print(item)

    for file in EMCI_csv_files:
        filtered_data = filter_brain_parts(file, universal_brain_parts) # filters each file for common parts

        output_file = os.path.join(filtered_EMCI_data, f"filtered_{os.path.basename(file)}") # allows the name change of csv file to be filtered

        # creates new csv file with filtered data
        with open (output_file, mode='w', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerows(filtered_data)
        
        # prints if successful csv file creation
        print(f"Filtered matrix saved as {output_file}")
else:
    print("No .csv files found")

