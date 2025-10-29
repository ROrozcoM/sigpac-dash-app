"""
Página 2: Área en Mapa (BBOX)
Todo en un archivo
"""
import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_mantine_components as dmc
import dash_leaflet as dl
import base64
import geopandas as gpd
import json
import requests

from utils.geo_utils import gdf_to_geojson, calcular_centro_zoom, exportar_geopackage, exportar_shapefile

# Registrar página
dash.register_page(__name__, path="/bbox", name="Área en Mapa")

# =============================================================================
# LAYOUT
# =============================================================================

layout = dmc.Container(
    size="xl",
    children=[
        html.H1("Selección por Área en Mapa"),
        html.P("Dibuja un rectángulo en el mapa para descargar las parcelas del área"),
        
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 2fr", "gap": "20px"},
            children=[
                # Columna izquierda: Instrucciones y controles
                dmc.Paper(
                    p="md",
                    shadow="sm",
                    withBorder=True,
                    children=[
                        html.H3("Paso 1: Dibuja el área"),
                        html.P("Usa el botón ⬜ en el mapa para dibujar un rectángulo"),
                        
                        html.Div(id="bbox-info", style={"marginBottom": "15px"}),
                        
                        dmc.Divider(mb="md"),
                        
                        html.H3("Paso 2: Filtra (opcional)"),
                        
                        dmc.NumberInput(
                            id="input-superficie-bbox",
                            label="Superficie máxima (ha)",
                            placeholder="Todas",
                            min=0,
                            step=0.5,
                            mb="md"
                        ),
                        
                        dmc.Button(
                            "Mostrar Parcelas",
                            id="btn-descargar-bbox",
                            fullWidth=True,
                            color="green",
                            size="lg",
                            disabled=True,
                            mb="md"
                        ),
                        
                        html.Div(id="status-bbox"),
                        
                        dmc.Divider(mt="md", mb="md"),
                        
                        html.Div(
                            id="seccion-seleccion",
                            style={"display": "none"},
                            children=[
                                html.H3("Paso 3: Selecciona parcelas"),
                                html.P("Haz clic en las parcelas del mapa para seleccionarlas"),
                                
                                html.Div(id="info-seleccion", style={"marginBottom": "10px"}),
                                
                                dmc.Button(
                                    "Deseleccionar Todas",
                                    id="btn-deseleccionar",
                                    fullWidth=True,
                                    color="red",
                                    variant="subtle",
                                    size="sm",
                                    mb="md"
                                ),
                                
                                dmc.Group([
                                    dmc.Button("📦 GeoPackage", id="btn-gpkg-bbox", color="green", disabled=True),
                                    dmc.Button("📁 Shapefile", id="btn-shp-bbox", color="blue", disabled=True),
                                ])
                            ]
                        )
                    ]
                ),
                
                # Columna derecha: Mapa
                html.Div([
                    dl.Map(
                        id="mapa-bbox",
                        center=[37.25, -4.375],
                        zoom=7,
                        style={"width": "100%", "height": "600px"},
                        children=[
                            # Capa base
                            dl.TileLayer(
                                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                                attribution="Esri"
                            ),
                            # Etiquetas
                            dl.TileLayer(
                                url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
                                attribution="Esri"
                            ),
                            # EditControl para dibujar
                            dl.FeatureGroup([
                                dl.EditControl(
                                    id="edit-control",
                                    draw={
                                        "polyline": False,
                                        "polygon": False,
                                        "circle": False,
                                        "circlemarker": False,
                                        "marker": False,
                                        "rectangle": True
                                    },
                                    edit={"edit": False},
                                    position="topleft"
                                )
                            ]),
                            # Capa de parcelas (se añade dinámicamente)
                            html.Div(id="capa-parcelas")
                        ]
                    )
                ])
            ]
        ),
        
        # Stores
        dcc.Store(id="store-bbox"),
        dcc.Store(id="store-gdf-bbox"),
        dcc.Store(id="store-seleccionadas", data=[]),
        dcc.Download(id="download-gpkg-bbox"),
        dcc.Download(id="download-shp-bbox"),
    ]
)


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output("store-bbox", "data"),
    Output("bbox-info", "children"),
    Output("btn-descargar-bbox", "disabled"),
    Input("edit-control", "geojson"),
    prevent_initial_call=True
)
def capturar_bbox(geojson):
    """Captura el rectángulo dibujado"""
    if not geojson or "features" not in geojson or len(geojson["features"]) == 0:
        return None, None, True
    
    # Tomar el último rectángulo dibujado
    feature = geojson["features"][-1]
    coords = feature["geometry"]["coordinates"][0]
    
    # Extraer bbox
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    
    bbox = [min(lons), min(lats), max(lons), max(lats)]
    
    # Calcular área aproximada en hectáreas
    # 1 grado lat ≈ 111 km, 1 grado lon ≈ 111 km * cos(lat)
    import math
    lat_center = (min(lats) + max(lats)) / 2
    altura_km = abs(max(lats) - min(lats)) * 111
    anchura_km = abs(max(lons) - min(lons)) * 111 * math.cos(math.radians(lat_center))
    area_ha = altura_km * anchura_km * 100  # km² a ha
    
    info = dmc.Alert(
        f"✅ Área seleccionada: {area_ha:.2f} ha",
        color="green"
    )
    
    return bbox, info, False


