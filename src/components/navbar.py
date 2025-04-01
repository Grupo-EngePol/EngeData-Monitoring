# package imports
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# local imports
from dash.exceptions import PreventUpdate
import json
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc


def create_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="black",weight=700),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


navbar = html.Div([




    dbc.Nav(
    vertical = 'md',
    pills = True,
    fill = True,
    horizontal='start',
    navbar_scroll = False,
    # justified=True,
    children=[
    html.H4("Menu",className='text-bold-black'),
    html.Hr(),
    html.Div(
            children=[
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="radix-icons:rocket",
                            label="Home",
                            href="/",
                        ),
                    ],
                ),
                dmc.Divider(
                    label="Data characterization", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="hugeicons:chart-line-data-02", label="Data Visualization", href="/page1"
                        ),
                        create_nav_link(
                            icon="fluent-mdl2:bar-chart-vertical-filter-solid", label="Data Filtering", href="/page2"
                        )
                    ],
                ),
                dmc.Divider(
                    label="Process modeling", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="hugeicons:market-analysis", label='Data Rectification', href='/page3'
                        ),
                        create_nav_link(
                            icon="eos-icons:neural-network", label='Data-Driven', href='/page4'
                        )
                    ],
                ),
                dmc.Divider(
                    label="Process monitoring", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Stack(
                    children=[
                        create_nav_link(
                            icon="streamline:medical-search-diagnosis", label='Fault Detection', href='/page5'
                        ),
                        create_nav_link(
                            icon="eos-icons:monitoring", label='KPI Analysis', href='/page6'
                        )
                    ],
                ),
            ],
        )
        
    ],
style={
    # "position": "fixed",
    # "top": "15rem",
    "left": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    # "background-color": "lightgreen",
    'border-top': '2px solid black',
    "overflow": "hidden"
})
    ],className='text-black',
    style={'border-top': '0px solid black', 'border-bottom': '0px solid black','border-radius': 0,
        "backgroundColor": '#D9E3F1'
        }
    # style=SIDEBAR_STYLE
)

