"""
Página 1: Descarga por Códigos SIGPAC
Todo en un archivo
"""
import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_mantine_components as dmc
import dash_leaflet as dl
import base64
import geopandas as gpd

from utils.sigpac_api import descargar_por_codigos, calcular_estadisticas
from utils.geo_utils import gdf_to_geojson, calcular_centro_zoom, exportar_geopackage, exportar_shapefile

# Registrar página
dash.register_page(__name__, path="/", name="Códigos SIGPAC")

# =============================================================================
# LAYOUT
# =============================================================================

layout = dmc.Container(
    size="xl",
    children=[
        html.H1("Descarga por Códigos SIGPAC"),
        html.P("Introduce códigos en formato PR:MU:PO:PA:RE (uno por línea)"),
        
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 2fr", "gap": "20px"},
            children=[
                # Columna izquierda: Formulario
                dmc.Paper(
                    p="md",
                    shadow="sm",
                    withBorder=True,
                    children=[
                        dmc.Textarea(
                            id="input-codigos",
                            label="Códigos de parcelas",
                            placeholder="14:010:1:5:2\n14:010:1:5:3",
                            minRows=10,
                            autosize=True,
                            mb="md"
                        ),
                        
                        dmc.Group(
                            mb="md",
                            children=[
                                dmc.Button("Ejemplo", id="btn-ej1", size="xs", variant="light"),
                                dmc.Button("Limpiar", id="btn-limpiar", size="xs", color="red", variant="subtle"),
                            ]
                        ),
                        
                        dmc.Button(
                            "Descargar Parcelas",
                            id="btn-descargar",
                            fullWidth=True,
                            color="green",
                            size="lg",
                            mb="md"
                        ),
                        
                        html.Div(id="status-msg")
                    ]
                ),
                
                # Columna derecha: Resultados
                html.Div([
                    html.Div(id="stats-cards", style={"marginBottom": "20px"}),
                    dmc.Box(
                        pos="relative",
                        style={"minHeight": "500px"},
                        children=[
                            dmc.LoadingOverlay(
                                visible=False,
                                id="loading-overlay",
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
                            html.Div(id="mapa-resultados")
                        ]
                    ),
                    html.Div(
                        id="botones-descarga",
                        style={"marginTop": "20px", "display": "none"},
                        children=dmc.Group([
                            dmc.Button("📦 GeoPackage", id="btn-gpkg", color="green"),
                            dmc.Button("📁 Shapefile", id="btn-shp", color="blue"),
                        ])
                    )
                ])
            ]
        ),
        
        # Stores
        dcc.Store(id="store-gdf"),
        dcc.Store(id="store-loading", data=False),
        dcc.Download(id="download-gpkg"),
        dcc.Download(id="download-shp"),
    ]
)


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output("input-codigos", "value"),
    Output("store-gdf", "data", allow_duplicate=True),
    Input("btn-ej1", "n_clicks"),
    Input("btn-limpiar", "n_clicks"),
    prevent_initial_call=True
)
def ejemplos(ej1, limpiar):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "btn-ej1":
        return "14:900:74:1492:4\n14:900:74:86:4\n14:900:74:86:7\n14:900:74:86:16", no_update
    else:  # btn-limpiar
        return "", None  # Limpia textarea Y store


# Callback para activar loading al presionar el botón
@callback(
    Output("loading-overlay", "visible", allow_duplicate=True),
    Output("store-loading", "data"),
    Input("btn-descargar", "n_clicks"),
    prevent_initial_call=True
)
def activar_loading(n):
    """Muestra el overlay cuando se presiona el botón"""
    return True, True


@callback(
    Output("store-gdf", "data"),
    Output("status-msg", "children"),
    Output("loading-overlay", "visible"),
    Output("store-loading", "data", allow_duplicate=True),
    Input("store-loading", "data"),
    State("input-codigos", "value"),
    prevent_initial_call=True
)
def descargar(loading, codigos_text):
    if not loading:
        return no_update, no_update, no_update, no_update
        
    if not codigos_text:
        return None, dmc.Alert("Introduce códigos", color="yellow"), False, False
    
    lineas = [l.strip() for l in codigos_text.strip().split("\n") if l.strip()]
    if not lineas:
        return None, dmc.Alert("No hay códigos válidos", color="yellow"), False, False
    
    dict_parcelas = {i+1: linea for i, linea in enumerate(lineas)}
    
    try:
        gdf = descargar_por_codigos(dict_parcelas)
        
        if gdf is None or len(gdf) == 0:
            return None, dmc.Alert("No se encontraron parcelas", color="red"), False, False
        
        return gdf.to_json(), dmc.Alert(f"✅ {len(gdf)} parcelas descargadas", color="green"), False, False
    
    except Exception as e:
        return None, dmc.Alert(f"Error: {str(e)}", color="red"), False, False


@callback(
    Output("stats-cards", "children"),
    Output("mapa-resultados", "children"),
    Output("botones-descarga", "style"),
    Input("store-gdf", "data"),
    prevent_initial_call=True
)
def mostrar_resultados(gdf_json):
    if not gdf_json:
        return None, None, {"display": "none"}
    
    gdf = gpd.read_file(gdf_json)
    stats = calcular_estadisticas(gdf)
    
    # Stats cards
    stats_cards = html.Div(
        style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"},
        children=[
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Parcelas", style={"fontSize": "12px", "color": "#666"}),
                html.Div(str(stats['num_parcelas']), style={"fontSize": "24px", "fontWeight": "bold", "color": "green"})
            ]),
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Superficie Total", style={"fontSize": "12px", "color": "#666"}),
                html.Div(f"{stats['superficie_total']:.2f} ha", style={"fontSize": "24px", "fontWeight": "bold", "color": "blue"})
            ]),
            dmc.Paper(p="md", withBorder=True, children=[
                html.Div("Media", style={"fontSize": "12px", "color": "#666"}),
                html.Div(f"{stats['superficie_media']:.2f} ha", style={"fontSize": "24px", "fontWeight": "bold", "color": "orange"})
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
            # Parcelas - sin options, con style directo
            dl.GeoJSON(
                data=geojson,
                id="geojson-parcelas",
                style={
                    "fillColor": "#00ff00",
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
    Output("download-gpkg", "data"),
    Input("btn-gpkg", "n_clicks"),
    State("store-gdf", "data"),
    prevent_initial_call=True
)
def descargar_gpkg(n, gdf_json):
    if not gdf_json:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    contenido, nombre = exportar_geopackage(gdf)
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)


@callback(
    Output("download-shp", "data"),
    Input("btn-shp", "n_clicks"),
    State("store-gdf", "data"),
    prevent_initial_call=True
)
def descargar_shp(n, gdf_json):
    if not gdf_json:
        return no_update
    
    gdf = gpd.read_file(gdf_json)
    contenido, nombre = exportar_shapefile(gdf)
    
    return dict(content=base64.b64encode(contenido).decode(), filename=nombre, base64=True)