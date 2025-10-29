"""
Página 3: Descarga ATOM
Todo en un archivo
"""
import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_mantine_components as dmc
import dash_leaflet as dl
import base64
import geopandas as gpd

from utils.sigpac_atom import descargar_sigpac
from utils.geo_utils import gdf_to_geojson, calcular_centro_zoom, exportar_geopackage, exportar_shapefile
from utils.municipios_data import MUNICIPIOS

# Registrar página
dash.register_page(__name__, path="/atom", name="Descarga ATOM")

# Datos de provincias
PROVINCIAS = [
    {"value": "01", "label": "01 - Araba/Álava"},
    {"value": "02", "label": "02 - Albacete"},
    {"value": "03", "label": "03 - Alacant/Alicante"},
    {"value": "04", "label": "04 - Almería"},
    {"value": "05", "label": "05 - Ávila"},
    {"value": "06", "label": "06 - Badajoz"},
    {"value": "07", "label": "07 - Balears, Illes"},
    {"value": "08", "label": "08 - Barcelona"},
    {"value": "09", "label": "09 - Burgos"},
    {"value": "10", "label": "10 - Cáceres"},
    {"value": "11", "label": "11 - Cádiz"},
    {"value": "12", "label": "12 - Castelló/Castellón"},
    {"value": "13", "label": "13 - Ciudad Real"},
    {"value": "14", "label": "14 - Córdoba"},
    {"value": "15", "label": "15 - Coruña, A"},
    {"value": "16", "label": "16 - Cuenca"},
    {"value": "17", "label": "17 - Girona"},
    {"value": "18", "label": "18 - Granada"},
    {"value": "19", "label": "19 - Guadalajara"},
    {"value": "20", "label": "20 - Gipuzkoa"},
    {"value": "21", "label": "21 - Huelva"},
    {"value": "22", "label": "22 - Huesca"},
    {"value": "23", "label": "23 - Jaén"},
    {"value": "24", "label": "24 - León"},
    {"value": "25", "label": "25 - Lleida"},
    {"value": "26", "label": "26 - Rioja, La"},
    {"value": "27", "label": "27 - Lugo"},
    {"value": "28", "label": "28 - Madrid"},
    {"value": "29", "label": "29 - Málaga"},
    {"value": "30", "label": "30 - Murcia"},
    {"value": "31", "label": "31 - Navarra"},
    {"value": "32", "label": "32 - Ourense"},
    {"value": "33", "label": "33 - Asturias"},
    {"value": "34", "label": "34 - Palencia"},
    {"value": "35", "label": "35 - Palmas, Las"},
    {"value": "36", "label": "36 - Pontevedra"},
    {"value": "37", "label": "37 - Salamanca"},
    {"value": "38", "label": "38 - Santa Cruz de Tenerife"},
    {"value": "39", "label": "39 - Cantabria"},
    {"value": "40", "label": "40 - Segovia"},
    {"value": "41", "label": "41 - Sevilla"},
    {"value": "42", "label": "42 - Soria"},
    {"value": "43", "label": "43 - Tarragona"},
    {"value": "44", "label": "44 - Teruel"},
    {"value": "45", "label": "45 - Toledo"},
    {"value": "46", "label": "46 - València/Valencia"},
    {"value": "47", "label": "47 - Valladolid"},
    {"value": "48", "label": "48 - Bizkaia"},
    {"value": "49", "label": "49 - Zamora"},
    {"value": "50", "label": "50 - Zaragoza"},
]

USOS = [
    {"value": "OV", "label": "OV - Olivar"},
    {"value": "VI", "label": "VI - Viñedo"},
    {"value": "TA", "label": "TA - Tierras arables"},
    {"value": "PA", "label": "PA - Pastos"},
    {"value": "PR", "label": "PR - Prados"},
    {"value": "FY", "label": "FY - Frutales"},
    {"value": "CA", "label": "CA - Cítricos"},
    {"value": "FO", "label": "FO - Forestal"},
]

# =============================================================================
# LAYOUT
# =============================================================================

