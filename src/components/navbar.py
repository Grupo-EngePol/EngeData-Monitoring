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
                dmc.Text(label, size="sm", c="black", fw=700),
            ]
        ),
        href=href,
        style={"textDecoration": "none", "display": "block", "marginBottom": "10px"},
    )


navbar = html.Div([
    dbc.Nav(
        vertical='md',
        pills=True,
        fill=True,
        horizontal='start',
        navbar_scroll=False,
        children=[
            html.H4("Menu", className='text-bold-black'),
            html.Hr(),
            
            # Seção Home
            create_nav_link(
                icon="radix-icons:rocket",
                label="Home",
                href="/",
            ),
            
            # Divider
            html.Div([
                html.Hr(),
                html.P("Data characterization", style={"margin": "10px 0", "fontWeight": "bold"}),
            ]),
            
            # Seção Data characterization
            create_nav_link(
                icon="hugeicons:chart-line-data-02", 
                label="Data Visualization", 
                href="/page1"
            ),
            create_nav_link(
                icon="fluent-mdl2:bar-chart-vertical-filter-solid", 
                label="Data Filtering", 
                href="/page2"
            ),
            
            # Divider
            html.Div([
                html.Hr(),
                html.P("Process modeling", style={"margin": "10px 0", "fontWeight": "bold"}),
            ]),
            
            # Seção Process modeling
            create_nav_link(
                icon="hugeicons:market-analysis", 
                label='Data Rectification', 
                href='/page3'
            ),
            create_nav_link(
                icon="eos-icons:neural-network", 
                label='Data-Driven', 
                href='/page4'
            ),
            
            # Divider
            html.Div([
                html.Hr(),
                html.P("Process monitoring", style={"margin": "10px 0", "fontWeight": "bold"}),
            ]),
            
            # Seção Process monitoring
            create_nav_link(
                icon="streamline:medical-search-diagnosis", 
                label='Fault Detection', 
                href='/page5'
            ),
            create_nav_link(
                icon="eos-icons:monitoring", 
                label='KPI Analysis', 
                href='/page6'
            ),
        ]
    )
],
className='text-black',
style={
    'border-top': '0px solid black',
    'border-bottom': '0px solid black',
    'border-radius': 0,
    "backgroundColor": '#D9E3F1',
    "left": 0,
    "width": "20rem",
    "padding": "1rem 1rem",
    'border-top': '2px solid black',
    # "overflow": "hidden"  # Removed overflow hidden
})
