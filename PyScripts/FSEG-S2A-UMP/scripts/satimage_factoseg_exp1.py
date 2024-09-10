"""

Factorization based segmentation

"""
# Import required packages
import time
import math
import numpy as np
import rasterio as rio
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Import customized modules
import satellite_image_factoseg as satseg

def main():
    
    time0 = time.time()
    # Declare required directories and path 
    img_dir = "../S2A"
    out_dir = "../EXP1"
    input_path = img_dir + "Ibadan_enhanced_2048x2048.tif"
    input_path = "./M1.pgm"
    # img_dir = "./S2A/"
    # file_name = "M2.pgm"
    # file_name = "Ibadan_enhanced_image_from_S2A.png"
    # img_path = img_dir + file_name
    
    # Run segmentation: try different window size, with and without nonneg constraints
    # ws = 25
    # segmented_output = FacSeg_main(img_path, ws=ws, segn=0, omega=.045, nonneg_constraint=True)
    
    # Define filter bank and apply to image. for color images, convert rgb to grey scale and then apply filter bank
    filter_bank = [('log', .5, [3, 3]), ('log', 1, [5, 5]),
                   ('gabor', 1.5, 0), ('gabor', 1.5, math.pi/2), ('gabor', 1.5, math.pi/4), ('gabor', 1.5, -math.pi/4),
                   ('gabor', 2.5, 0), ('gabor', 2.5, math.pi/2), ('gabor', 2.5, math.pi/4), ('gabor', 2.5, -math.pi/4)]
    
    ws = 25
    segn = 0
    omega = .045
    nct = True
    # output_path = "./Ibadan_factbased_segmented_ws%d_ncT.tif" % (ws)
    # segmented_output = satseg.FacSeg_S2A_imagery(input_path=input_path,
    #                                              filter_bank=filter_bank,
    #                                              output_path=output_path,
    #                                              ws=ws, segn=segn, omega=omega,
    #                                              nonneg_constraint=nct)
    segmented_output = satseg.FacSeg_main(image_path=input_path,
                                          filter_bank=filter_bank,
                                          ws=ws, segn=segn, omega=omega,
                                          nonneg_constraint=nct)
    
    # Show results
    fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(12, 6))
    # ax[0].imshow(segmented_output[0], cmap='gray')
    # ax[1].imshow(segmented_output[1], cmap='gray_r')
    #
    sat_image = rio.open(input_path)
    rgb_image = rgb_S2A_image(sat_image)
    # sat_image = rio.open(output_path)
    # segmented_output = sat_image.read()
    ax[0].imshow(rgb_image, cmap='terrain')
    ax[1].imshow(segmented_output[0], cmap='terrain')
    
    #
    ax[0].set_title("Original S2A image")
    ax[1].set_title("Segmented image (ws = %d)" %(ws))

    print('\nFSEG total run time is about %0.2f seconds or %0.2f minutes.\n' % (time.time() - time0, (time.time() - time0)/60.))

    plt.tight_layout()
    plt.show()
    
    # Save composite texture features
    # output_feature_filename = "./example_rgb_1_output_ncF.npy"
    # # output_feature_filename = img_dir + file_name.split('_')[0] + '_' + "fseg_output_ws25_ncF.npy"
    # np.save(output_feature_filename, seg_out)
    
    # # Save visualized composite texture map
    # output_image_filename = img_dir + "./example_M2_output__ws%d_ncT.png" % (ws)
    # output_image_filename = img_dir + "./example_rgb_1_output_ws%d_ncT.png" % (ws)
    # output_image_filename = img_dir + file_name.split('_')[0] + '_' + "fseg_output_ws%d_ncT.png" % (ws)
    output_image_filename = img_dir + "example_S2A_output__ws%d_ncT.png" % (ws)
    fig.savefig(output_image_filename, bbox_inches='tight', dpi=300)
    


if __name__ == '__main__':
    
    main()
