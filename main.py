"""
SIGPAC Dash App
"""
import dash
from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="SIGPAC Parcelas"
)

# Layout simple
app.layout = dmc.MantineProvider(
    html.Div(
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column"
        },
        children=[
            # Header mejorado
            html.Div(
                style={
                    "backgroundColor": "#2d6a4f",
                    "padding": "20px 40px",
                    "color": "white",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                },
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "space-between",
                            "maxWidth": "1400px",
                            "margin": "0 auto"
                        },
                        children=[
                            # Logo clickeable
                            dcc.Link(
                                href="/home",
                                style={"textDecoration": "none", "color": "white", "display": "flex", "alignItems": "center"},
                                children=[
                                    html.Span(DashIconify(icon="mdi:hexagon-multiple-outline", width=52, color="#aeb237",
                                                        style={"verticalAlign": "middle", "marginRight": "8px"}), style={"fontSize": "24px"}),
                                    html.H2("SIGPAC Parcelas", style={"margin": "0", "fontWeight": "700", "fontSize": "24px"})
                                ]
                            ),
                            # Navegación
                            html.Nav(
                                style={"display": "flex", "gap": "8px", "alignItems": "center"},
                                children=[
                                    dcc.Link(
                                        "Inicio",
                                        href="/home",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "10px 20px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "Descarga por códigos",
                                        href="/",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "10px 20px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "Descargar por área en mapa",
                                        href="/bbox",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "10px 20px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "Descarga y filtro ATOM",
                                        href="/atom",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "10px 20px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500"
                                        },
                                        className="nav-link"
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            ),
            
            # Contenido de páginas (crece para ocupar espacio)
            html.Div(
                style={"flex": "1"},
                children=[
                    dmc.Container(
                        dash.page_container,
                        size="xl",
                        px="md",
                        pt="xl"
                    )
                ]
            ),
            
            # Footer profesional (siempre abajo)
            html.Div(
                style={
                    "textAlign": "center",
                    "padding": "30px 20px",
                    "borderTop": "1px solid #e0e0e0",
                    "backgroundColor": "#f8f9fa"
                },
                children=[
                    html.Div(
                        style={"marginBottom": "10px"},
                        children=[
                            html.Span(DashIconify(icon="mdi:hexagon-multiple-outline", width=52, color="#aeb237",
                                                        style={"verticalAlign": "middle", "marginRight": "8px"}), style={"fontSize": "24px"}),
                            html.Span(
                                "SIGPAC Parcelas",
                                style={"fontSize": "18px", "fontWeight": "600", "color": "#2d6a4f"}
                            )
                        ]
                    ),
                    html.Div(
                        style={"color": "#666", "fontSize": "14px", "marginBottom": "8px"},
                        children="Descarga y visualización de datos agrícolas SIGPAC"
                    ),
                    html.Div(
                        style={"color": "#999", "fontSize": "13px"},
                        children=[
                            "Desarrollado por ",
                            html.Span(
                                "Rafael Orozco",
                                style={"fontWeight": "600", "color": "#2d6a4f"}
                            ),
                            " • 2025"
                        ]
                    )
                ]
            )
        ]
    )
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8050)