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
from datetime import date


from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


# import dash_daq as daq
import datetime
import plotly.express as px


# example importing backend folder class
# from Backend.source.Class_Case import Case



# Example, calling callbacks from callback folder
from .callbacks_pg2 import callback_dateload_barchart

from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch_pg2", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch_pg2"),
    ]
)


df = px.data.tips()
days = df.day.unique()

layout = html.Div(
    [
        html.Div(color_mode_switch),
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in days],
            value=days[0],
            clearable=False,
        ),
        dcc.Graph(id="bar-chart"),
    ]
)



callback_dateload_barchart.get_callback_barchart()
callback_dateload_barchart.get_callback_figtemplate()
callback_dateload_barchart.get_callback_logotemplate()

clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
        return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch_pg2", "id"),
    Input("color-mode-switch_pg2", "value"),
)







