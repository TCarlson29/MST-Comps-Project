# File to find the universally common parts of the brain for each type of patient (NL and EMCI)
# Can change the input csv files for each different type of patient

# unfamiliar with sets but used geeksforgeeks and w3 schools for help with the functions:
# https://www.geeksforgeeks.org/sets-in-python/
# https://www.w3schools.com/python/ref_set_intersection_update.asp
# 

import csv

csv_files = [
            '"C:\Users\tjcar\Downloads\Patient1_connectivity_matrix.csv"', '"C:\Users\tjcar\Downloads\Patient2_connectivity_matrix.csv"'
            ]

# another way of doing whats above
# csv_folder = 'path the to google drive folder with csv files'

def read_first_column(file_path):
    brain_part_set = set() # used set because it doesn't allow for duplicate values

    if file_path.endswith('.csv'): # checks if the input is csv file
        with open (file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row: # make sure row isn't empty
                    brain_part_set.add(row[0]) # adds the first column to the set

    return brain_part_set

if csv_files:
    universal_brain_parts = read_first_column(csv_files[0]) # gets the first column of the first csv file

    for file in csv_files[1:]: # loops through all files until the end - want to start at 1 because of line above
        current_column = read_first_column(file)
        universal_brain_parts.intersection_update(current_column) # removes the uncommon parts of the brain - intersection_update returns the values present in both sets

    for item in universal_brain_parts:
        print(item)
else:
    print("No .csv files found")

