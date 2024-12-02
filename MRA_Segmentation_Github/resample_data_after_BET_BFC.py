import os
from nilearn.image import resample_img
from os import path
import nibabel as nib

# Define directories
in_dir = "" #PATH TO GET BRAIN EXTRACTED + BIAS FIELD NORMALISATION DATA
out_dir = "" #PATH TO SAVE BRAIN EXTRACTED + BIAS FIELD NORMALISATION + RESAMPLED DATA

# Ensure the output directory exists
os.makedirs(out_dir, exist_ok=True)

# List all files in the input directory
imgs = os.listdir(in_dir)

for MRA_file in imgs:
    if ".nii.gz" in MRA_file:
        img_dir = path.join(in_dir, MRA_file)  # Create full path for the input file
        load_MRA = nib.load(img_dir)  # Load NIfTI file
        resampled_img = resample_img(
            load_MRA,
            target_affine=load_MRA.affine,
            target_shape=(512, 512, 170),
            interpolation="nearest"
        )  # Resample the image

        # Generate new file name
        split_file_name = MRA_file.split(".nii")
        new_file_name = split_file_name[0] + "_resampled" + ".nii.gz"
        new_dir = path.join(out_dir, new_file_name)

        # Save the resampled image
        nib.save(resampled_img, new_dir)
        print(f"Done resampling of: {MRA_file}")