layout = dmc.Container(
    size="xl",
    children=[
        html.H1("Descarga ATOM Oficial"),
        html.P("Descarga datos oficiales de FEGA por provincia y municipio"),
        
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 2fr", "gap": "20px"},
            children=[
                # Columna izquierda: Formulario
                dmc.Paper(
                    p="md",
                    shadow="sm",
                    withBorder=True,
                    children=[
                        dmc.Select(
                            id="select-provincia",
                            label="Provincia",
                            placeholder="Selecciona provincia",
                            data=PROVINCIAS,
                            searchable=True,
                            mb="md"
                        ),
                        
                        dmc.Select(
                            id="select-municipio",
                            label="Municipio",
                            placeholder="Primero selecciona una provincia",
                            data=[],
                            searchable=True,
                            disabled=True,
                            mb="md"
                        ),
                        
                        dmc.NumberInput(
                            id="input-superficie",
                            label="Superficie máxima (ha)",
                            placeholder="Opcional",
                            min=0,
                            step=0.5,
                            mb="md"
                        ),
                        
                        dmc.NumberInput(
                            id="input-pendiente",
                            label="Pendiente mínima (‰)",
                            placeholder="Opcional",
                            min=0,
                            max=1000,
                            mb="md"
                        ),
                        
                        dmc.MultiSelect(
                            id="select-usos",
                            label="Usos del suelo",
                            placeholder="Todos los usos",
                            data=USOS,
                            mb="md"
                        ),
                        
                        dmc.Button(
                            "Descargar desde ATOM",
                            id="btn-descargar-atom",
                            fullWidth=True,
                            color="green",
                            size="lg",
                            mb="sm"
                        ),
                        
                        dmc.Button(
                            "Limpiar",
                            id="btn-limpiar-atom",
                            fullWidth=True,
                            color="red",
                            variant="subtle",
                            size="sm",
                            mb="md"
                        ),
                        
                        html.Div(id="status-atom")
                    ]
                ),
                
                # Columna derecha: Resultados
                html.Div([
                    html.Div(id="stats-atom", style={"marginBottom": "20px"}),
                    dmc.Box(
                        pos="relative",
                        style={"minHeight": "500px"},
                        children=[
                            dmc.LoadingOverlay(
                                visible=False,
                                id="loading-overlay-atom",
                                zIndex=1000,
                                loaderProps={
                                    "variant": "custom",
                                    "children": dmc.Image(
                                        h=150,
                                        radius="md",
                                        src="/assets/pato.gif",
                                    ),
                                },
                                overlayProps={"radius": "sm", "blur": 2}
                            ),
                            html.Div(id="mapa-atom")
                        ]
                    ),
                    html.Div(
                        id="botones-descarga-atom",
                        style={"marginTop": "20px", "display": "none"},
                        children=dmc.Group([
                            dmc.Button("📦 GeoPackage", id="btn-gpkg-atom", color="green"),
                            dmc.Button("📁 Shapefile", id="btn-shp-atom", color="blue"),
                        ])
                    )
                ])
            ]
        ),
        
        # Stores
        dcc.Store(id="store-gdf-atom"),
        dcc.Store(id="store-loading-atom", data=False),
        dcc.Download(id="download-gpkg-atom"),
        dcc.Download(id="download-shp-atom"),
    ]
)


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output("select-municipio", "data"),
    Output("select-municipio", "disabled"),
    Output("select-municipio", "placeholder"),
    Output("select-municipio", "value"),
    Input("select-provincia", "value"),
    prevent_initial_call=False
)
def actualizar_municipios(provincia):
    """Carga los municipios de la provincia seleccionada"""
    if not provincia:
        return [], True, "Primero selecciona una provincia", None
    
    # Buscar municipios de la provincia
    municipios = MUNICIPIOS.get(provincia, [])
    
    if not municipios:
        return [], True, f"No hay municipios para provincia {provincia}", None
    
    return municipios, False, "Selecciona un municipio", None


@callback(
    Output("select-provincia", "value"),
    Output("select-municipio", "value", allow_duplicate=True),
    Output("input-superficie", "value"),
    Output("input-pendiente", "value"),
    Output("select-usos", "value"),
    Output("store-gdf-atom", "data", allow_duplicate=True),
    Input("btn-limpiar-atom", "n_clicks"),
    prevent_initial_call=True
)
def limpiar_atom(n):
    """Limpia todos los campos y resultados"""
    return None, None, None, None, None, None


# Callback para activar loading al presionar el botón
@callback(
    Output("loading-overlay-atom", "visible", allow_duplicate=True),
    Output("store-loading-atom", "data"),
    Input("btn-descargar-atom", "n_clicks"),
    prevent_initial_call=True
)
def activar_loading_atom(n):
    """Muestra el overlay cuando se presiona el botón"""
    return True, True


