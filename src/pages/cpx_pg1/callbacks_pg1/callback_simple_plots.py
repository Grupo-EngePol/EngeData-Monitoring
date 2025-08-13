from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc

from utils.cache_df import get_df_cached

def _fetch_df(data) -> pd.DataFrame:
    """Recupera DataFrame do storage, aceitando tanto chave de cache (df:...) quanto JSON orient='split'."""
    if data is None:
        return pd.DataFrame()
    # Chave de cache
    if isinstance(data, str) and data.startswith("df:"):
        return get_df_cached(data)
    # JSON (fallback para sessões antigas)
    try:
        return pd.read_json(data, orient="split")
    except Exception:
        # Caso o Store tenha recebido um dict serializado automaticamente
        if isinstance(data, dict) and {'columns', 'data'}.issubset(data.keys()):
            try:
                return pd.DataFrame(data.get('data'), columns=data.get('columns'))
            except Exception:
                return pd.DataFrame()
        return pd.DataFrame()


def _is_datetime_series(s: pd.Series) -> bool:
    return pd.api.types.is_datetime64_any_dtype(s) or pd.api.types.is_datetime64tz_dtype(s)


def _coerce_numeric(s: pd.Series) -> pd.Series:
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    if pd.api.types.is_numeric_dtype(s):
        return s
    s_str = s.astype(str)
    s_str = s_str.str.replace("\u00A0", "", regex=False)
    s_str = s_str.str.replace(" ", "", regex=False)
    if s_str.str.contains(",").mean() > 0.5 and s_str.str.contains(".").mean() > 0.5:
        s_str = s_str.str.replace(".", "", regex=False)
        s_str = s_str.str.replace(",", ".", regex=False)
    else:
        s_str = s_str.str.replace(",", ".", regex=False)
    return pd.to_numeric(s_str, errors="coerce")


from dash import dcc, html

def create_ts_plot_layout(df):
    yaxis_options = [
        {"label": col, "value": col} for col in df.columns if col != "data"
    ]

    plot_mode_options = [
        {"label": "Lines", "value": "lines"},
        {"label": "Markers", "value": "markers"},
        {"label": "Lines+Markers", "value": "lines+markers"},
    ]

    layout = html.Div([
        dcc.Dropdown(
            id="ts-yaxis-dropdown",
            options=yaxis_options,
            value=[yaxis_options[0]["value"]] if yaxis_options else [],
            multi=True,
            clearable=False,
            style={"width": "60%", "display": "inline-block"},
        ),
        dcc.RadioItems(
            id="ts-plot-mode",
            options=plot_mode_options,
            value="markers",
            labelStyle={"display": "inline-block", "margin-left": "20px"},
            style={"width": "35%", "display": "inline-block", "verticalAlign": "top"},
        ),
        dcc.Graph(id="ts-graph"),
        html.Div(id="debug-output"),
    ])

    return layout


def register_simple_plot_callbacks():
    @callback(
        Output('dce_view_host', 'children'),
        Input('view-data-btn', 'n_clicks'),
        State('storage_database_raw', 'data'),
        prevent_initial_call=True
    )
    def display_plot_component(n_clicks, store_val):
        df = _fetch_df(store_val)
        if df.empty:
            raise PreventUpdate
        return create_ts_plot_layout(df)

@callback(
    Output("ts-graph", "figure"),
    Output("debug-output", "children"),
    Input("storage_database_raw", "data"),
    Input("ts-yaxis-dropdown", "value"),
    Input("ts-plot-mode", "value"),
)
def update_ts_graph(data, yaxis_cols, plot_mode):
    if not data or not yaxis_cols:
        return go.Figure(), "No data or y-axis column selected"

    df = _fetch_df(data)

    # Determine x-axis data
    x = None
    x_label = None
    for col in df.columns:
        if _is_datetime_series(df[col]):
            x = df[col]
            x_label = col
            break
    if x is None:
        # Use index if no datetime column found
        x = df.index
        x_label = "index"

    fig = go.Figure()
    debug_info = []

    for yaxis_col in yaxis_cols:
        y = _coerce_numeric(df[yaxis_col])
        valid_mask = y.notna()
        y_clean = y[valid_mask]
        if isinstance(x, pd.Series) or isinstance(x, pd.Index):
            x_clean = x[valid_mask]
        else:
            x_clean = pd.Series(x).iloc[valid_mask.values]

        # Enforce line mode if points exceed 50k
        if len(y_clean) > 50000:
            mode = "lines"
        else:
            if plot_mode == "lines+markers":
                mode = "lines+markers"
            elif plot_mode == "lines":
                mode = "lines"
            elif plot_mode == "markers":
                mode = "markers"
            else:
                mode = "lines"

        fig.add_trace(
            go.Scatter(
                x=x_clean,
                y=y_clean,
                mode=mode,
                name=yaxis_col,
            )
        )

        debug_info.append(f"{yaxis_col}: {len(y_clean)} points, mode: {mode}")

    fig.update_layout(
        title=f"Time Series Plot",
        xaxis_title=x_label,
        yaxis_title=", ".join(yaxis_cols),
        template="plotly_white",
    )

    return fig, " | ".join(debug_info)