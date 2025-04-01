from dash import html
import dash_bootstrap_components as dbc

def header():
    header = dbc.Card([ 
    dbc.CardHeader(children=[       
    html.A(
            dbc.Row([
                # dbc.Col(html.Img(src=logo_nitro_encoded,className="w-100"),width=2,align="center",style={'margin-right': '5px','verticalAlign': 'top','border-right': '2px solid white'}),

                dbc.Col(dbc.NavbarBrand(children = [html.H5("Nome APP",
                                            style={'color':'white','verticalAlign': 'top','margin-top': '10px','margin-left': '5px'})], style={'margin-top': '2px','verticalAlign': 'top'}),width=12,align="center", className="ms-2"),
                
                ],
                align="center",
                className="g-0",
            ),
            # href="/",
            href='https://plotly.com',
            style={"textDecoration": "none"},
        )]
        ,
        style={
                "border-radius": "1px",
                "border-width": "2px",
                "border-bottom": "2px solid black",
                # "backgroundColor": '#003760',
            })
    ],color='primary')
    return header