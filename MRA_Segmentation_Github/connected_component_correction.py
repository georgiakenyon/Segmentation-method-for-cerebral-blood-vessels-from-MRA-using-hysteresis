import numpy as np
import nibabel as nib
import cc3d
import os
from os import path


img_dir = "" #PATH FOR RESAMPLED + HESSIAN FILTERED + THRESHOLDED + MERGED DATA
new_dir = "" #PATH FOR RESAMPLED + HESSIAN FILTERED + THRESHOLDED + MERGED DATA + CONNECTED COMPONENT DATA

imgs = os.listdir(img_dir)

for MRA_file in imgs:
    if ".nii.gz" in MRA_file:
        image_dir = path.join(img_dir, MRA_file) #create directory for each file name as iterates through 'if' command
        load_MRA = nib.load(image_dir)   #load nifty file
        MRA_img = load_MRA.get_fdata() #numpy array
        new_array = np.copy(MRA_img)
        labels_out, N = cc3d.connected_components(new_array, return_N=True)
        #labels_out, N = cc3d.largest_k(labels_out, k=3, connectivity=26, delta=0, return_N=True)
        labels_out = cc3d.dust(labels_out, threshold=100, connectivity=26, in_place=False)
        binary_label = np.where(labels_out > 0.0, 1, 0)
        split_file_name = MRA_file.split('.nii')
        new_file_name = (split_file_name[0] + "_connected_component" + ".nii.gz")
        new_out_dir = path.join(new_dir, new_file_name)
        new_img_nii = nib.Nifti1Image(binary_label, load_MRA.affine)  # produces new nifti file from array
        nib.save(new_img_nii, new_out_dir)  # saves the nifti file in folder
        print(f'Done connected component correction of: {MRA_file}')