from dash import callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.express as px
from components import logo_sidebar


import plotly.io as pio
from dash import Patch

df = px.data.medals_wide(indexed=True)

def get_callback_heatmap():
    @callback(
            Output("heatmaps-graph", "figure"), 
            Input("heatmaps-medals", "value"),
            )
    def filter_heatmap(cols):
        fig = px.imshow(df[cols])
        return fig
    return

def get_callback_figtemplate():
    @callback(
        Output("heatmaps-graph", "figure",allow_duplicate=True),
        Input("color-mode-switch_pg1", "value"),
        prevent_initial_call=True
    )
    def update_figure_template(switch_on):
        # When using Patch() to update the figure template, you must use the figure template dict
        # from plotly.io  and not just the template name
        print(switch_on,'switch_on')
        template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]

        patched_figure = Patch()
        patched_figure["layout"]["template"] = template
        return patched_figure
    return

def get_callback_logotemplate():
    @callback(
        Output('row_logosidebar', "children",allow_duplicate=True),
        Input("color-mode-switch_pg1", "value"),
        prevent_initial_call=True
    )
    def update_logo_template(switch_on):
        if switch_on:
            return logo_sidebar.logo_sidebar_dark
        else:
            return logo_sidebar.logo_sidebar_white
    return

