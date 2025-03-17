#Gets the shape and time dimension of an nii file

import nibabel as nib

# Load the NIfTI file
nii_file_path = '/Users/reedschubert/Desktop/Comps/NLNII/Patient1/Patient1.nii'
img = nib.load(nii_file_path)

#Get the image data
data = img.get_fdata()
print(data.shape)#Check the shape of the data