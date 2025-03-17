#Reads information in dcm file
import pydicom

#Reading .dcm file
dcm_file = '/Users/reedschubert/Desktop/Comps/NL_Data/002_S_0295/Resting_State_fMRI/2012-05-10_15_42_37.0/I303069/ADNI_002_S_0295_MR_Resting_State_fMRI_br_raw_20120511095055857_1930_S150058_I303069.dcm'
dicom_data = pydicom.dcmread(dcm_file)
print(dicom_data)

