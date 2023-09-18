# -*- coding: utf-8 -*-
"""
@author: SSALAZAR
"""
from osgeo import gdal
import numpy as np
import os,glob, cv2
from tqdm import tqdm


def crop(img_in="/content/Road_Analysis_From_Satellite/data_example/images/20230221_175753_SN29_L3_SR_MS_11_0.tif",
         SIZE=100,fol_crop='/content/crop', EXT='tif'):  

    if not os.path.exists(fol_crop): # here '100' corresponds to size by default
        os.makedirs(fol_crop)
        
    ds = gdal.Open(img_in)

    num_bands = ds.RasterCount
    data = []
    for i in range(num_bands):
        band = ds.GetRasterBand(i+1)
        band_data = band.ReadAsArray()
        data.append(band_data)
    data = np.array(data)
    img_np = np.transpose(data, (1, 2, 0))
    img_width, img_height, dimension = img_np.shape
    height_sizes = [SIZE]
    width_sizes =  [SIZE]
    print(img_np.shape)
    for height in tqdm(height_sizes):
        width=height
        k = 0
        for i in range(0, img_height, height):
            for j in range(0, img_width, width):
                try:
                    imagen_test_name = os.path.join(fol_crop,img_in.split('/')[-1].replace("."+EXT, '') + '_{}_{}_{}_{}_{}_1.{}'.format(i, j, k, height, width,EXT))
                    #print(imagen_test_name)
                    if not os.path.exists(imagen_test_name):
                        gdal.Translate(imagen_test_name, img_in,options='-srcwin {} {} {} {}'.format(j, i, width, height))
                except:
                    pass
                k+=1


    image_files = os.listdir(fol_crop)
    print(len(image_files))
    for image_file in image_files:
        #print(image_file)
        try:
            image_path = os.path.join(fol_crop, image_file)
            image = cv2.imread(image_path)
            if (image == [0, 0, 0]).all():
                # If the image is all black, delete it
                os.remove(image_path)
                
        except:
            pass

    print(len(os.listdir(fol_crop)))
