import pandas as pd
from datetime import datetime as dt
from dash.dependencies import Input, Output, State

# ----------------------------------------------------
# IMPOSTS FRONT END
# ----------------------------------------------------
from app import app
from app.layout.layout_result import *

@app.callback(
    [
        Output("progress", "value"), 
        Output("progress", "children")
    ],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    progress = min(n % 110, 100)
    return progress, f"{progress} %" if progress >= 5 else ""
