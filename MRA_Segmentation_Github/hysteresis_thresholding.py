import numpy as np
import os
from os import path
import nibabel as nib
from scipy.ndimage import gaussian_filter
from skimage import filters

HESSIAN_FILTERED_DIR = "" #PATH TO HESSIAN FILTERED + RESAMPLED DATA
THRESHOLDED_DIR = "" #PATH FOR HESSIAN FILTERED + RESAMPLED + HYSTERESIS THRESHOLDED DATA

imgs = os.listdir(HESSIAN_FILTERED_DIR)

#CHOOSE UPPER + LOWER THRESHOLDS
HIGH_THRESHOLD = 29
LOW_THRESHOLD = 19
#GAUSSIAN_FILTER_SIGMA = 0 #DO NOT USE GAUSSIAN IF USING HESSIAN AS IT IS IN-BUILT TO ITK HESSIAN FILTER

IMAGE_DIMENSIONS = [512, 512, 170] #IMAGE DIMENSIONS
no_voxels = np.prod(IMAGE_DIMENSIONS)
DATA_TYPE = "" #Differentiator of types of images, i.e. "Guys" or "HH" in IXI dataset

# gaussian filter, HYSTERESIS CANNY EDGE DETECTOR then binary mask
#does not use maximum intensity value- the 99th percentile of the values

for MRA_file in imgs:
    if DATA_TYPE in MRA_file:
        img_dir = path.join(HESSIAN_FILTERED_DIR, MRA_file) #create directory for each file name as iterates through 'if' command
        load_MRA = nib.load(img_dir)   #load nifty file
        MRA_img = load_MRA.get_fdata() #numpy array
        #smooth_arr = gaussian_filter(MRA_img, sigma=GAUSSIAN_FILTER_SIGMA) #GAUSSIAN FILTER (HESSIAN FILTER ALREADY HAS GAUSSIAN FILTER IF USING- IF NOT, REPLACE "MRA_FILE" WITH "smooth_array"
        percentile_element = np.percentile(MRA_img, 99.9)
        max_element = np.amax(MRA_img)  # maximum intensity value in array
        L_thresh = (percentile_element / 100) * (HIGH_THRESHOLD)
        H_thresh = (percentile_element / 100) * (LOW_THRESHOLD)
        #threshold = (max_element / 100) * (HH_percent_thresh) #finds 5% value of the maximum element in array
        print(f'The upper threshold value for image {MRA_file} is: {H_thresh}, and the lower threshold value is: {L_thresh}, the percentile intensity is: {percentile_element}')
        hyst = filters.apply_hysteresis_threshold(MRA_img, L_thresh, H_thresh).astype(int)
        non_zero = np.count_nonzero(hyst)
        print(f'Total number of non-zero voxels = {non_zero}')
        print(f'Percentage of vessel-voxels = {no_voxels / non_zero}%')
        #thresh_arr = np.where(thresh_arr <= threshold, 0, 1)
        split_file_name = MRA_file.split('.nii')
        new_file_name = (split_file_name[0] + "_canny_threshold_h_" + str(HIGH_THRESHOLD) + "_l_" + str(LOW_THRESHOLD) + "_gaussian_" + str(gaussian_filter_sigma) + ".nii.gz")
        new_dir = path.join(THRESHOLDED_DIR, new_file_name)
        new_img_nii = nib.Nifti1Image(hyst, load_MRA.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_dir)  # saves the nifti file in folder
        print(f'Done thresholding of: {MRA_file}')


