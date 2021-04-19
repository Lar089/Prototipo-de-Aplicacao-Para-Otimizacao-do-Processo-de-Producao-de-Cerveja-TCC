import flask
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__,static_folder='static/')
app = dash.Dash(__name__, server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ---------------------------------
# IMPORTS
# ---------------------------------
from app.layout.layout import layout
app.layout = layout

from app.callbacks import *