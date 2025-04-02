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

def get_callback_btn_tooltip1():
    @callback(
        Output("tooltip_pretreat", "is_open"),
        [Input('pretable-data-btn', "n_clicks")],
        [State("tooltip_pretreat", "is_open")],
    )
    def toggle_tooltip(n, is_open):
        ctx = dash.callback_context
        if ctx.triggered[0]["prop_id"].split(".")[0] == 'pretable-data-btn':
        # if n:
            return not is_open
        return  is_open
    return

def get_callback_btn_tooltip2():
    @callback(
        Output("tooltip_pretreat2", "is_open"),
        [Input('view-data-btn', "n_clicks")],
        [State("tooltip_pretreat2", "is_open")],
    )
    def toggle_tooltip(n, is_open):
        ctx = dash.callback_context
        if ctx.triggered[0]["prop_id"].split(".")[0] == 'view-data-btn':
        # if n:
            return  not is_open
        return is_open
    return

# def get_callback_print_sucess_msg_pg1():
#     @callback(
#         Output('load_data_check','children'),
#         [Input('dropdown-flag-btn-json','data')],
#     )
#     def sucess_msg_pretreat(data_json_pret):

#         if data_json_pret is None:
#             raise PreventUpdate
#         print('data_json_pret',data_json_pret,json.loads(data_json_pret))
#         if json.loads(data_json_pret) is False:

#         # ctx = dash.callback_context
#         # if ctx.triggered[0]["prop_id"].split(".")[0] == 'pretreatment-data-btn':
#             alert=dbc.Alert(
#             [
#                 html.H4("Pre-tratamento completado!", className="alert-heading"),
#                 html.P(
#                     "O pre-tratamento dos dados fornecidos foi finalizado."
#                     " Agora a visualização dos dados está habilitada, assim"
#                     " como o conteúdo e funcionalidade da aba de predição."
#                 ),
#                 html.Hr(),
#                 html.P(
#                     "Este alerta desaparecerá automáticamente",
#                     className="mb-0",
#                 ),
#                 ]
#             ,duration=8000,style={"backgroundColor": '#78C2AD'})
#             return alert
#         else:
#             raise PreventUpdate
#     return