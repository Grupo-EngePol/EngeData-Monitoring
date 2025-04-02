# from app import app  # Importe o objeto app do arquivo app.py
# from index import app  # Importe o objeto app do arquivo app.py
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
import dash_mantine_components as dmc

import base64
from io import BytesIO
import os


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith(".xlsx"):
        df = pd.read_excel(BytesIO(decoded),index_col=0, header=[0], engine='openpyxl')
        flag_load=False

        return df, html.Div([
            dmc.Alert("Arquivo carregado com sucesso!", title="Success!", color="green"),
            ]), flag_load
    elif filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(decoded),index_col=0, header=[0],sep=';')
        flag_load=False

        return df, html.Div([
            dmc.Alert("Arquivo carregado com sucesso!", title="Success!", color="green"),
            ]), flag_load
    elif filename.endswith('h5'):
        df = pd.read_hdf(os.path.join(os.getcwd(),'Backend','data',filename))
        flag_load=False
        return df, html.Div([
            "Arquivo carregado com sucesso! :D."
        ]),flag_load
    
    else:
        flag_load=True
        return pd.DataFrame(), html.Div([
            "Tipo de arquivo não suportado."
        ]),flag_load


def get_callback_nodal():
    @callback(
        Output("modal", "is_open"),
        Output("output-data-upload", "children",allow_duplicate=True),
        Input("open", "n_clicks"),
        Input("close", "n_clicks"),
        State("modal", "is_open"),
        State("upload-data", "contents"),
        State("upload-data", "filename"),
        prevent_initial_call=True
    )

    def toggle_modal(n1, n2,is_open, contents, filename):
        # ctx = dash.callback_context
        # if ctx.triggered[0]["prop_id"].split(".")[0] == 'pretreatment-data-btn':
        #     raise PreventUpdate

        if n1 or n2:
            return not is_open, None
        return is_open, None
    return

def get_callback_content():
    # Primeiro dcc Store para almazenar o dataframe raw e gerar os options para os Dropdown menus (Store Callback)
    @callback([ Output('storage_database_raw', 'data'),
                Output("output-data-upload", "children"),
                Output('pretable-data-btn','disabled'),
                Output('view-data-btn','disabled'),
                Output('load_data_check','children')], 
                [Input("upload-data", "contents")], 
                State("upload-data", "filename"),
                    prevent_initial_call=True)
    def update_output(contents, filename):

        df = pd.DataFrame()
        if contents == None or filename==None:
            raise PreventUpdate
        else:
            df, children,flag_load = parse_contents(contents, filename)
            # some expensive data processing step by ex:
            # cleaned_df = slow_processing_step(value)
            alert=dbc.Alert(
            [
                html.H4("Carregamento de dados completado!", className="alert-heading"),
                html.P(
                    "O carregamento dos dados no arquivo fornecido foi finalizado."
                    " Agora a visualização dos dados está habilitada, assim"
                    " como o conteúdo e funcionalidade de Preview em tabela."
                ),
                html.Hr(),
                html.P(
                    "Este alerta desaparecerá automáticamente",
                    className="mb-0",
                ),
                ]
            ,duration=8000,style={"backgroundColor": '#78C2AD'})

        return df.to_json(date_format='iso', orient='split'),children,False,False,alert
    return

