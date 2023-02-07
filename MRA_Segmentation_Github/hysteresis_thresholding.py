import numpy as np
import os
from os import path
import nibabel as nib
from scipy.ndimage import gaussian_filter
from skimage import filters

hessian_filtered_mra = "" #PATH TO HESSIAN FILTERED + RESAMPLED DATA
thresholded_dir = "" #PATH FOR HESSIAN FILTERED + RESAMPLED + HYSTERESIS THRESHOLDED DATA

imgs = os.listdir(hessian_filtered_mra)

#CHOOSE UPPER + LOWER THRESHOLDS
high_threshold = 29
low_threshold = 19
gaussian_filter_sigma = 0

# gaussian filter, HYSTERESIS CANNY EDGE DETECTOR then binary mask
#does not use maximum intensity value- the 99th percentile of the values
for MRA_file in imgs:
    if "Guys" in MRA_file:
        img_dir = path.join(hessian_filtered_mra, MRA_file) #create directory for each file name as iterates through 'if' command
        load_MRA = nib.load(img_dir)   #load nifty file
        MRA_img = load_MRA.get_fdata() #numpy array
        thresh_arr = gaussian_filter(MRA_img, sigma=gaussian_filter_sigma)
        percentile_element = np.percentile(MRA_img, 99.9)
        max_element = np.amax(thresh_arr)  # maximum intensity value in array
        L_thresh = (percentile_element / 100) * (high_threshold)
        H_thresh = (percentile_element / 100) * (low_threshold)
        #threshold = (max_element / 100) * (HH_percent_thresh) #finds 5% value of the maximum element in array
        #print(f'The threshold value for image {MRA_file} is: {threshold}')
        print(f'The upper threshold value for image {MRA_file} is: {H_thresh}, and the lower threshold value is: {L_thresh}, the percentile intensity is: {percentile_element}')
        hyst = filters.apply_hysteresis_threshold(thresh_arr, L_thresh, H_thresh).astype(int)
        non_zero = np.count_nonzero(hyst)
        print(f'Total number of non-zero voxels = {non_zero}')
        print(f'Percentage of vessel-voxels = {44564480 / non_zero}%')
        #thresh_arr = np.where(thresh_arr <= threshold, 0, 1)
        split_file_name = MRA_file.split('.nii')
        new_file_name = (split_file_name[0] + "_canny_threshold_h_" + str(high_threshold) + "_l_" + str(low_threshold) + "_gaussian_" + str(gaussian_filter_sigma) + ".nii.gz")
        new_dir = path.join(thresholded_dir, new_file_name)
        new_img_nii = nib.Nifti1Image(hyst, load_MRA.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_dir)  # saves the nifti file in folder
        print(f'Done thresholding of: {MRA_file}')

for MRA_file in imgs:
    if "HH" in MRA_file:
        img_dir = path.join(hessian_filtered_mra, MRA_file) #create directory for each file name as iterates through 'if' command
        load_MRA = nib.load(img_dir)   #load nifty file
        MRA_img = load_MRA.get_fdata() #numpy array
        thresh_arr = gaussian_filter(MRA_img, sigma=gaussian_filter_sigma)
        percentile_element = np.percentile(MRA_img, 99.99)
        max_element = np.amax(thresh_arr)  # maximum intensity value in array
        L_thresh = (percentile_element / 100) * (high_threshold)
        H_thresh = (percentile_element / 100) * (low_threshold)
        #threshold = (max_element / 100) * (HH_percent_thresh) #finds 5% value of the maximum element in array
        #print(f'The threshold value for image {MRA_file} is: {threshold}')
        print(f'The upper threshold value for image {MRA_file} is: {H_thresh}, and the lower threshold value is: {L_thresh}, the percentile intensity is: {percentile_element}')
        hyst = filters.apply_hysteresis_threshold(thresh_arr, L_thresh, H_thresh).astype(int)
        non_zero = np.count_nonzero(hyst)
        print(f'Total number of non-zero voxels = {non_zero}')
        print(f'Percentage of vessel-voxels = {44564480/non_zero}%')
        #thresh_arr = np.where(thresh_arr <= threshold, 0, 1)
        split_file_name = MRA_file.split('.nii')
        new_file_name = (split_file_name[0] + "_canny_threshold_h_" + str(high_threshold) + "_l_" + str(low_threshold) + "_gaussian_" + str(gaussian_filter_sigma) + ".nii.gz")
        new_dir = path.join(thresholded_dir, new_file_name)
        new_img_nii = nib.Nifti1Image(hyst, load_MRA.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_dir)  # saves the nifti file in folder
        print(f'Done thresholding of: {MRA_file}')
