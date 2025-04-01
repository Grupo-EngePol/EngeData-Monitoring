import dash
import dash_bootstrap_components as dbc


def app_builder():
    app = dash.Dash(__name__, use_pages=True, pages_folder="",external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
    app.config.suppress_callback_exceptions = True
    return app



    