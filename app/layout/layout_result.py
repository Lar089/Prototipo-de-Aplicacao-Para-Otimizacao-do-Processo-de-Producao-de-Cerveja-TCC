import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_table
import plotly.figure_factory as ff

# ---------------------------------
# IMPORTS
# ---------------------------------


# ---------------------------------
# LAYOUT GERAL
# ---------------------------------
layout = html.Div([
    
    html.Div([
        html.Hr(),
    ],
    style={'width': '90%', 'float': 'right'}),

    html.Div([
        html.H4("Resultado da Otimização"),
    ],
    style={'width': '65%', 'float': 'right'}),
    
    html.Div([
        html.Hr(),
    ],
    style={'width': '90%', 'float': 'right'}),

    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Tebela de Resultados', children=[
                dcc.Loading(id="loading-2",children=[
                html.P(),
                dash_table.DataTable(
                    id="data-table_results",
                    columns=[
                        {"name": "Tarefa", "id": "Task"}, 
                        {"name": "Recurso", "id": "Task1"},
                        {"name": "Inicio", "id": "Start"},
                        {"name": "Fim", "id": "Finish"},
                        ],       
                    data = [{
                    'Tarefa' : '', 
                    'Recurso' : '', 
                    'Inicio' : '',
                    'Fim' : ''
                    }],
                    page_size=10,
                    style_cell={'minWidth': 95, 'maxWidth': 95,
                                'width': 95, 'textAlign': 'center'},
                    style_table={'height': '350px'},
                    style_as_list_view=True,            
                ),
            ])
        ]),
        dcc.Tab(id="data-gantt_results",label='Gráfico de Resultados', children=[
            dcc.Graph(id="gantt")
        ]),
    ])


    ],
    style={'width': '90%', 'float': 'right'}),
        
],
    style={'width': '60%', 'float': 'letf', 'display': 'inline-block'}
)