@callback(
    Output("store-gdf-bbox", "data"),
    Output("status-bbox", "children"),
    Input("btn-descargar-bbox", "n_clicks"),
    State("store-bbox", "data"),
    State("input-superficie-bbox", "value"),
    prevent_initial_call=True
)
def descargar_bbox(n, bbox, sup_max):
    """Descarga parcelas del bbox usando API SIGPAC"""
    if not bbox:
        return None, dmc.Alert("No hay área seleccionada", color="yellow")
    
    try:
        # Usar requests directamente a la API SIGPAC OGC
        min_lon, min_lat, max_lon, max_lat = bbox
        
        base_url = "https://sigpac-hubcloud.es/ogcapi/collections/recintos/items"
        params = {
            'f': 'json',
            'limit': 5000,
            'bbox': f"{min_lon},{min_lat},{max_lon},{max_lat}"
        }
        
        response = requests.get(base_url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        if 'features' not in data or len(data['features']) == 0:
            return None, dmc.Alert("No se encontraron parcelas en el área", color="yellow")
        
        # Crear GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(data['features'], crs="EPSG:4326")
        
        # Filtrar por superficie si se especifica
        if sup_max and 'superficie' in gdf.columns:
            gdf = gdf[gdf['superficie'] <= sup_max].copy()
        
        if len(gdf) == 0:
            return None, dmc.Alert("No hay parcelas que cumplan los filtros", color="yellow")
        
        # Añadir ID único
        gdf['id_parcela'] = range(len(gdf))
        
        return gdf.to_json(), dmc.Alert(f"✅ {len(gdf)} parcelas descargadas. Haz clic en el mapa para seleccionarlas", color="green")
    
    except Exception as e:
        return None, dmc.Alert(f"Error: {str(e)}", color="red")


@callback(
    Output("capa-parcelas", "children"),
    Output("seccion-seleccion", "style"),
    Input("store-gdf-bbox", "data"),
    Input("store-seleccionadas", "data"),
    prevent_initial_call=True
)
def mostrar_parcelas(gdf_json, seleccionadas):
    """Muestra las parcelas en el mapa con colores según selección"""
    if not gdf_json:
        return None, {"display": "none"}
    
    gdf = gpd.read_file(gdf_json, layer='recinto' if '.gpkg' in str(gdf_json) else None)
    
    # Crear una capa por cada parcela para poder colorearlas individualmente
    capas = []
    
    for idx, row in gdf.iterrows():
        # Determinar color según si está seleccionada
        color = "#00ff00" if str(idx) in seleccionadas else "#3388ff"
        opacity = 0.7 if str(idx) in seleccionadas else 0.4
        
        geojson_feature = {
            "type": "Feature",
            "geometry": row.geometry.__geo_interface__,
            "properties": {"id": str(idx)}
        }
        
        capa = dl.GeoJSON(
            data=geojson_feature,
            id={"type": "parcela", "index": str(idx)},
            style={
                "fillColor": color,
                "color": "#ffffff",
                "weight": 2,
                "fillOpacity": opacity
            },
            hoverStyle={
                "fillColor": "#ffff00",
                "fillOpacity": 0.8,
                "weight": 3
            }
        )
        capas.append(capa)
    
    return capas, {"display": "block"}


@callback(
    Output("store-seleccionadas", "data"),
    Output("info-seleccion", "children"),
    Output("btn-gpkg-bbox", "disabled"),
    Output("btn-shp-bbox", "disabled"),
    Input({"type": "parcela", "index": dash.dependencies.ALL}, "n_clicks"),
    Input("btn-deseleccionar", "n_clicks"),
    State("store-seleccionadas", "data"),
    State({"type": "parcela", "index": dash.dependencies.ALL}, "id"),
    prevent_initial_call=True
)
def gestionar_seleccion(n_clicks_list, n_deselect, seleccionadas, ids_list):
    """Gestiona la selección de parcelas por clic"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return seleccionadas, "", True, True
    
    trigger_id = ctx.triggered[0]["prop_id"]
    
    # Deseleccionar todas
    if "btn-deseleccionar" in trigger_id:
        return [], "0 parcelas seleccionadas", True, True
    
    # Click en parcela
    if "parcela" in trigger_id:
        # Extraer el índice de la parcela clickeada
        import json
        trigger_dict = json.loads(trigger_id.split(".")[0])
        parcela_id = trigger_dict["index"]
        
        if seleccionadas is None:
            seleccionadas = []
        
        if parcela_id in seleccionadas:
            # Deseleccionar
            seleccionadas = [s for s in seleccionadas if s != parcela_id]
        else:
            # Seleccionar
            seleccionadas = seleccionadas + [parcela_id]
        
        num_sel = len(seleccionadas)
        info = dmc.Alert(f"✅ {num_sel} parcela(s) seleccionada(s)", color="blue") if num_sel > 0 else "0 parcelas seleccionadas"
        disabled = num_sel == 0
        
        return seleccionadas, info, disabled, disabled
    
    return seleccionadas, "", True, True


@callback(
    Output("download-gpkg-bbox", "data"),
    Input("btn-gpkg-bbox", "n_clicks"),
    State("store-gdf-bbox", "data"),
    State("store-seleccionadas", "data"),
    prevent_initial_call=True
)
def descargar_gpkg_bbox(n, gdf_json, seleccionadas):
    if not gdf_json or not seleccionadas:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    
    # Filtrar solo las seleccionadas
    ids = [int(i) for i in seleccionadas]
    gdf_sel = gdf[gdf['id_parcela'].isin(ids)]
    
    contenido, nombre = exportar_geopackage(gdf_sel, "parcelas_bbox.gpkg")
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)


@callback(
    Output("download-shp-bbox", "data"),
    Input("btn-shp-bbox", "n_clicks"),
    State("store-gdf-bbox", "data"),
    State("store-seleccionadas", "data"),
    prevent_initial_call=True
)
def descargar_shp_bbox(n, gdf_json, seleccionadas):
    if not gdf_json or not seleccionadas:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    
    # Filtrar solo las seleccionadas
    ids = [int(i) for i in seleccionadas]
    gdf_sel = gdf[gdf['id_parcela'].isin(ids)]
    
    contenido, nombre = exportar_shapefile(gdf_sel, "parcelas_bbox")
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)