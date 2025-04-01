import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
# from numpy import random
from dash_bootstrap_templates import load_figure_template
# import dash_daq as daq
# import datetime
# load_figure_template(["minty"])



# Connect to your app pages
from pages.cpx_pg1 import page1
from pages.cpx_pg2 import page2
from pages.cpx_pg3 import page3
from pages import home, not_found_404
# Connect the navbar to the index
from components import navbar
from components import header,logo_sidebar

nav = navbar

#-----
from app import app_builder
app = app_builder()
# server = app.server

# app = dash.Dash(__name__, use_pages=True, pages_folder="",external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
# app.config.suppress_callback_exceptions = True
dash.register_page("Home", layout=home.layout)
dash.register_page("Page1", layout=page1.layout)
dash.register_page("Page2", layout=page2.layout)
dash.register_page("Page3", layout=page3.layout)
dash.register_page('404_Error', path="/404",layout=not_found_404.layout)
#-----

# Define the index page layout
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     nav, 
#     html.Div(id='page-content', children=[html.H1("Blank page! wait for loading")]), 
# ])



app.layout = html.Div(children=[

    dbc.Row([
            header.header()
            ],align="center"),
    dbc.Row([
    dcc.Store(id='digest-loaddata-pg1',storage_type='session'),
    dcc.Store(id='digest-loaddata-pg2',storage_type='session'),
    dcc.Store(id='temperature_profile_computed_data',storage_type='session'),
    dcc.Location(id='url', refresh=False),
    ]),


    dbc.Row([dbc.Col([dbc.Row(id='row_logosidebar',children=[logo_sidebar.logo_sidebar_dark])],width=2), 
                dbc.Col([dbc.Row()],width=10)],
                align='start', style={"display": "inlineBlock",
                            "marginTop": "1%"
                        }),

    # dbc.Row(dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%","opacity":"1"}),width=2),
    #         align='start', style={"display": "inlineBlock",
    #                         "marginTop": "0%"
    #                     }), 

    dbc.Row([dbc.Col([dbc.Row(children=[nav])],width=2), 
            dbc.Col([dbc.Row([html.Div(id='page-content', children=[])])],width=10)],
            align='start', style={"display": "inlineBlock",
                        "marginTop": "0%"
                    })

    , 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')],
            prevent_initial_call=True
            )
def display_page(pathname):
    if pathname == '/': #/home
        return home.layout
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    if pathname == '/page3':
        return page3.layout
    else: # if redirected to unknown link
        # return "404 Page Error! Please choose a link"
        
        layout404 = dbc.Container(
        fluid=True,
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [   
                            dbc.Row(dbc.Col( html.H1("404 Page Error! Please choose a link"),
                                            width=12),
                                    style={'marginTop':'0%',"marginBottom": "0%"},justify='end'),
                        ], width=12
                    ),

                    ],
                    justify='end',
                    style={"display": "inlineBlock",
                            "marginTop": "5%"
                        }),

                    ]
            )
        
        return layout404


# ...código existente...
server = app.server

if __name__ == "__main__":
    app.run()
    # input("Press enter to proceed...")

# if __name__ == "__main__":
#     app.run_server(debug=True)

