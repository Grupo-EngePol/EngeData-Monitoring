# package imports
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# local imports
from utils.images import logo_senai_encoded
from dash.exceptions import PreventUpdate
import json

# component
navbar = dbc.Navbar(#className='bg-primary',
                    children=[
    dbc.Container(
        [
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src=logo_senai_encoded, height='70px'),style={'margin-right': '5px'}),
                    dbc.Col(html.H6('  ',style={'height':'55px'}),style={'border-right': '2px solid white'}),
                    dbc.Col(dbc.NavbarBrand("NOME APP", className="ms-2",style={"fontSize": "30px"}))
                    ],
                    align="center",
                    className="g-0",
                ),
                # href="/",
                href='https://plotly.com',
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler",n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Home",id='navlink_home',href='/')),
                                dbc.NavItem(dbc.NavLink("Page1",id='navlink_pg1',href='/page1',disabled=False)),
                                dbc.NavItem(dbc.NavLink("Page2",id='navlink_pg2',href='/page2',disabled=False,n_clicks=0)),
                                dbc.NavItem(
                                    dbc.NavLink("Page3",id='navlink_pg3',href='/page3',disabled=False),
                                    # dbc.NavLink("Complex Page",href='/complex'),
                                    # add an auto margin after page 2 to
                                    # push later links to end of nav
                                    className="me-auto",
                                ),
                                
                                dbc.NavItem(dbc.NavLink("Help")),
                                dbc.NavItem(dbc.NavLink("About")),
                            ],
                            # make sure nav takes up the full width for auto
                            # margin to get applied
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                # the row should expand to fill the available horizontal space
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    )],
    dark=True,
    color="primary",
    # color='#78C2AD'
)

# add callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

