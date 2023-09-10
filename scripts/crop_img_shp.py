import geopandas as gpd
import rasterio
from rasterio.mask import mask

def crop_img_shp(img_in,shp_in,img_out):

    # Read the image
    with rasterio.open(img_in) as src:
        # Crop the image using the road shapefile
        raster_crs = src.crs

    gdf = gpd.read_file(shp_in)
    gdf.to_crs(raster_crs, inplace=True)

    with rasterio.open(img_in) as src:
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        out_meta = src.meta.copy()

    # Update the metadata for the cropped GeoTIFF
    out_meta.update({
        'height': out_image.shape[1],
        'width': out_image.shape[2],
        'transform': out_transform
    })

    # Save the cropped GeoTIFF
    with rasterio.open(img_out, 'w', **out_meta) as dest:
        dest.write(out_image)
