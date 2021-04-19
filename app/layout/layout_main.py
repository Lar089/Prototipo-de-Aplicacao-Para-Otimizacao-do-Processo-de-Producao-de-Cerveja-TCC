import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from datetime import date, datetime, timedelta


# ---------------------------------
# IMPORTS
# ---------------------------------
from app.helper import define_list_beer
from app.callbacks import create, create_sample
# ---------------------------------
# LAYOUT GERAL
# ---------------------------------
layout = html.Div([
    html.Div([
        html.P(),
        # ---------------------------------
        # ENTRADA DO HORIZON/TEMPO
        # ---------------------------------
        dbc.Label("Selecione o Tempo", html_for="selecione-tempo"),
        html.Div([
            dcc.DatePickerRange(
                id='horizon_time',
                month_format='DD/MM/YYYY',
                end_date=date.today() + timedelta(days=20),
                start_date=date.today(),
            ),
        ]),
        html.Div(id='id_calendar'),

        dbc.Row([
            # ---------------------------------
            # BOTÃO COM A LISTA DE CERVEJAS
            # ---------------------------------
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label("Lista de Cervejas",
                        html_for="lista-de-cervejas"),
                    html.Div([
                        dcc.Dropdown(id='list_beer',options=[{'label': i, 'value': i}
                            for i in define_list_beer()],),
                    ]),
                ]),width=6,
            ),
            # ---------------------------------
            # ENTRADA DO VOLUME
            # ---------------------------------
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label(
                        "Volume", html_for="bulk"),
                    dbc.Input(
                        type="number",
                        id="bulk_beer",
                        placeholder="Select...",
                        min=1,
                    ),
            ]), width=6,),
            ],
            form=True,
        ),

        html.Div([
            # ------------------------------------
            # BOTÃO ADICIONAR NA LISTA DE CERVEJA
            # ------------------------------------
            html.Div([
                dbc.Button(id='button_add', color="primary",
                           n_clicks=0, children='Adicionar'),
                html.Div(id='output-state')
            ]),
            html.Div(id='id-div')
        ]),
        html.P(),

        # ---------------------------------
        # LABEL BEER LIST
        # ---------------------------------
        html.Div([
            dbc.Label("Lista de Cervejas", html_for="lista-de-cervejas")
        ], style={'width': '62%', 'float': 'right'}),

        # ---------------------------------
        # TABELA COM A LISTA DE CERVEJAS
        # ---------------------------------
        html.Div(
            dash_table.DataTable(
                id="data-table",
                columns=[{"name": "Cerveja", "id": "Beer"}] + [
                    {"name": "Volume", "id": "volume"}],
                data=[],
                page_size=6,
                style_cell={'minWidth': 95, 'maxWidth': 95,
                            'width': 95, 'textAlign': 'center'},
                style_table={'height': '250px'},
                style_as_list_view=True,
                row_selectable='multi',                
            ),
            style={'width': '97%', 'float': 'right'},
        ),

        html.P(),
        html.Div([
            # ---------------------------------
            # BOTÃO LIMPAR LISTA
            # ---------------------------------
            html.Div([
                dbc.Button(id='button_delete_all',
                           n_clicks=0, children='Limpar Lista', color="primary"),
                dbc.Button(id='button_delete_items',
                           n_clicks=0, children='Remover Itens', color="primary"),                                           
                html.Div(id='output-delete_all')
            ], style={'width': '70%', 'float': 'left', 'display': 'inline-block'}),
            html.Div(id='id_delete_all'),

            # ---------------------------------
            # BOTÃO GERAR MALHA
            # ---------------------------------
            html.Div([
                dbc.Button(id='button_optimize', color="primary",
                           n_clicks=0, children='Otimizar'),
                html.Div(id='output-optimize')
            ], style={'width': '15%', 'float': 'right', 'display': 'inline-block2'}),
            html.Div(id='id_optimize'),
        ]),
        html.P(),

    ],
        style={'width': '92%', 'float': 'right'}),
],
    style={'width': '36%', 'float': 'left', 'display': 'inline-block'}
)

# color:"#DBD2B2"
