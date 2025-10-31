"""
SIGPAC Dash App - Responsive Version
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

# Layout responsive
app.layout = dmc.MantineProvider(
    html.Div(
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column"
        },
        children=[
            # Header responsive
            html.Div(
                style={
                    "backgroundColor": "#2d6a4f",
                    "padding": "15px 20px",
                    "color": "white",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                },
                className="header-container",
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "15px",
                            "maxWidth": "1400px",
                            "margin": "0 auto"
                        },
                        className="header-content",
                        children=[
                            # Logo (siempre visible)
                            dcc.Link(
                                href="/home",
                                style={
                                    "textDecoration": "none",
                                    "color": "white",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                },
                                className="logo-link",
                                children=[
                                    html.Span(
                                        DashIconify(icon="mdi:hexagon-multiple-outline", width=40, color="#aeb237"),
                                        style={"marginRight": "8px"}
                                    ),
                                    html.H2(
                                        "SIGPAC Parcelas",
                                        style={
                                            "margin": "0",
                                            "fontWeight": "700",
                                            "fontSize": "clamp(20px, 5vw, 24px)"
                                        }
                                    )
                                ]
                            ),
                            # Navegación (se adapta en móvil)
                            html.Nav(
                                style={
                                    "display": "flex",
                                    "flexWrap": "wrap",
                                    "gap": "8px",
                                    "justifyContent": "center",
                                    "alignItems": "center"
                                },
                                className="nav-container",
                                children=[
                                    dcc.Link(
                                        "Inicio",
                                        href="/home",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "8px 16px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500",
                                            "fontSize": "clamp(13px, 2.5vw, 15px)",
                                            "whiteSpace": "nowrap",
                                            "textAlign": "center"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "Códigos",
                                        href="/",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "8px 16px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500",
                                            "fontSize": "clamp(13px, 2.5vw, 15px)",
                                            "whiteSpace": "nowrap",
                                            "textAlign": "center"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "Mapa",
                                        href="/bbox",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "8px 16px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500",
                                            "fontSize": "clamp(13px, 2.5vw, 15px)",
                                            "whiteSpace": "nowrap",
                                            "textAlign": "center"
                                        },
                                        className="nav-link"
                                    ),
                                    dcc.Link(
                                        "ATOM",
                                        href="/atom",
                                        style={
                                            "color": "white",
                                            "textDecoration": "none",
                                            "padding": "8px 16px",
                                            "borderRadius": "6px",
                                            "transition": "background-color 0.2s",
                                            "fontWeight": "500",
                                            "fontSize": "clamp(13px, 2.5vw, 15px)",
                                            "whiteSpace": "nowrap",
                                            "textAlign": "center"
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
                        pt="xl",
                        className="main-container"
                    )
                ]
            ),
            
            # Footer responsive
            html.Div(
                style={
                    "textAlign": "center",
                    "padding": "clamp(20px, 4vw, 30px) 20px",
                    "borderTop": "1px solid #e0e0e0",
                    "backgroundColor": "#f8f9fa"
                },
                className="footer-container",
                children=[
                    html.Div(
                        style={"marginBottom": "10px"},
                        children=[
                            html.Span(
                                DashIconify(icon="mdi:hexagon-multiple-outline", width=40, color="#aeb237"),
                                style={"marginRight": "8px"}
                            ),
                            html.Span(
                                "SIGPAC Parcelas",
                                style={
                                    "fontSize": "clamp(16px, 3vw, 18px)",
                                    "fontWeight": "600",
                                    "color": "#2d6a4f"
                                }
                            )
                        ]
                    ),
                    html.Div(
                        style={
                            "color": "#666",
                            "fontSize": "clamp(12px, 2.5vw, 14px)",
                            "marginBottom": "8px"
                        },
                        children="Descarga y visualización de datos agrícolas SIGPAC"
                    ),
                    html.Div(
                        style={
                            "color": "#999",
                            "fontSize": "clamp(11px, 2vw, 13px)"
                        },
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


import os

#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 8040))
    #app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    app.run(debug=True, port=8040)