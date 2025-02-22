# filters data from the universally common brain regions to find the specifically the left and right regions of the brain
# (maybe) also filters for randomly sized sets of regions (specific to Alzheimer's/EMCI patients??)

import csv
import os

EMCI_csv_files = [
    'filtered_EMCI_matrices/filtered_Patient1_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient2_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient3_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient4_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient5_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient6_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient7_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient8_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient9_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient10_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient11_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient12_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient13_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient14_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient15_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient16_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient17_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient18_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient19_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient20_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient21_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient22_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient23_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient24_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient25_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient26_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient27_connectivity_matrix.csv', 
    'filtered_EMCI_matrices/filtered_Patient28_connectivity_matrix.csv', 'filtered_EMCI_matrices/filtered_Patient29_connectivity_matrix.csv', 
]

# folder for simulated data
simulated_data = 'EMCI_simulated_data'

# creates folder if it doesn't exist
if not os.path.exists(simulated_data):
    os.makedirs(simulated_data)

def read_first_column_l(file_path):
    left_regions = set()

    if file_path.endswith('.csv'): # checks if the input is csv file
        with open (file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0].endswith('_L'): # makes sure the region is in the left hemisphere
                    left_regions.add(row[0]) # adds the first column to the set
    
    return left_regions

def read_first_column_r(file_path):
    right_regions = set()

    if file_path.endswith('.csv'): # checks if the input is csv file
        with open (file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0].endswith('_R'): # makes sure the region is in the right hemisphere
                    right_regions.add(row[0]) # adds the first column to the set
    
    return right_regions

def filter_left_regions(file_path, left_regions):
    filtered_left_data = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) # reads the first line

        # filters out the columns in left regions
        columns_to_keep = [0]

        for i in range(1, len(header)):
            if header[i] in left_regions:
                columns_to_keep.append(i)
        
        # adds the header / first row
        filtered_first_row = []
        for i in columns_to_keep:
            filtered_first_row.append(header[i])
        filtered_left_data.append(filtered_first_row)

        # adds the rest of the rows
        for row in reader:
            if row[0] in left_regions:
                filtered_row = []
                for i in columns_to_keep:
                    filtered_row.append(row[i])
                filtered_left_data.append(filtered_row)
        
        return filtered_left_data

def filter_right_regions(file_path, right_regions):
    filtered_right_data = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) # reads the first line

        # filters out the columns in right regions
        columns_to_keep = [0] # was having issues retaining the first column so started at 0

        for i in range(1, len(header)):
            if header[i] in right_regions:
                columns_to_keep.append(i)
        
        # adds the header / first row
        filtered_first_row = []
        for i in columns_to_keep:
            filtered_first_row.append(header[i])
        filtered_right_data.append(filtered_first_row)

        # adds the rest of the rows
        for row in reader:
            if row[0] in right_regions:
                filtered_row = []
                for i in columns_to_keep:
                    filtered_row.append(row[i])
                filtered_right_data.append(filtered_row)
        
        return filtered_right_data

if EMCI_csv_files:
    left_regions = read_first_column_l(EMCI_csv_files[0]) # gets the first column of the first filtered csv file with left regions
    right_regions = read_first_column_r(EMCI_csv_files[0]) # gets the first column of the first filtered csv file with right regions

    # prints left regions
    for item in left_regions:
        print(item)

    # prints right regions
    for item in right_regions:
        print(item)

    for file in EMCI_csv_files:
        filtered_data_1 = filter_left_regions(file, left_regions) # filters each file for left brain regions
        filtered_data_2 = filter_right_regions(file, right_regions) # filters each file for right brain regions

        output_file_1 = os.path.join(simulated_data, f"left_{os.path.basename(file)}") # allows the name change of csv file to be left
        output_file_2 = os.path.join(simulated_data, f"right_{os.path.basename(file)}") # allows the name change of csv file to be right

        # creates new csv file with left filtered data
        with open (output_file_1, mode='w', newline='', encoding='utf-8') as output_csv_l:
            writer = csv.writer(output_csv_l)
            writer.writerows(filtered_data_1)
        
        # creates new csv file with right filtered data
        with open (output_file_2, mode='w', newline='', encoding='utf-8') as output_csv_r:
            writer = csv.writer(output_csv_r)
            writer.writerows(filtered_data_2)
        
        # prints if successful csv file creation
        print(f"left matrix saved as {output_file_1}")

        # prints if successful csv file creation
        print(f"right matrix saved as {output_file_2}")
else:
    print("No .csv files found")
