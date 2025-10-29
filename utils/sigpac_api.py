"""
Utilidades para API SIGPAC - Métodos 1 y 2
"""
import geopandas as gpd
import requests
from io import BytesIO
from typing import Dict, Optional
import pandas as pd

URL_BASE = "https://sigpac-hubcloud.es/servicioconsultassigpac/query/recinfo/{pr}/{mu}/{ag}/{zo}/{po}/{pa}/{re}.geojson"

def descargar_por_codigos(dict_parcelas: Dict[int, str]) -> Optional[gpd.GeoDataFrame]:
    """Descarga parcelas por códigos SIGPAC"""
    gdf_sigpac = None
    
    for k, v in dict_parcelas.items():
        try:
            parcela_info = v.split(":")
            if len(parcela_info) != 5:
                continue
            
            pr, mu, po, pa, re = parcela_info
            ag = "0"
            zo = "0"
            
            url = URL_BASE.format(pr=pr, mu=mu, ag=ag, zo=zo, po=po, pa=pa, re=re)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            gdf_temp = gpd.read_file(BytesIO(response.content))
            gdf_temp['id_entrada'] = k
            gdf_temp['codigo_sigpac'] = v
            
            if gdf_sigpac is None:
                gdf_sigpac = gdf_temp
            else:
                gdf_sigpac = pd.concat([gdf_sigpac, gdf_temp], ignore_index=True)
        except:
            continue
    
    return gdf_sigpac


def calcular_estadisticas(gdf: gpd.GeoDataFrame) -> dict:
    """Calcula estadísticas básicas"""
    stats = {
        'num_parcelas': len(gdf),
        'superficie_total': 0,
        'superficie_media': 0
    }
    
    if 'superficie' in gdf.columns:
        stats['superficie_total'] = float(gdf['superficie'].sum())
        stats['superficie_media'] = float(gdf['superficie'].mean())
    
    return stats
