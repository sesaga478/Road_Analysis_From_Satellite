import geopandas as gpd
from shapely.geometry import LineString
import fiona
import rasterio
from pyproj import CRS
from shapely.geometry import box

#Take one kml and transform into shapefile
def kml_shp(kml_in,shp_out):
    fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by defaul
    gdf = gpd.read_file(kml_in, driver='kml')
    gdf=gdf[gdf['geometry'].astype(str).str.startswith('LINE')]
    gdf.to_file(shp_out, driver='ESRI Shapefile')

#Take one shapefile and buffer it
def shp_buf(buffer,shp_in,shp_out):
    gdf = gpd.read_file(shp_in)
    buffered_gdf = gdf.buffer(buffer)
    gdf['geometry']=buffered_gdf
    gdf.to_file(shp_out)

#Take a bigger shapefile and fit it based on geotif image
def shp_img_fit(shp_in,img_in,shp_out):
    with rasterio.open(img_in) as src:
        shapefile = gpd.read_file(shp_in)
        shapefile = shapefile.to_crs(CRS(src.crs))
        shapefile_extent = shapefile.total_bounds
        geotiff_extent = [src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top]
        intersection_geometry = box(*geotiff_extent).intersection(box(*shapefile_extent))
        if not intersection_geometry.is_empty:
            clipped_shapefile = shapefile.intersection(intersection_geometry)
            # Comprobar si el shapefile recortado tiene geometría válida
            if not clipped_shapefile.empty:
                shapefile['geometry']=clipped_shapefile
                shapefile=shapefile[~shapefile['geometry'].is_empty]
                display(shapefile.head(2))
                shapefile.to_file(shp_out)
