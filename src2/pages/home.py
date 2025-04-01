import dash
from dash import callback
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from dash import callback, Input, Output,State, Patch, clientside_callback
from components import logo_sidebar
from dash.exceptions import PreventUpdate

import base64
import os
import json
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

layout = html.Div([
    html.Div(color_mode_switch),
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
])

clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
        return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)


@callback(
    Output('row_logosidebar', "children",allow_duplicate=True),
    Input("color-mode-switch", "value"),
    prevent_initial_call=True
)
def update_logo_template(switch_on):
    if switch_on:
        return logo_sidebar.logo_sidebar_dark
    else:
        return logo_sidebar.logo_sidebar_white
    


