import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

import pandas as pd


def gantt_fig(df):
    data = []

    for row in df.itertuples():
        data.append(dict(Task=str(row.Phase), Start=str(row.StartDate),
                         Finish=str(row.EndDate), Resource=str(row.ObjectID)))

    colors = ['rgb(0, 102, 204)', 'rgb(204, 0, 0)', 'rgb(0, 153, 0)']

    fig = ff.create_gantt(data, index_col='Resource',
                          reverse_colors=True, show_colorbar=True,
                          showgrid_x=True, title='Gantt Chart')
    fig['layout'].update( margin=dict(l=310))

    return fig


df = pd.DataFrame({'ObjectID': ['ITDM-1', 'ITDM-1', 'ITDM-1', 'ITDM-1',
                                'ITDM-10', 'ITDM-10', 'ITDM-10',
                                'ITDM-101', 'ITDM-101', 'ITDM-101'],
                   'Phase': ['phasezero', 'phaseone', 'phasetwo', 'phasethree',
                             'phasezero', 'phaseone', 'phasetwo', 'phasezero',
                             'phaseone', 'phasetwo'],
                   'StartDate': ['2016-12-1', '2017-3-22', '2017-8-21', '2017-9-21',
                                 '2016-12-1', '2016-12-5', '2016-12-9', '2017-5-11',
                                 '2017-5-12', '2017-8-17'],
                   'EndDate': ['2017-5-22', '2017-8-21', '2017-9-21',  '2017-12-22',
                               '2017-2-5', '2017-4-9',  '2016-12-13', '2017-5-12',
                               '2017-8-17',  '2017-10-5']})

options = df['ObjectID'].unique()


app = dash.Dash()

app.layout = html.Div([html.H1('Gantt table'),
                       dcc.Dropdown(id='my-dropdown',
                                    options=[{'label': n, 'value': n}
                                             for n in options],
                                    value=options[0]),
                       dcc.Graph(id='display-selected-value')
                      ]
                     )



@app.callback(
    dash.dependencies.Output('display-selected-value', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_gantt(value):
    df2plot = df[df['ObjectID']==value].reset_index(drop=True)
    fig = gantt_fig(df2plot)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)