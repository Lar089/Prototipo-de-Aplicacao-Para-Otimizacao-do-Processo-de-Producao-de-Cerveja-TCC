import json
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# ---------------------------------
# LENDO JSON
# ---------------------------------
def read_json():
    with open('./app/data/cervejas.json','r', encoding='utf8') as f:
        return json.load(f)

# ---------------------------------
# LENDO A LISTA DE CERVEJAS
# ---------------------------------
def read_beer():
    data = read_json()
    return data['Cervejas']

# ----------------------------------
# DEFINE A LISTA DE NOMES DE CERVEJA
# ----------------------------------
def define_list_beer():
    data = read_beer()
    list_beer_name = []
    for i in data:
        list_beer_name.append(i['Nome'])
    return list_beer_name

