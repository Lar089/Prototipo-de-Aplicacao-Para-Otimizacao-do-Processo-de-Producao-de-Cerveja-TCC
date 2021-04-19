import pandas as pd
from datetime import date, datetime, timedelta
from dash.dependencies import Input, Output, State
from pandas.io.json import json_normalize
import dash
from sys import platform
import plotly.figure_factory as ff
import plotly.io as pio
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
# ----------------------------------------------------
# IMPORTS FRONT END
# ----------------------------------------------------
from app import app
from app.layout.layout_main import *
from app.helper import *
from app.beer_list_dao import *
# ----------------------------------------------------
# IMPORTS BACK END
# ----------------------------------------------------
import uuid

# Data
data = read_beer()


# ----------------------------------------------------
# AÇÃO DO BOTÃO ADICIONAR LISTA DE CERVEJAS NA TABELA
# ----------------------------------------------------
cont_add = 0
cont_delete = 0
@app.callback(
    [Output("data-table", "data"),
    Output("data-table", "selected_rows")],
    [Input('button_add', 'n_clicks'),
    Input('button_delete_all', 'n_clicks'),
    Input('button_delete_items', 'n_clicks')],
    [State("list_beer", "value"),
     State("bulk_beer", "value"),
     State("data-table", "selected_rows"),
     State("data-table", "data")
     ])
def update_data(n_clicks_add, n_clicks_delete_all, n_clicks_delete_items, beer, bulk, selected_data, data):   

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        return create(), []
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    print('Contexto de click', ctx.triggered)
    print('Id do elemento clicado: ', button_id)
        
    L = data.copy()

    if button_id == 'button_add':
        if all([beer, bulk]):
            print('add_beer:', beer, bulk)
            print(L)
            if not isin(L, beer):
                L = add(L,beer,bulk)
            # Se a cerveja já não esta presente
            else:
                print('Erro. A cerveja já está presente na lista.')        
            
    elif button_id == 'button_delete_all':
        print('button_delete_all')            
        L = create()        

    elif button_id == 'button_delete_items':        
        print('button_delete_items')            
        print(selected_data)
        L = remove_by_indexes(L, selected_data)
       
    # Retorna o novo dataframe na forma de dicionário,
    # também retorna a lista de linhas selecionadas    
    print(L)
    return L, []
   


# ---------------------------------
# AÇÃO DO BOTÃO ADICIONAR NA MALHA
# ---------------------------------
@app.callback(    
    [
        Output('data-table_results', 'data'),
        Output('gantt', 'figure')
    ],
    [
       Input('button_optimize', 'n_clicks')
    ],
    [
        State('data-table', 'data'),
        State('horizon_time', 'start_date'),
        State('horizon_time', 'end_date'),
        State('gantt', 'figure')
    ])
def update_output(add_info_malha, data_table, start_date, end_date, fig_gantt):

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    print('Contexto de click', ctx.triggered)
    print('Id do elemento clicado: ', button_id)
    
    if not button_id == 'button_optimize':
        raise PreventUpdate

    # ---------------------------------
    # VERIFICA SE O BOTÃO ADICIONAR NA MALHA FOI 
    # ---------------------------------    
    df = pd.DataFrame.from_dict(data_table)     
    df_cervejas = json_normalize(data)

    df_to_optimize = df.merge(df_cervejas, left_on = 'Beer', right_on = 'Nome')[["SIGLA", "tanques", "volume", "Tempo_fermentacao"]]    
    print('To optimize', df_to_optimize)
    
    from dateutil.parser import parse
    start_datetime = parse(start_date)
    end_datetime = parse(end_date)
    diff = end_datetime - start_datetime    
    horizon = round( diff.total_seconds() / (3600 * 24) )    
    print('Horizon', horizon)
    
    dict_to_optimize = df_to_optimize.to_dict("records")

    
    foldername = create_opt_folder()
    save_dict_to_optimize(foldername, dict_to_optimize)
    print(foldername)
    print('Chamando backend')    
    execute_optimization(foldername, horizon)
    df_solution, stats = load_results(foldername)    
    #df_solution, stats = otimizar(dict_to_optimize, horizon)    
    # O data frame df_solution contém o resultado da otimização
    print('Otimização concluída')
    print(df_solution)
    fig = update_gantt(df_solution)
    return df_solution.to_dict("records"), fig


def create_opt_folder (foldername = None):
    import os
    if foldername == None:
        foldername = str(uuid.uuid4())
    if not os.path.exists('temp'):
        os.makedirs('temp')
    if not os.path.exists('temp/'+foldername):
        os.makedirs('temp/'+foldername)
    return foldername

def save_dict_to_optimize( foldername, dict_to_optimize ):
    import pickle
    with open('temp/'+foldername+'/dict_to_optimize.pickle', 'wb') as handle:
        pickle.dump(dict_to_optimize, handle, protocol=pickle.HIGHEST_PROTOCOL)  

def execute_optimization( foldername, horizon ):
    import os
    print('Inicio da execução do script')
    os.system('python app/otimizacao/run.py -data ' + foldername + ' -horizon ' + str(horizon) )
    print('Fim da execução do script')

def load_results( foldername ):
    import pickle
    with open('temp/'+foldername+'/df_solution.pickle', 'rb') as handle:
        df_solution = pickle.load(handle)
    with open('temp/'+foldername+'/stats.pickle', 'rb') as handle:
        stats = pickle.load(handle)
    return df_solution, stats

def update_gantt(df_results):
    df_results.Inicio = df_results.Inicio.astype(int)
    df_results.Fim = df_results.Fim.astype(int)
    df_results.Tarefa = df_results.Tarefa.str.replace("A",'_LOTE_')
    df_results['Lote'] = ("LOTE_" + df_results.Tarefa.str.extract(".*_(?P<Lote>\d)")).values

    df_results.rename(columns = {
        'Tarefa': 'Task1', 
        'Recurso': 'Task',
        'Inicio': 'Start',
        'Fim': 'Finish',
        'Lote' : 'Lote'
    }, inplace=True)

    xlabels = df_results[['Task','Start','Finish']].sort_values(['Start','Finish']).groupby('Task').first().reset_index().sort_values('Start')['Task'].values

    pio.templates.default = "simple_white"

#, index_col='Lote'
    fig = ff.create_gantt(df_results, index_col='Lote', show_hover_fill = True, group_tasks=True, 
    showgrid_x=True, show_colorbar=True)
    fig['layout']['xaxis'].update({'type': None, 'title' : "Tempo (em unidades de tempo de produção, utc)"}) 
    fig['layout']['yaxis'].update({'title' : "Recursos", "categoryorder" : "array", "categoryarray" : xlabels})

    return fig
