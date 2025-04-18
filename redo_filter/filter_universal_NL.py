'''
Tanner Carlson
4/15/2025
Filter universal brain regions out of the original csv files
NL only
'''

'''
set help:
https://www.geeksforgeeks.org/sets-in-python/
https://www.w3schools.com/python/ref_set_intersection_update.asp

os help:
https://docs.python.org/3/library/os.html
'''


import os
import csv

NL_csv_files = [
            'NL_data/Patient1_connectivity_matrix.csv', 'NL_data/Patient2_connectivity_matrix.csv', 'NL_data/Patient3_connectivity_matrix.csv', 
            'NL_data/Patient4_connectivity_matrix.csv', 'NL_data/Patient5_connectivity_matrix.csv', 'NL_data/Patient6_connectivity_matrix.csv', 
            'NL_data/Patient7_connectivity_matrix.csv', 'NL_data/Patient8_connectivity_matrix.csv', 'NL_data/Patient9_connectivity_matrix.csv', 
            'NL_data/Patient10_connectivity_matrix.csv', 'NL_data/Patient11_connectivity_matrix.csv', 'NL_data/Patient12_connectivity_matrix.csv', 
            'NL_data/Patient13_connectivity_matrix.csv', 'NL_data/Patient14_connectivity_matrix.csv', 'NL_data/Patient15_connectivity_matrix.csv', 
            'NL_data/Patient16_connectivity_matrix.csv', 'NL_data/Patient17_connectivity_matrix.csv', 'NL_data/Patient18_connectivity_matrix.csv', 
            'NL_data/Patient19_connectivity_matrix.csv', 'NL_data/Patient20_connectivity_matrix.csv', 'NL_data/Patient21_connectivity_matrix.csv', 
            'NL_data/Patient22_connectivity_matrix.csv', 'NL_data/Patient23_connectivity_matrix.csv', 'NL_data/Patient24_connectivity_matrix.csv', 
            'NL_data/Patient25_connectivity_matrix.csv', 'NL_data/Patient26_connectivity_matrix.csv', 'NL_data/Patient27_connectivity_matrix.csv', 
            'NL_data/Patient28_connectivity_matrix.csv', 'NL_data/Patient29_connectivity_matrix.csv'
            ]

# creates the folder name for the universal brain regions in the NL matrices
universal_regions_NL_matrices = 'NL_universal_regions_matrices'

# physically creates the folder if it doesn't exist
if not os.path.exists(universal_regions_NL_matrices):
    os.makedirs(universal_regions_NL_matrices)

# baseline set for the universal regions in the NL matrices
def read_first_column(file_path):
    brain_part_set = set() # used set because it doesn't allow for duplicate values

    if file_path.endswith('.csv'): # checks if the input is csv file
        with open (file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row: # make sure row isn't empty
                    brain_part_set.add(row[0]) # adds the first column to the set

    return brain_part_set

# filters through the matrix and keeps the universally common brain regions
def filter_brain_parts(file_path, universal_brain_regions):
    filtered_matrix = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) # reads the first line

        # filters out the columns with universally common names
        columns_to_keep = []
        for i in range(len(header)):
            if header[i] in universal_brain_regions:
                columns_to_keep.append(i)
        
        # adds the header / first row
        filtered_first_row = []
        for i in columns_to_keep:
            filtered_first_row.append(header[i])
        filtered_matrix.append(filtered_first_row)
        
        # adds the rest of the rows
        for row in reader:
            if row[0] in universal_brain_regions:
                filtered_row = []
                for i in columns_to_keep:
                    filtered_row.append(row[i])
                filtered_matrix.append(filtered_row)
        
        return filtered_matrix
                

# walks through each NL file and removes the uncommon brain regions in all matrices.
if NL_csv_files:
    universal_brain_regions = read_first_column(NL_csv_files[0]) # gets the first column of the first csv file

    # loops through all files and removes the uncommon regions of the brain - want to start at 1 because of line above
    for file in NL_csv_files[1:]: 
        current_column = read_first_column(file)
        # removes the uncommon regions of the brain - intersection_update returns the values present in both sets
        universal_brain_regions.intersection_update(current_column)

    for file in NL_csv_files:
        # gets the universal brain regions rows and columns from the csv files
        filtered_data = filter_brain_parts(file, universal_brain_regions)

        # changes the name of the output file for easier organization
        output_file = os.path.join(universal_regions_NL_matrices, f"universal_regions_{os.path.basename(file)}")

        # creates new csv file with universal regions data
        with open (output_file, mode='w', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerows(filtered_data)
        
        # prints if successful csv file creation
        print(f"Filtered matrix saved as {output_file}")
else:
    print("No .csv files found")