#APPLY HESSIAN FILTER TO DATA
#Run with parameter: --sigma = σ (0.47 & 0.94 orig)

import argparse
import os
from os import path
import itk
from distutils.version import StrictVersion as VS

in_dir = "" #IN_DIR = MRA FILES TO BE INPUT
out_dir = "" #OUT_DIR = OUTPUT HESSIAN FILTERED IMAGES
sigma = "" #PARAMETER

IN_list = os.listdir(in_dir)

for image in IN_list:
    curr_img = image.split('.')
    in_img = curr_img[0]
    output_image = (in_img + "_BFC_BET_resampled_Hessian_" + sigma + ".nii.gz") #Rename image with appropriate details
    output_dir = path.join(out_dir, output_image)
    output_image = output_dir
    input_dir = path.join(in_dir, image)
    input_image = input_dir

    if VS(itk.Version.GetITKVersion()) < VS("5.0.0"):
        print("ITK 5.0.0 or newer is required.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Segment blood vessels.")
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--alpha1", type=float, default=0.5)
    parser.add_argument("--alpha2", type=float, default=2.0)
    args = parser.parse_args()
    input_image = itk.imread(input_image, itk.ctype("float"))

    hessian_image = itk.hessian_recursive_gaussian_image_filter(
        input_image, sigma=args.sigma
    )

    vesselness_filter = itk.Hessian3DToVesselnessMeasureImageFilter[
        itk.ctype("float")
    ].New()
    vesselness_filter.SetInput(hessian_image)
    vesselness_filter.SetAlpha1(args.alpha1)
    vesselness_filter.SetAlpha2(args.alpha2)

    itk.imwrite(vesselness_filter, output_image)
