import dash
from dash import callback,clientside_callback
from dash import dcc
from dash import html
from dash import dash_table

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
# load_figure_template(["slate"])
import numpy as np
import pandas as pd
import json
from numpy import random

import dash_mantine_components as dmc
import dash_chart_editor as dce
from dash_iconify import DashIconify


from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import base64
import datetime
import io

# import dash_daq as daq
# import datetime


# example importing backend folder class
#  from Backend.source.Class_Case import Case
# import joblib
# from sklearn.preprocessing import MinMaxScaler
# import copy

# Example, calling callbacks from callback folder
from .callbacks_pg1 import callback_dateload_heatmap
from .callbacks_pg1 import callback_loaddatabase
from .callbacks_pg1 import callback_aggrid_table
from .callbacks_pg1 import callback_dce_plots
from .callbacks_pg1 import callback_tooltips_notifications

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


setup_comparison_box = dbc.Card(className='bg-dark',
        children=[
        
            dbc.CardHeader(#className='bg-primary',
                children=["Carregamento e pre-processamento de dados"],
                style={
                    "text-align": "center",
                    "color": "white",
                    "backgroundColor": '#78C2AD',
                    "border-radius": "1px",
                    "border-width": "5px",
                    "border-top": "1px solid rgb(216, 216, 216)",
                },
            ),

            dbc.CardBody([

                dbc.Row([
                    dbc.Col([
                    html.Div([
                        # dbc.Button('Carregar',id = 'open'),
                        # dmc.Button("Carregar dados",id='open',
                        #             leftIcon=DashIconify(icon='fa-solid:file-upload'), size="md",
                        #             color='#23a847',variant="gradient", gradient={"from": "teal", "to": "lime", "deg": 105}),
                        
                        dmc.Button(
                                "Carregar dados",
                                id='open',
                                n_clicks=0,
                                leftIcon=DashIconify(icon='vscode-icons:file-type-excel',width=30), size="sm",
                            variant="gradient", 
                            gradient={"from": "orange", "to": "red"}),


                        dbc.Modal([
                            dbc.ModalHeader("Carregar Arquivo Excel"),
                            dbc.ModalBody([
                                dcc.Upload(
                                    id="upload-data",
                                    children=html.Div([
                                        "Arraste e solte ou ",
                                        html.A("selecione um arquivo Excel")
                                    ]),
                                    multiple=False,
                                ),
                                dcc.Loading(id='loading-load-msg',
                                                # type='circle',
                                                type='cube',
                                                color='#78C2AD',
                                                children=
                                html.Div(id="output-data-upload")),
                            ]),
                            dbc.ModalFooter([
                                dbc.Button("Fechar", id="close", 
                                        # className="btn btn-primary",
                                        className="btn",
                                        style={"backgroundColor": '#78C2AD',
                                            "border": "1px solid rgb(216, 216, 216)",
                                            "border-radius": "1px"})
                            ]),
                        ],
                        id="modal",
                        size="lg"
                        ),
                        # dcc.Store stores the intermediate value
                        # dcc.Store(id='intermediate-data-value'),
                        # dcc.Store stores the segregated value
                        dcc.Store(id='segregated-data-value')]
                    ),
                        ],width=4),

                    
                    dbc.Col([
                    html.Div([
                        # html.Button("Pre-tratar dados",id = 'pretreatment-data-btn'),

                        dmc.Button("Preview em tabela",id='pretable-data-btn',
                                   disabled=True,
                                    leftIcon=DashIconify(icon='fluent:table-sparkle-20-filled',width=30), size="sm",
                                    variant="gradient", gradient={"from": "orange", "to": "red"}),
                        dbc.Tooltip(
                                children= html.Div([dbc.Alert("A seguir os dados são resumidos em uma tabela dinâmica, em que alguns filtros podem ser aplicados,"
                                "A aplicação desses filtros não será efetiva na base de dados", color='#F2989C')], style={"backgroundColor": '#F2989C'}),
                                id="tooltip_pretreat",
                                is_open=False,
                                target="pretable-data-btn",
                                placement='right',
                                trigger=None,
                            ),]
                    ),
                        ],width=4),

                    dbc.Col([
                    html.Div([
                        # html.Button("Pre-tratar dados",id = 'pretreatment-data-btn'),

                        dmc.Button("Visualização",id='view-data-btn',
                                   disabled=True,
                                    leftIcon=DashIconify(icon='cib:mathworks',width=30), size="sm",
                                    variant="gradient", gradient={"from": "orange", "to": "red"}),
                        
                        dbc.Tooltip(
                                children= html.Div([dbc.Alert("A seguir os dados serão exportados para um componente de visualização e plotagem personalizada,"
                                "O correto funcionamento deste componente, depende do tamanho dos dados", color='#F2989C')], style={"backgroundColor": '#F2989C'}),
                                id="tooltip_pretreat2",
                                is_open=False,
                                target='view-data-btn',
                                placement='right',
                                trigger=None,
                            )]
                    ),
                        ],width=4)


                    ],
                    align='center',
                    justify = "evenly"
                    ),

                dbc.Row([html.Br()]),

                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dmc.Text("Carregamento de dados e visualização de tabela-resumo",color='dimmed'),
                            ])
                    ], width=12)
                    ]),

                dbc.Row([html.Br()]),


                
            ],style={"backgroundColor":'#343A40'})
        ],
    )

layout = dbc.Container(
        fluid=True,
        children=[
            html.Div(color_mode_switch),
            dbc.Row(
                [
                    dbc.Col(
                        [  setup_comparison_box 
                        ], width=6
                    ),

                    dbc.Col([dbc.Row(
                        
                        # dcc.Loading(id='loading-data-pretreated-pg1',
                        #                         type='cube',
                        #                         color='#78C2AD',
                        #                         children=html.Div(children='',id='load_data_check'))

                        html.Div(children='',id='load_data_check')                        
                                                        ,align='center',
                                                style={"marginTop": "20%"}
                                                
                                                )
                                                ])


                    ],
                    style={
                            "marginTop": "3%"
                        }),

            dbc.Row(dcc.Loading(id='loading-table-pretreated-pg1',
                                                type='cube',
                                                color='#78C2AD',
                                                children=html.Div(children=[],id='grid_table')), style={
                            "marginTop": "3%"
                        }),

            dbc.Row(
                children=[
                dcc.Loading(id='loading-table-pretreated-pg1',
                                                type='cube',
                                                color='#78C2AD',
                                                children=html.Div(id='dce_view_host',children=[]))
                
                
                    # html.Div(
                    #     [   html.H4("Dash Chart Editor Demo with the Plotly Solar dataset"),
                    #         dce.DashChartEditor(
                    #             id="chart-editor",
                    #             dataSources=df.to_dict("list"),
                    #         ),
                    #         # dmc.Affix(
                    #         #     dmc.Button("Save this chart", id="add-to-layout"),
                    #         #     position={"bottom": 20, "left": 20},
                    #         # ),
                    #     ],
                    # ),

                ],style={"marginTop": "3%"})

            ]
    )





# callback_dateload_heatmap.get_callback_heatmap()
# callback_dateload_heatmap.get_callback_figtemplate()
# callback_dateload_heatmap.get_callback_logotemplate()

callback_loaddatabase.get_callback_nodal()
callback_loaddatabase.get_callback_content()
callback_aggrid_table.get_callback_update_grid()
callback_dce_plots.get_callback_chart_editor()
# callback_tooltips_notifications.get_callback_btn_tooltip1()
# callback_tooltips_notifications.get_callback_btn_tooltip2()

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








