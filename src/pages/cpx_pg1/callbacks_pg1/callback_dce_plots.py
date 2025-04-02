from dash import callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import numpy as np
import pandas as pd
import dash
import plotly.graph_objs as go
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import json
import dash_ag_grid as dag
import dash_mantine_components as dmc
import dash_chart_editor as dce

def chart_editor(df):
    return html.Div(
        [   html.H4("Dash Chart Editor Demo with the user dataset"),
            dce.DashChartEditor(
                id="chart-editor",
                dataSources=df.to_dict("list"),
            ),
            # dmc.Affix(
            #     dmc.Button("Save this chart", id="add-to-layout"),
            #     position={"bottom": 20, "left": 20},
            # ),
        ],
    )

def get_callback_chart_editor():
    @callback(
            Output('dce_view_host','children'),
            
            [Input('view-data-btn', 'n_clicks')],
            [State('storage_database_raw', "data")],
            prevent_initial_call=True

        )
    def update_dropdown(nclicks,df_storage_database_json):
        if True:
            if nclicks is None:
                raise PreventUpdate
            if df_storage_database_json is None:
                raise PreventUpdate
            
            df = pd.read_json(df_storage_database_json, orient='split')
            df['data']=df.index
            df = df.iloc[::10] #df.loc[:,tags_]
            df["data"] = pd.to_datetime(df['data'], infer_datetime_format=True).dt.strftime('%Y-%m-%d %H:%M:%S')

            return chart_editor(df)
    return

# @callback(
#     Output("chartEditor", "dataSources"),
#     Input("dataset", "value"),
# )
# def set_dataset(v):
#     return datasets[v]