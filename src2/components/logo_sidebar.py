from dash import html
from utils.images import logo_EngeData_encoded_white,logo_EngeData_encoded_dark

logo_sidebar_white = html.A(

              html.Img(src=logo_EngeData_encoded_white,className="w-100"),
              href='https://plotly.com',
              style={"textDecoration": "none",
                     'margin-right': '1px',
                     'verticalAlign': 'top',
                     'border-bottom': '0px solid black'},
       )

logo_sidebar_dark = html.A(

              html.Img(src=logo_EngeData_encoded_dark,className="w-100"),
              href='https://plotly.com',
              style={"textDecoration": "none",
                     'margin-right': '1px',
                     'verticalAlign': 'top',
                     'border-bottom': '0px solid black'},
       )