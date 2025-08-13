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

from utils import ensureDatetime as EnDT

import base64
from io import BytesIO
import os

from utils.cache_df import put_df


def _coerce_numeric_col(s: pd.Series) -> pd.Series:
    """Converte série para numérica quando possível, tratando vírgula decimal e milhares."""
    if pd.api.types.is_numeric_dtype(s):
        return s
    try:
        s_str = s.astype(str)
        s_str = s_str.str.replace("\u00A0", "", regex=False)
        s_str = s_str.str.replace(" ", "", regex=False)
        # Heurística simples para vírgula decimal
        if s_str.str.contains(",").mean() > 0.5 and s_str.str.contains(".").mean() > 0.5:
            s_str = s_str.str.replace(".", "", regex=False)
            s_str = s_str.str.replace(",", ".", regex=False)
        else:
            s_str = s_str.str.replace(",", ".", regex=False)
        try:
            return pd.to_numeric(s_str)
        except Exception:
            return s
    except Exception:
        return s


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith(".xlsx"):
        df = pd.read_excel(BytesIO(decoded), index_col=0, header=0, engine='openpyxl')
        flag_load = False
        children = html.Div([ dmc.Alert("Arquivo carregado com sucesso!", title="Success!", color="green") ])

    elif filename.endswith(".csv"):
        bio = BytesIO(decoded)
        # Inferir separador automaticamente
        df = pd.read_csv(bio, index_col=0, header=0, sep=None, engine="python")
        flag_load = False
        children = html.Div([ dmc.Alert("Arquivo carregado com sucesso!", title="Success!", color="green") ])

    elif filename.endswith(".h5"):
        df = pd.read_hdf(os.path.join(os.getcwd(), 'Backend', 'data', filename))
        flag_load = False
        children = html.Div(["Arquivo carregado com sucesso! :D."])

    else:
        flag_load = True
        df = pd.DataFrame()
        children = html.Div(["Tipo de arquivo não suportado."])

    # >>> Aqui o ajuste-chave <<<
    df = EnDT.ensure_datetime(df, time_col=None, set_index=True)

    # Normaliza nomes de colunas (remove espaços/acentos invisíveis)
    df.columns = pd.Index(map(str, df.columns)).str.strip()

    # Conversão de colunas numéricas representadas como string (ex.: vírgula decimal)
    for col in df.columns:
        if col == "data":
            continue
        df[col] = _coerce_numeric_col(df[col])

    return df, children, flag_load




def get_callback_nodal():
    @callback(
        Output("modal", "is_open"),
        Output("output-data-upload", "children", allow_duplicate=True),
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
    # Primeiro dcc Store para armazenar o dataframe raw e gerar os options para os Dropdown menus (Store Callback)
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
            df, children, flag_load = parse_contents(contents, filename)
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
        
        df_key = put_df(df)  # <<< guarda o DF no cache e retorna uma chave
        return df_key, children, False, False, alert
    
    return

