import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import pathlib

import dash
from dash.dependencies import Input, Output
import numpy as np

import socket
import glob

host = socket.gethostbyname(socket.getfqdn())
files = glob.glob(r'G:\공유 드라이브\handa_daily\market_anomalies\performance\anomalies\*.csv')

file_names = list(map(lambda x : x.split('\\')[-1].split('.')[0], files))
F = []

for i in range(len(files)):
    F.append({'label': file_names[i], 'value': files[i]})

A = pd.DataFrame()
for i in range(len(files)):
    a = pd.read_csv(files[i], header = None)
    a.columns = ('date', files[i].split('\\')[-1].split('.')[0])
    a = a.set_index('date')
    A = pd.concat([A,a],axis=1, sort=True)

df = a
years = list(set(pd.Series(pd.to_datetime(df.index)).dt.year))

available_indicators = list(df.columns)



def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div([
                dcc.Dropdown(
                    id='my-dropdown',
                    options=F,
                    value=list(F[0].values())[1]),
                html.Div(id='output-container'),

                dcc.Graph(id='graph-with-slider'),
                dcc.Slider(
                    id='year-slider',
                    min=min(years),
                    max=max(years),
                    value=min(years),
                    marks={str(year): str(year) for year in years},
                    step=None
                )
            ])
        ],
        className="page",
    )


def callback1(app):
    @app.callback(
        dash.dependencies.Output('output-container', 'figure'),
        [dash.dependencies.Input('my-dropdown', 'value')])
    def update_output(value):
        a = pd.read_csv(value, header=None)
        a.columns = ('date', value[i].split('\\')[-1].split(',')[0])
        a = a.set_index('date')

        return update_figure()

def callback2(app):
    @app.callback(
        Output('graph-with-slider', 'figure'),
        [Input('year-slider', 'value'),
         Input('my-dropdown', 'value')])
    def update_figure(selected_year, selected):

        dff = A[selected.split('\\')[-1].split('.')[0]]
        filtered_df = dff.loc[str(selected_year):]
        traces = []

        df_by_continent = filtered_df
        traces.append(go.Scatter(
            x=df_by_continent.index,
            y=np.cumprod(1 + df_by_continent) - 1,
            text=i,
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

        return {
            'data': traces,
            'layout': {
                'height': 500,
                'margin': {'l': 40, 'b': 40, 'r': 10, 't': 10},
                'annotations': [{
                    'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                    'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                    'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                    'text': 'hi'
                }],
            }
        }
