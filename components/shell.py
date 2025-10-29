"""
AppShell - Estructura principal de la aplicación
Incluye Header, Navbar, Main y Footer
"""

from dash import html, page_container, callback, Input, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_shell():
    """
    Crea el shell completo de la aplicación con AppShell
    """
    return dmc.MantineProvider(
        theme={
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "green",
        },
        children=[
            dmc.NotificationProvider(
                
                    dmc.AppShell(
                        children=[
                            _create_header(),
                            _create_navbar(),
                            _create_main(),
                        ],
                        header={"height": 60},
                        navbar={
                            "width": 250,
                            "breakpoint": "sm",
                            "collapsed": {"mobile": True}
                        },
                        padding="0",
                        id="app-shell"
                    )
                
            )
        ]
    )


def _create_header():
    """Header con logo y burger menu"""
    return dmc.AppShellHeader(
        children=dmc.Group(
            children=[
                dmc.Burger(
                    id="burger-button",
                    opened=False,
                    hiddenFrom="sm",
                    size="sm"
                ),
                dmc.Group(
                    children=[
                        DashIconify(
                            icon="mdi:sprout",
                            width=30,
                            color="white"
                        ),
                        dmc.Text(
                            "SIGPAC Parcelas",
                            size="xl",
                            fw=700,
                            c="white"
                        )
                    ],
                    gap="xs"
                ),
            ],
            h="100%",
            px="md",
            justify="space-between"
        ),
        style={"backgroundColor": "#2d6a4f"}
    )


def _create_navbar():
    """Navbar lateral (solo móvil)"""
    return dmc.AppShellNavbar(
        children=[
            dmc.Stack(
                children=[
                    dmc.NavLink(
                        label="Códigos SIGPAC",
                        leftSection=DashIconify(icon="mdi:map-marker-multiple"),
                        href="/",
                        active=True
                    ),
                    dmc.NavLink(
                        label="Área en Mapa",
                        leftSection=DashIconify(icon="mdi:draw"),
                        href="/bbox"
                    ),
                    dmc.NavLink(
                        label="Descarga ATOM",
                        leftSection=DashIconify(icon="mdi:download"),
                        href="/atom"
                    ),
                ],
                p="md",
                gap="xs"
            )
        ],
        id="navbar"
    )


def _create_main():
    """Contenido principal con tabs y páginas"""
    return dmc.AppShellMain(
        children=[
            # Tabs de navegación (desktop)
            _create_navigation_tabs(),
            
            # Contenido de las páginas
            dmc.Container(
                children=page_container,
                fluid=True,
                pt="md",
                pb="xl"
            ),
            
            # Footer
            _create_footer()
        ]
    )


def _create_navigation_tabs():
    """Tabs de navegación para desktop"""
    return dmc.Container(
        children=dmc.Tabs(
            children=[
                dmc.TabsList(
                    children=[
                        dmc.TabsTab(
                            "Códigos SIGPAC",
                            value="/",
                            leftSection=DashIconify(icon="mdi:map-marker-multiple")
                        ),
                        dmc.TabsTab(
                            "Área en Mapa",
                            value="/bbox",
                            leftSection=DashIconify(icon="mdi:draw")
                        ),
                        dmc.TabsTab(
                            "Descarga ATOM",
                            value="/atom",
                            leftSection=DashIconify(icon="mdi:download")
                        ),
                    ],
                    grow=False
                )
            ],
            id="navigation-tabs",
            value="/",
            visibleFrom="sm"
        ),
        fluid=True,
        pt="xs",
        pb="xs",
        style={"borderBottom": "1px solid #e9ecef"}
    )


def _create_footer():
    """Footer de la aplicación"""
    return dmc.Container(
        children=dmc.Text(
            "🌾 SIGPAC Parcelas | Descarga y visualización de datos agrícolas",
            size="sm",
            c="dimmed",
            ta="center"
        ),
        fluid=True,
        style={
            "borderTop": "1px solid #e9ecef",
            "paddingTop": "20px",
            "paddingBottom": "20px",
            "marginTop": "40px",
        }
    )


# =============================================================================
# CALLBACKS del Shell
# =============================================================================

@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    prevent_initial_call=True
)
def toggle_navbar(opened):
    """Toggle del burger menu en móvil"""
    return {
        "width": 250,
        "breakpoint": "sm",
        "collapsed": {"mobile": not opened}
    }


@callback(
    Output("navigation-tabs", "value"),
    Input("_pages_location", "pathname"),
    prevent_initial_call=True
)
def sync_tabs_with_url(pathname):
    """Sincroniza tabs con la URL"""
    return pathname if pathname else "/"