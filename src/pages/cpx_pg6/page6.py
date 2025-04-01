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
import plotly.express as px

# import dash_daq as daq
import datetime

# example importing backend folder class
# from Backend.source.Class_Case import Case



# Example, calling callbacks from callback folder
from .callbacks_pg6 import callback_dateload_histogram



from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch_pg6", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch_pg6"),
    ]
)


np.random.seed(2020)

layout = html.Div(
    [   
        html.Div(color_mode_switch),
        dcc.Graph(id="histograms-graph6"),
        html.P("Mean:"),
        dcc.Slider(
            id="histograms-mean6", min=-3, max=3, value=0, marks={-3: "-3", 3: "3"}
        ),
        html.P("Standard Deviation:"),
        dcc.Slider(id="histograms-std6", min=1, max=3, value=1, marks={1: "1", 3: "3"}),
    ]
)


callback_dateload_histogram.get_callback_histogram()
callback_dateload_histogram.get_callback_figtemplate()
callback_dateload_histogram.get_callback_logotemplate()

clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
        return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch_pg6", "id"),
    Input("color-mode-switch_pg6", "value"),
)




