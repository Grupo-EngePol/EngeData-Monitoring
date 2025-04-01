import dash
from dash import callback,clientside_callback
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
# load_figure_template(["slate"])
import numpy as np
import pandas as pd
import json
from numpy import random

import dash_mantine_components as dmc
from dash_iconify import DashIconify


from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

# import dash_daq as daq
# import datetime


# example importing backend folder class
#  from Backend.source.Class_Case import Case
# import joblib
# from sklearn.preprocessing import MinMaxScaler
# import copy

# Example, calling callbacks from callback folder
from .callbacks_pg1 import callback_dateload_heatmap

from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])
# load_figure_template(["LUX"])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch_pg1", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch_pg1"),
    ]
)


df = px.data.medals_wide(indexed=True)

layout = html.Div(
    [
        html.Div(color_mode_switch),
        html.P("Medals included:"),
        dcc.Checklist(
            id="heatmaps-medals",
            options=[{"label": x, "value": x} for x in df.columns],
            value=df.columns.tolist(),
        ),
        dcc.Graph(id="heatmaps-graph"),
    ]
)


callback_dateload_heatmap.get_callback_heatmap()
callback_dateload_heatmap.get_callback_figtemplate()
callback_dateload_heatmap.get_callback_logotemplate()

clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
        return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch_pg1", "id"),
    Input("color-mode-switch_pg1", "value"),
)








