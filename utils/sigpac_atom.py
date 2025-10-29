"""
SIGPAC ATOM - Descarga oficial desde FEGA
"""
import geopandas as gpd
import requests
from zipfile import ZipFile
from io import BytesIO
import tempfile
import os
from typing import Optional, Union, List
from urllib.parse import quote


def descargar_sigpac(
    provincia: int,
    municipio: Union[int, str],
    superficie_max_ha: Optional[float] = None,
    pendiente_min_mil: Optional[int] = None,
    uso_sigpac: Optional[Union[str, List[str]]] = None,
    campana: str = "2024",
    formato: str = "gpkg"
) -> Optional[gpd.GeoDataFrame]:
    """
    Descarga recintos SIGPAC desde servicio ATOM oficial
    
    Parámetros:
    -----------
    provincia : int
        Código de provincia (ej: 14 para Córdoba)
    municipio : int o str
        Código de municipio (ej: "051" o 51)
    superficie_max_ha : float, opcional
        Superficie máxima en hectáreas
    pendiente_min_mil : int, opcional
        Pendiente mínima en tanto por mil
    uso_sigpac : str o list, opcional
        Uso(s) del suelo a filtrar (ej: "OV" para olivar)
    campana : str
        Año de campaña (por defecto "2024")
    formato : str
        Formato: "gpkg" o "shp"
    
    Retorna:
    --------
    GeoDataFrame con los recintos filtrados o None
    """
    
    cod_prov = str(provincia).zfill(2)
    cod_mun = str(municipio).zfill(3)
    formato = formato.lower()
    
    # Nombres de provincias
    nombres_provincias = {
        "01": "ARABA/ALAVA", "02": "ALBACETE", "03": "ALACANT/ALICANTE",
        "04": "ALMERIA", "05": "AVILA", "06": "BADAJOZ", "07": "BALEARS, ILLES",
        "08": "BARCELONA", "09": "BURGOS", "10": "CACERES", "11": "CADIZ",
        "12": "CASTELLO/CASTELLON", "13": "CIUDAD REAL", "14": "CORDOBA",
        "15": "CORUNA, A", "16": "CUENCA", "17": "GIRONA", "18": "GRANADA",
        "19": "GUADALAJARA", "20": "GIPUZKOA", "21": "HUELVA", "22": "HUESCA",
        "23": "JAEN", "24": "LEON", "25": "LLEIDA", "26": "RIOJA, LA",
        "27": "LUGO", "28": "MADRID", "29": "MALAGA", "30": "MURCIA",
        "31": "NAVARRA", "32": "OURENSE", "33": "ASTURIAS", "34": "PALENCIA",
        "35": "PALMAS, LAS", "36": "PONTEVEDRA", "37": "SALAMANCA",
        "38": "SANTA CRUZ DE TENERIFE", "39": "CANTABRIA", "40": "SEGOVIA",
        "41": "SEVILLA", "42": "SORIA", "43": "TARRAGONA", "44": "TERUEL",
        "45": "TOLEDO", "46": "VALENCIA/VALENCIA", "47": "VALLADOLID",
        "48": "BIZKAIA", "49": "ZAMORA", "50": "ZARAGOZA"
    }
    
    nombre_prov = nombres_provincias.get(cod_prov, "PROVINCIA")
    
    # Fechas a probar
    fechas_probar = ["20240115", "20240105", "20240201", "20250205", "20250215"]
    
    base_url = f"https://www.fega.gob.es/atom/{campana}/rec_{campana}"
    subdir = f"{cod_prov} - {nombre_prov}"
    subdir_encoded = quote(subdir)
    
    gdf = None
    
    for fecha in fechas_probar:
        nombre_archivo = f"{cod_prov}{cod_mun}_rec_{campana}_{fecha}_{formato}.zip"
        url = f"{base_url}/{subdir_encoded}/{nombre_archivo}"
        
        try:
            response = requests.get(url, timeout=120)
            
            if response.status_code == 404:
                continue
            
            response.raise_for_status()
            gdf = _procesar_zip(response.content, formato)
            
            if gdf is not None:
                break
        except:
            continue
    
    if gdf is None:
        return None
    
    # Añadir columna superficie_ha
    if 'dn_surface' in gdf.columns:
        gdf['superficie_ha'] = gdf['dn_surface'] / 10000
    
    # Aplicar filtros
    if superficie_max_ha and 'superficie_ha' in gdf.columns:
        gdf = gdf[gdf['superficie_ha'] <= superficie_max_ha].copy()
    
    if pendiente_min_mil and 'pendiente_media' in gdf.columns:
        gdf = gdf[gdf['pendiente_media'] > pendiente_min_mil].copy()
    
    if uso_sigpac and 'uso_sigpac' in gdf.columns:
        if isinstance(uso_sigpac, str):
            gdf = gdf[gdf['uso_sigpac'] == uso_sigpac].copy()
        elif isinstance(uso_sigpac, list):
            gdf = gdf[gdf['uso_sigpac'].isin(uso_sigpac)].copy()
    
    return gdf if len(gdf) > 0 else None


def _procesar_zip(contenido_zip: bytes, formato: str) -> Optional[gpd.GeoDataFrame]:
    """Procesa ZIP en memoria"""
    try:
        with ZipFile(BytesIO(contenido_zip)) as z:
            extension = '.gpkg' if formato == 'gpkg' else '.shp'
            
            archivo_geo = None
            for nombre in z.namelist():
                if nombre.lower().endswith(extension):
                    archivo_geo = nombre
                    break
            
            if not archivo_geo:
                return None
            
            with tempfile.TemporaryDirectory() as tmpdir:
                z.extractall(tmpdir)
                ruta = os.path.join(tmpdir, archivo_geo)
                gdf = gpd.read_file(ruta)
        
        return gdf
    except:
        return None