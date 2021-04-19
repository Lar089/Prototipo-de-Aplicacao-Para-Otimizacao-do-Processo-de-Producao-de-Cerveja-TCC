import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# ---------------------------------
# IMPORTS
# ---------------------------------
from app.layout.layout_main import layout as layout_main
from app.layout.layout_result import layout as layout_result


layout = html.Div([
    # ---------------------------------
    # TITULO DA PAGINA
    # ---------------------------------
    dbc.Navbar([
            html.A(
                dbc.Row(                    [
                        dbc.Col(dbc.NavbarBrand("Otimizador do Processo de Produção de Cerveja", className="ml-2")),
                    ],# BrewHouse Optimization
                    align="center",
                    no_gutters=True,
                )
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
        ],
        color="#007BFF",
        dark=True,
    ),
    html.Div(layout_main),
    html.Div(layout_result)

])
