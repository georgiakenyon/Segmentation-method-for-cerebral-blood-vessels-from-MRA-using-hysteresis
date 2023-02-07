import os
from nilearn.image import resample_img
from os import path
import nibabel as nib

in_dir = "" #PATH TO GET BRAIN EXTRACTED + BIAS FIELD NORMALISATION DATA
out_dir = "" #PATH TO SAVE BRAIN EXTRACTED + BIAS FIELD NORMALISATION + RESAMPLED DATA

imgs = os.listdir(in_dir)

for MRA_file in imgs:
    if ".nii.gz" in MRA_file:
        img_dir = path.join(in_dir, MRA_file) #create directory for each file name as iterates through 'if' command
        load_MRA = nib.load(img_dir)   #load nifty file
        affine = load_MRA.affine
        MRA_img = load_MRA.get_fdata() #numpy array
        resampled_img = resample_img(load_MRA, target_affine=affine, target_shape=(512,512,170), interpolation='nearest')
        split_file_name = MRA_file.split('.nii')
        new_file_name = (split_file_name[0] + "_resampled" + ".nii.gz") #RENAME FILES
        new_dir = path.join(out_dir, new_file_name)
        new_img_nii = nib.Nifti1Image(resampled_img, resampled_img.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_dir)  # saves the nifti file in folder
        print(f'Done resampling of: {MRA_file}')

