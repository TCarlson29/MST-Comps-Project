import nibabel as nib
from nilearn.image import resample_to_img
from nilearn.input_data import NiftiLabelsMasker
import pandas as pd
import numpy as np

# File paths
fmri_path = "/Users/reedschubert/Desktop/Comps/EMCINII/Patient30/Patient30.nii" #Gets fMRI data from the .nii format (was converted from the .dcm files)
aal_path = "/Users/reedschubert/Desktop/Comps/AAL3/AAL3v1.nii" #Gets the AAL3 template data from the .nii in AAL3's file
aal_txt_path = "/Users/reedschubert/Desktop/Comps/AAL3/AAL3v1_1mm.nii.txt"  #Gets the brain regions that correspond with the 1-170 brain regions (in AAL3's txt file)

# Load images
fmri_img = nib.load(fmri_path)
aal_img = nib.load(aal_path)

resampled_aal_img = resample_to_img(aal_img, fmri_img, interpolation='nearest') #Resample AAL3 to match fMRI dimensions

resampled_aal_path = "/Users/reedschubert/Desktop/Comps/ResampledEMCI/ResampledPatient30.nii" #path to save the new file 
nib.save(resampled_aal_img, resampled_aal_path) # Save the resampled AAL3 image as a new .nii file that we will work with

print("Resampled AAL3 shape:", resampled_aal_img.shape)#prints new shape spatial dimensions (X, Y, Z axes) to make sure it matches the fMRI data we have

# Check the unique labels (regions) in the resampled AAL3 image
resampled_aal_data = resampled_aal_img.get_fdata()
unique_labels = np.unique(resampled_aal_data)#get a list of all the unique labels that actually appear in the resampled image.

# Remove label 0 to get final list of unique labels that have data 
#(0 shouldn't count, it's used to represent background voxels, 
#or empty space in the image that don't correspond to brain areas)
print(f"Number of unique regions in resampled AAL3 before removing 0: {len(unique_labels)}") #Should be 156 for 155 unique regions that have data + label 0 w background voxels
non_zero_labels = unique_labels[unique_labels != 0] #Gets rid of label 0
print(f"Number of unique regions in resampled AAL3 after removing 0: {len(non_zero_labels)}") #Should be 155 for the 155 regions w data
print(f"Unique labels in resampled AAL3: {non_zero_labels}") #prints 1-170, because the possible labels themselves range from 1-170, but the number of 
#regions with data is only 155 (hence when taking len(non_zero_labels) gets you 155)

#Create a masker object with the resampled atlas
#Source: https://nilearn.github.io/dev/modules/generated/nilearn.maskers.NiftiLabelsMasker.html
#Params: 
#labels_img=resampled_aal_img Defines regions based on our resampled AAL atlas
#standardize=True The signal is z-scored. Timeseries are shifted to zero mean and scaled to unit variance.
#Z-Score is a statistical measurement of a score's relationship to the mean in a group of scores.
#Essentially we do this to make the regions more comparable, and make sure that in our Pearson correlation that each time series contributes equally
#detrend=True
#We detrend signals. This removes low-frequency trends in the signal (e.g., scanner drift) to focus on meaningful neural activity.
#This will help us prevent false correlations, and reduce bias in connectivity values
#More info here: https://users.soe.ucsc.edu/~daspence/detrending_fmri.html
#Essentially this helps us account for scanner instability
masker = NiftiLabelsMasker(labels_img=resampled_aal_img, standardize=True, detrend=True) #creates a masker object that will extract the average time series from each brain region defined in the resampled AAL3 atlas

#loads the fMRI image, 
#Applies the resampled AAL atlas (that now corresponds with the dimensions of the fMRI data)
#This means that each voxel in fmri_img is assigned to a brain region using the resampled AAL3 atlas.
#All voxels that share the same region label are grouped together.
#For each brain region, AVERAGES THE fMRI SIGNAL across all voxels in that region giving us a single representative time series per region
time_series = masker.fit_transform(fmri_img)#Extract the mean time series from each region

# Print the shape of the time series
print("Time series shape:", time_series.shape) #Should be (100, 155), meaning 100 time points with 155 regions
#We originally had 100 time points from the scan, this value won't be changed. This was just how the fMRI images were captured 

# Read the region names from the AAL3 text file
region_names = [] #initalizes the region list (for naming columns in dataset purpose)
with open(aal_txt_path, 'r') as file: #opens txt file in read mode
    for line in file: 
        fileLine = line.strip().split() #Gets each line of the file (format # region #)
        region_names.append(fileLine[1])  #Appends only the region name to the list (fileLine[0] and fileLine[2] hold numerical values)

#Remove regions in the list that have no data using non_zero_labels
#We do i+1 because indexing of list starts at 0, but non_zero labels goes from 1-170 
#ex region_names[0] corresponds to label 1 in the AAL3 atlas
#Essentially this goes through our list and will remove all brain regions with no data so that the columns align correspondingly with the data
#Also makes sure the region names we get from the txt file are also in the non_zero_labels
region_names_filtered = [region_names[i] for i in range(len(region_names)) if i + 1 in non_zero_labels]

#Ensure the number of regions in the text file matches the time series columns
print(f"Number of regions in filtered AAL3 text file: {len(region_names_filtered)}") #Should be 155 matching the 155 unique regions with data that we got from np.unique

if len(region_names_filtered) != time_series.shape[1]: #error echecking to make sure the regions for columns match with regions in the time series (155 regions)
    print(f"Mismatch: Regions in filtered text file: {len(region_names_filtered)}, Regions in time series: {time_series.shape[1]}")
else:
    # Convert the time series to a DataFrame with region names as column labels
    time_series_df = pd.DataFrame(time_series, columns=region_names_filtered)

    # Save the DataFrame to a CSV file
    time_series_df.to_csv('/Users/reedschubert/Desktop/Comps/TimeSeriesEMCI/Patient30_time_series_with_labels_filtered.csv', index=False)
