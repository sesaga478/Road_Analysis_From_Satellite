import numpy as np
from osgeo import gdal, ogr
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import rasterio

def kmeans_tif_3b(tif_in,clusters,kmeans_out):
  ds = gdal.Open(tif_in)
  # Leer las bandas del GeoTIFF
  band1 = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
  band2 = ds.GetRasterBand(2).ReadAsArray().astype(np.float32)
  band3 = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)

  # Preparar los datos para el análisis de k-means
  rows, cols = band1.shape
  data = np.column_stack((band1.flatten(), band2.flatten(), band3.flatten()))
  print(data.shape)
  kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data)
  labels = kmeans.labels_
  print(set(labels))

  #MÉTRICAS
  unique_values, counts = np.unique(labels[labels != 0], return_counts=True)
  total_pixels = np.sum(counts)
  percentage_pixels = counts / total_pixels * 100
  print(np.round(percentage_pixels,decimals=2))

  plt.imshow(np.reshape(labels, (rows, cols)), cmap="viridis")
  plt.savefig(tif_in.replace('.tif','.svg'))
  plt.colorbar()
  plt.title(tif_in.split('/')[-1].split('.')[0])
  plt.show()


  results = labels.reshape(rows, cols)

  #EXPORTAR 1 RASTER
  driver = gdal.GetDriverByName("GTiff")
  kmeans_out = tif_in.replace('.tif','_kmeans.tif')
  output_ds = driver.Create(kmeans_out, cols, rows, 1, gdal.GDT_Int32)
  output_band = output_ds.GetRasterBand(1)
  output_band.WriteArray(results)

  # Establecer los metadatos y la proyección del nuevo archivo GeoTIFF
  output_ds.SetGeoTransform(ds.GetGeoTransform())
  output_ds.SetProjection(ds.GetProjection())

  ds = None
  output_ds = None
