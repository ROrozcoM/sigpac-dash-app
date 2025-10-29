"""
Utilidades geoespaciales
"""
import geopandas as gpd
import tempfile
import os
from zipfile import ZipFile
from io import BytesIO
from typing import Tuple
import json


def exportar_geopackage(gdf: gpd.GeoDataFrame, nombre: str = "parcelas.gpkg") -> Tuple[bytes, str]:
    """Exporta a GeoPackage"""
    with tempfile.TemporaryDirectory() as tmpdir:
        ruta = os.path.join(tmpdir, nombre)
        gdf.to_file(ruta, driver="GPKG")
        with open(ruta, 'rb') as f:
            contenido = f.read()
    return contenido, nombre


def exportar_shapefile(gdf: gpd.GeoDataFrame, nombre_base: str = "parcelas") -> Tuple[bytes, str]:
    """Exporta a Shapefile (ZIP)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_shp = os.path.join(tmpdir, f"{nombre_base}.shp")
        gdf.to_file(ruta_shp, driver="ESRI Shapefile")
        
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zipf:
            for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                archivo = f"{nombre_base}{ext}"
                ruta_archivo = os.path.join(tmpdir, archivo)
                if os.path.exists(ruta_archivo):
                    zipf.write(ruta_archivo, archivo)
        
        zip_buffer.seek(0)
        contenido = zip_buffer.read()
    
    return contenido, f"{nombre_base}.zip"


def gdf_to_geojson(gdf: gpd.GeoDataFrame) -> dict:
    """Convierte GeoDataFrame a GeoJSON dict"""
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    return json.loads(gdf.to_json())


def calcular_centro_zoom(gdf: gpd.GeoDataFrame) -> Tuple[list, int]:
    """Calcula centro y zoom para mapa"""
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    
    bounds = gdf.total_bounds
    min_lon, min_lat, max_lon, max_lat = bounds
    
    centro_lat = (min_lat + max_lat) / 2
    centro_lon = (min_lon + max_lon) / 2
    
    extent = max(max_lon - min_lon, max_lat - min_lat)
    
    if extent > 1.0:
        zoom = 8
    elif extent > 0.1:
        zoom = 12
    else:
        zoom = 14
    
    return [centro_lat, centro_lon], zoom