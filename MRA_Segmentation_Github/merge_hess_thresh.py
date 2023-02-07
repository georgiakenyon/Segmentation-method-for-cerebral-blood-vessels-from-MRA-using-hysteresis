#MERGE THE HESSIAN FILTERED + THRESHOLDED IMAGES
import numpy as np
import nibabel as nib
import os
from os import path

LOWER_HESS_DIR = "" #PATH TO RESAMPLED + (LOWER SIGMA) HESSIAN FILTERED + THRESHOLDED DATA
UPPER_HESS_DIR = "" #PATH TO RESAMPLED + (UPPER SIGMA) HESSIAN FILTERED + THRESHOLDED DATA
MERGED_DIR = "" ##PATH TO RESAMPLED + COMPLETE HESSIAN FILTERED + THRESHOLDED DATA

LOWER_HESS_IMG = sorted(os.listdir(LOWER_HESS_DIR))
UPPER_HESS_IMG = sorted(os.listdir(UPPER_HESS_DIR))

new = list(zip(LOWER_HESS_IMG, UPPER_HESS_IMG))

for i, j in new:
    if ".nii.gz" in i and j:
        lower_hess_img_dir = path.join(LOWER_HESS_DIR, i) #create directory for each file name as iterates through 'if' command
        upper_hess_img_dir = path.join(UPPER_HESS_DIR, j)
        MRA_l_hess = nib.load(lower_hess_img_dir)   #load nifty file
        lower_hess = MRA_l_hess.get_fdata() #numpy array
        MRA_u_hess = nib.load(upper_hess_img_dir)  # load nifty file
        upper_hess = MRA_u_hess.get_fdata()  # numpy array
        full_img = lower_hess + upper_hess
        binary_img = np.where(full_img > 0.0, 1.0, 0.0)
        split_file_name = i.split('.nii')
        new_file_name = (split_file_name[0] + "_merged" + ".nii.gz")
        new_out_dir = path.join(MERGED_DIR, new_file_name)
        new_img_nii = nib.Nifti1Image(binary_img, MRA_u_hess.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_out_dir)  # saves the nifti file in folder
        print(f'Done merging of: {i} and {j}')



