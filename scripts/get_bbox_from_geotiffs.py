import rasterio,os,glob
import pandas as pd
from rasterio.warp import calculate_default_transform, transform_bounds
from pyproj import CRS
from leafmap import leafmap

def get_bbox_from_geotiffs(list_tif_in=glob.glob(r'F:\BID2023\crop_5000\*.tif'),
                           excel_out = r'F:\BID2023\bbox_data_5000_3.xlsx'):
    bbox_list = []

    for geotiff_file in list_tif_in:
        with rasterio.open(geotiff_file) as src:
            bounds = src.bounds
            transform = src.transform

            # Get the CRS of the source raster
            src_crs = src.crs

            # Define the target CRS as EPSG:4326 (GCS WGS 84)
            dst_crs = CRS.from_epsg(4326)

            # Calculate the default transform to target CRS
            transform, width, height = calculate_default_transform(src_crs, dst_crs, src.width, src.height, bounds.left, bounds.bottom, bounds.right, bounds.top)

            # Calculate the transformed bounds in the target CRS
            geo_bounds = transform_bounds(src_crs, dst_crs, bounds.left, bounds.bottom, bounds.right, bounds.top)

            bbox_list.append({
                'File': geotiff_file,
                'Name': geotiff_file.split('/')[-1],
                'MinX': bounds.left,
                'MinY': bounds.bottom,
                'MaxX': bounds.right,
                'MaxY': bounds.top,
                'Coordinates': [(bounds.left, bounds.bottom), (bounds.right, bounds.bottom),
                                (bounds.right, bounds.top), (bounds.left, bounds.top)],
                'PixelCoordinates': [(0, 0), (src.width, 0),
                                     (src.width, src.height), (0, src.height)],
                'GeoCoordinates': [(geo_bounds[0], geo_bounds[1]), (geo_bounds[2], geo_bounds[1]),
                                   (geo_bounds[2], geo_bounds[3]), (geo_bounds[0], geo_bounds[3])],
                'BoundingBox': [geo_bounds[0], geo_bounds[1], geo_bounds[2], geo_bounds[3]]
            })

    df = pd.DataFrame(bbox_list)        
    # Save the DataFrame to an Excel file
    
    df.to_excel(excel_out, index=False)
    print("Bounding box data saved to:", excel_out)        
    return bbox_list