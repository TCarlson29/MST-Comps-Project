#Compares the shape between an nii file and the AAL3 template
import nibabel as nib
import numpy as np


#Load fMRI data
fmri_path = "/Users/reedschubert/Desktop/Comps/NlfTI/ADNI4_GE_UHP_20230131_13.nii"
fmri_img = nib.load(fmri_path)
fmri_data = fmri_img.get_fdata()

#Load AAL3 Atlas
aal_path = "/Users/reedschubert/Desktop/Comps/AAL3/AAL3v1.nii" 
aal_img = nib.load(aal_path)
aal_data = aal_img.get_fdata()

# Check that the fMRI data and atlas have the same dimensions
print("fMRI shape:", fmri_data.shape)
print("AAL3 shape:", aal_data.shape)
