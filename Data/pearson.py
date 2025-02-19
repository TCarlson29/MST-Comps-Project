import pandas as pd
import numpy as np

# Load the data from the CSV file
df = pd.read_csv("/Users/reedschubert/Desktop/Comps/TimeSeriesEMCI/Patient30_time_series_with_labels_filtered.csv")  # Replace with your actual CSV file path

# Compute Pearson correlation matrix
correlation_matrix = df.corr(method='pearson')

# Save the correlation matrix to a CSV file
correlation_matrix.to_csv("/Users/reedschubert/Desktop/Comps/MatricesEMCI/Patient30_connectivity_matrix.csv", index=True)
