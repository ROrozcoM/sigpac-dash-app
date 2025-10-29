"""
Página de Inicio - Información sobre la herramienta
"""
import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/home", name="Inicio")

layout = dmc.Container(
    size="lg",
    children=[
        # Hero section
        html.Div(
            style={
                "textAlign": "center",
                "padding": "60px 20px 40px",
                "background": "linear-gradient(135deg, #2d6a4f 0%, #40916c 100%)",
                "borderRadius": "12px",
                "color": "white",
                "marginBottom": "40px"
            },
            children=[
            html.H1(
                [
                    DashIconify(icon="mdi:hexagon-multiple-outline", width=52, color="#aeb237",
                                style={"verticalAlign": "middle", "marginRight": "8px"}),
                    "SIGPAC Parcelas",
                ],
                style={
                    "fontSize": "46px",
                    "fontWeight": "700",
                    "marginBottom": "20px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "gap": "8px",
                },
            ),
                html.P(
                    "Herramienta profesional para descarga y visualización de datos agrícolas del Sistema de Información Geográfica de Parcelas Agrícolas",
                    style={"fontSize": "18px", "maxWidth": "700px", "margin": "0 auto", "lineHeight": "1.6"}
                )
            ]
        ),
        
        # Introducción
        dmc.Paper(
            p="xl",
            shadow="sm",
            withBorder=True,
            mb="xl",
            children=[
                html.H2("¿Qué es esta herramienta?", style={"color": "#2d6a4f", "marginBottom": "20px"}),
                html.P(
                    "SIGPAC Parcelas es una aplicación web que facilita el acceso y descarga de datos geográficos de parcelas agrícolas españolas. "
                    "Utiliza las APIs oficiales del Ministerio de Agricultura, Pesca y Alimentación (MAPA) para proporcionar información actualizada "
                    "sobre recintos SIGPAC en toda España.",
                    style={"fontSize": "16px", "lineHeight": "1.8", "color": "#555"}
                )
            ]
        ),
        
        # Métodos de descarga
        html.H2("Métodos de Descarga", style={"color": "#2d6a4f", "marginBottom": "20px"}),
        
        dmc.SimpleGrid(
            cols={"base": 1, "md": 3},
            spacing="lg",
            mb="xl",
            children=[
                # Método 1
                dmc.Paper(
                    p="lg",
                    shadow="sm",
                    withBorder=True,
                    style={"height": "100%"},
                    children=[
                        html.Div(
                            DashIconify(icon="mdi:map-marker-radius-outline", width=42, color="#2b8a3e"),
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        html.H3("Códigos SIGPAC", style={"textAlign": "center", "color": "#2d6a4f", "marginBottom": "15px"}),
                        html.P(
                            "Descarga parcelas específicas introduciendo sus códigos en formato PR:MU:PO:PA:RE. Ideal para consultas precisas.",
                            style={"fontSize": "14px", "color": "#666", "textAlign": "center"}
                        )
                    ]
                ),
                
                # Método 2
                dmc.Paper(
                    p="lg",
                    shadow="sm",
                    withBorder=True,
                    style={"height": "100%"},
                    children=[
                        html.Div(
                            DashIconify(icon="mdi:vector-square-edit", width=42, color="#f59f00"),
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        html.H3("Área en Mapa", style={"textAlign": "center", "color": "#2d6a4f", "marginBottom": "15px"}),
                        html.P(
                            "Dibuja un rectángulo en el mapa interactivo y descarga todas las parcelas del área. Selecciona individualmente las que necesites.",
                            style={"fontSize": "14px", "color": "#666", "textAlign": "center"}
                        )
                    ]
                ),
                
                # Método 3
                dmc.Paper(
                    p="lg",
                    shadow="sm",
                    withBorder=True,
                    style={"height": "100%"},
                    children=[
                        html.Div(
                            DashIconify(icon="mdi:cloud-download-outline", width=42, color="#1971c2"),
                            style={"textAlign": "center", "marginBottom": "15px"},
                        ),
                        html.H3("Descarga ATOM", style={"textAlign": "center", "color": "#2d6a4f", "marginBottom": "15px"}),
                        html.P(
                            "Acceso directo al servicio ATOM oficial de FEGA. Descarga municipios completos con filtros avanzados.",
                            style={"fontSize": "14px", "color": "#666", "textAlign": "center"}
                        )
                    ]
                ),
            ]
        ),
        
        # Fuentes de datos
        html.H2("🔗 Fuentes de Datos", style={"color": "#2d6a4f", "marginBottom": "20px"}),
        
        dmc.Paper(
            p="xl",
            shadow="sm",
            withBorder=True,
            mb="lg",
            children=[
                html.H3("API SIGPAC - Hub Cloud", style={"color": "#40916c", "marginBottom": "15px"}),
                html.P(
                    "Servicio de consulta de recintos SIGPAC mediante API REST y OGC API Features.",
                    style={"fontSize": "15px", "marginBottom": "10px", "color": "#555"}
                ),
                html.Ul(
                    style={"color": "#666", "lineHeight": "1.8"},
                    children=[
                        html.Li([
                            html.Strong("URL Base: "),
                            html.A(
                                "https://sigpac-hubcloud.es",
                                href="https://sigpac-hubcloud.es",
                                target="_blank",
                                style={"color": "#2d6a4f"}
                            )
                        ]),
                        html.Li([html.Strong("Métodos: "), "Consulta por códigos, bbox, OGC API Features"]),
                        html.Li([html.Strong("Formato: "), "GeoJSON, GPKG, Shapefile"]),
                        html.Li([html.Strong("Cobertura: "), "Toda España"]),
                    ]
                )
            ]
        ),
        
        dmc.Paper(
            p="xl",
            shadow="sm",
            withBorder=True,
            mb="xl",
            children=[
                html.H3("Servicio ATOM FEGA", style={"color": "#40916c", "marginBottom": "15px"}),
                html.P(
                    "Servicio oficial de descarga de cartografía SIGPAC del Fondo Español de Garantía Agraria (FEGA).",
                    style={"fontSize": "15px", "marginBottom": "10px", "color": "#555"}
                ),
                html.Ul(
                    style={"color": "#666", "lineHeight": "1.8"},
                    children=[
                        html.Li([
                            html.Strong("Organismo: "),
                            html.A(
                                "FEGA - Ministerio de Agricultura",
                                href="https://www.fega.gob.es",
                                target="_blank",
                                style={"color": "#2d6a4f"}
                            )
                        ]),
                        html.Li([
                            html.Strong("Servicio ATOM: "),
                            html.A(
                                "fega.gob.es/atom",
                                href="https://www.fega.gob.es/atom",
                                target="_blank",
                                style={"color": "#2d6a4f"}
                            )
                        ]),
                        html.Li([html.Strong("Actualización: "), "Campaña anual (2024)"]),
                        html.Li([html.Strong("Formato: "), "GeoPackage (.gpkg) y Shapefile (.shp)"]),
                        html.Li([html.Strong("Nivel: "), "Municipio completo"]),
                    ]
                )
            ]
        ),
        
        # Características
        html.H2("Características", style={"color": "#2d6a4f", "marginBottom": "20px"}),
        
        dmc.Paper(
            p="xl",
            shadow="sm",
            withBorder=True,
            mb="xl",
            children=[
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                        "gap": "24px",
                        "textAlign": "center",
                        "alignItems": "center",
                    },
                    children=[
                        html.Div([
                            DashIconify(icon="mdi:map-search-outline", width=40, color="#228be6", style={"marginBottom": "10px"}),
                            html.Strong("Visualización interactiva", style={"display": "block", "marginBottom": "5px"}),
                            html.Span("Mapas Leaflet con capas satelitales y temáticas", 
                                    style={"fontSize": "14px", "color": "#666"}),
                        ]),
                        html.Div([
                            DashIconify(icon="mdi:file-table-box-multiple-outline", width=40, color="#40c057", style={"marginBottom": "10px"}),
                            html.Strong("Múltiples formatos", style={"display": "block", "marginBottom": "5px"}),
                            html.Span("Exporta tus datos en GeoPackage, Shapefile o GeoJSON", 
                                    style={"fontSize": "14px", "color": "#666"}),
                        ]),
                        html.Div([
                            DashIconify(icon="mdi:crosshairs-gps", width=40, color="#f59f00", style={"marginBottom": "10px"}),
                            html.Strong("Selección precisa", style={"display": "block", "marginBottom": "5px"}),
                            html.Span("Filtra y selecciona exactamente las parcelas a descargar", 
                                    style={"fontSize": "14px", "color": "#666"}),
                        ]),
                        html.Div([
                            DashIconify(icon="mdi:rocket-launch-outline", width=40, color="#fa5252", style={"marginBottom": "10px"}),
                            html.Strong("Descarga rápida", style={"display": "block", "marginBottom": "5px"}),
                            html.Span("Acceso directo y optimizado a APIs oficiales SIGPAC", 
                                    style={"fontSize": "14px", "color": "#666"}),
                        ]),
                    ],
                )
            ],
        ),
        
        # Call to action
        html.Div(
            style={"textAlign": "center", "padding": "40px 20px"},
            children=[
                html.H2("¿Listo para empezar?", style={"color": "#2d6a4f", "marginBottom": "20px"}),
                html.P(
                    "Selecciona el método de descarga que mejor se adapte a tus necesidades",
                    style={"fontSize": "16px", "color": "#666", "marginBottom": "30px"}
                ),
                dmc.Group(
                    justify="center",
                    gap="md",
                    children=[
                        dmc.Button(
                            "Búsqueda por códigos SIGPAC",
                            size="lg",
                            color="green",
                        ),
                        dmc.Button(
                            "Búsqueda por área en Mapa",
                            size="lg",
                            color="blue",
                        ),
                        dmc.Button(
                            "Filtro y Descarga ATOM",
                            size="lg",
                            color="teal",
                        ),
                    ]
                )
            ]
        )
    ]
)