@callback(
    Output("store-gdf-atom", "data"),
    Output("status-atom", "children"),
    Output("loading-overlay-atom", "visible"),
    Output("store-loading-atom", "data", allow_duplicate=True),
    Input("store-loading-atom", "data"),
    State("select-provincia", "value"),
    State("select-municipio", "value"),
    State("input-superficie", "value"),
    State("input-pendiente", "value"),
    State("select-usos", "value"),
    prevent_initial_call=True
)
def descargar_atom(loading, provincia, municipio, superficie, pendiente, usos):
    if not loading:
        return no_update, no_update, no_update, no_update
    
    if not provincia or not municipio:
        return None, dmc.Alert("Selecciona provincia y municipio", color="yellow"), False, False
    
    try:
        gdf = descargar_sigpac(
            provincia=int(provincia),
            municipio=municipio,
            superficie_max_ha=superficie if superficie else None,
            pendiente_min_mil=pendiente if pendiente else None,
            uso_sigpac=usos if usos else None
        )
        
        if gdf is None or len(gdf) == 0:
            return None, dmc.Alert("No se encontraron datos. Verifica provincia/municipio", color="red"), False, False
        
        return gdf.to_json(), dmc.Alert(f"✅ {len(gdf)} parcelas descargadas desde ATOM", color="green"), False, False
    
    except Exception as e:
        return None, dmc.Alert(f"Error: {str(e)}", color="red"), False, False


@callback(
    Output("stats-atom", "children"),
    Output("mapa-atom", "children"),
    Output("botones-descarga-atom", "style"),
    Input("store-gdf-atom", "data"),
    prevent_initial_call=True
)
def mostrar_resultados_atom(gdf_json):
    if not gdf_json:
        return None, None, {"display": "none"}
    
    gdf = gpd.read_file(gdf_json)
    
    # Calcular estadísticas
    num_parcelas = len(gdf)
    
    # Superficie
    if 'superficie_ha' in gdf.columns:
        sup_total = gdf['superficie_ha'].sum()
        sup_media = gdf['superficie_ha'].mean()
    else:
        sup_total = 0
        sup_media = 0
    
    # Stats cards
    stats_cards = html.Div(
        style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"},
        children=[
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Recintos", style={"fontSize": "12px", "color": "#666"}),
                html.Div(str(num_parcelas), style={"fontSize": "24px", "fontWeight": "bold", "color": "green"})
            ]),
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Superficie Total", style={"fontSize": "12px", "color": "#666"}),
                html.Div(f"{sup_total:.2f} ha", style={"fontSize": "24px", "fontWeight": "bold", "color": "blue"})
            ]),
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Media", style={"fontSize": "12px", "color": "#666"}),
                html.Div(f"{sup_media:.2f} ha", style={"fontSize": "24px", "fontWeight": "bold", "color": "orange"})
            ]),
        ]
    )
    
    # Mapa
    centro, zoom = calcular_centro_zoom(gdf)
    geojson = gdf_to_geojson(gdf)
    
    mapa = dl.Map(
        center=centro,
        zoom=zoom,
        style={"width": "100%", "height": "500px"},
        children=[
            # Capa base satelital
            dl.TileLayer(
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attribution="Esri"
            ),
            # Etiquetas
            dl.TileLayer(
                url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
                attribution="Esri"
            ),
            # Parcelas
            dl.GeoJSON(
                data=geojson,
                id="geojson-atom",
                style={
                    "fillColor": "#ff6b35",
                    "color": "#ffffff", 
                    "weight": 2,
                    "fillOpacity": 0.5
                },
                hoverStyle={
                    "fillColor": "#ffff00",
                    "fillOpacity": 0.7,
                    "weight": 3
                }
            )
        ]
    )
    
    return stats_cards, mapa, {"marginTop": "20px", "display": "block"}


@callback(
    Output("download-gpkg-atom", "data"),
    Input("btn-gpkg-atom", "n_clicks"),
    State("store-gdf-atom", "data"),
    prevent_initial_call=True
)
def descargar_gpkg_atom(n, gdf_json):
    if not gdf_json:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    contenido, nombre = exportar_geopackage(gdf, "parcelas_atom.gpkg")
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)


@callback(
    Output("download-shp-atom", "data"),
    Input("btn-shp-atom", "n_clicks"),
    State("store-gdf-atom", "data"),
    prevent_initial_call=True
)
def descargar_shp_atom(n, gdf_json):
    if not gdf_json:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    contenido, nombre = exportar_shapefile(gdf, "parcelas_atom")
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)