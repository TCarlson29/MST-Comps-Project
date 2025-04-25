'''
Tanner Carlson
4/15/2025
Splits up universal brain regions every 5 nodes, selected randomly, then creates new csv files with each split
EMCI and NL
'''

import os
import csv
import random

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


# creates the directories to store random split matrices
random_filter_NL = 'NL_random_split_matrices'
random_filter_EMCI = 'EMCI_random_split_matrices'

# physically creates the folder if it doesn't exist
if not os.path.exists(random_filter_NL):
    os.makedirs(random_filter_NL)

if not os.path.exists(random_filter_EMCI):
    os.makedirs(random_filter_EMCI)

# Read the matrix, including labels from the first row and column, but skip the first row (column labels)
def read_matrix_with_labels(file_path):
    labels = []  # To store labels (first column)
    matrix = []  # To store the matrix values

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        
        # Skip the first row entirely (the column headers)
        next(reader)

        for row in reader:
            if row:
                labels.append(row[0])
                row_values = []
                for val in row[1:]:
                    if val:  # Check if the value is not empty
                        row_values.append(float(val))
                    else:
                        row_values.append(0.0)
                matrix.append(row_values)

    return labels, matrix

# Generate random chunks of the matrix (e.g., 5x5, 10x10) while keeping labels
def random_chunk_from_matrix(matrix, labels, chunk_size):
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0

    # Ensure the chunk size does not exceed the matrix dimensions
    if chunk_size > num_rows or chunk_size > num_cols:
        print(f"Error: Chunk size {chunk_size} exceeds matrix size {num_rows}x{num_cols}")
        return []

    # Randomly select unique indices for both rows and columns
    random.seed(74) # sets the random selection so it doesn't change every time I run this function
    selected_indices = random.sample(range(num_rows), chunk_size)

    # Extract the chunk of the matrix using the selected row and column indices
    chunk_matrix = []
    # Loop over the selected row indices
    for row_idx in selected_indices:
        row_chunk = []

        for col_idx in selected_indices:
            # Append the corresponding value from the matrix to the row chunk
            row_chunk.append(matrix[row_idx][col_idx])
        
        chunk_matrix.append(row_chunk)
    
    # Extract the corresponding labels for rows
    chunk_row_labels = []
    for row_idx in selected_indices:
        chunk_row_labels.append(labels[row_idx])

    # Extract the corresponding labels for columns
    chunk_col_labels = []
    for col_idx in selected_indices:
        chunk_col_labels.append(labels[col_idx])

    return chunk_row_labels, chunk_col_labels, chunk_matrix

# Function to save chunk data as CSV with labels
def save_chunk_as_csv(output_file, chunk_row_labels, chunk_col_labels, chunk_matrix):
    with open(output_file, mode='w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)

        # Write the label row (column labels) with an empty cell at the top-left corner
        writer.writerow([''] + chunk_col_labels)
        
        # Write the matrix rows with row labels
        for i, row in enumerate(chunk_matrix):
            writer.writerow([chunk_row_labels[i]] + row)

# Main loop for processing all files and saving random chunks in patient-specific folders
def process_files(csv_files, output_folder):
    for file in csv_files:
        # Extract the patient name from the file path (e.g., "Patient1", "Patient2", etc.)
        patient_name = os.path.basename(file).split('_')[0]
        
        # Create a folder for each patient
        patient_folder = os.path.join(output_folder, patient_name)
        os.makedirs(patient_folder, exist_ok=True)

        # Read the matrix and labels
        labels, matrix = read_matrix_with_labels(file)

        # Generate and save random chunks of different sizes
        for chunk_size in range(5, 146, 5):
            output_file = os.path.join(patient_folder, f"{patient_name}_random_chunk_{chunk_size}x{chunk_size}.csv")
            chunk_row_labels, chunk_col_labels, chunk_matrix = random_chunk_from_matrix(matrix, labels, chunk_size)

            # Save the chunk to the CSV file
            save_chunk_as_csv(output_file, chunk_row_labels, chunk_col_labels, chunk_matrix)
            
            print(f"Saved random chunk {chunk_size}x{chunk_size} for {patient_name} to {output_file}")

# Process EMCI and NL datasets
process_files(NL_csv_files, random_filter_NL)
process_files(EMCI_csv_files, random_filter_EMCI)