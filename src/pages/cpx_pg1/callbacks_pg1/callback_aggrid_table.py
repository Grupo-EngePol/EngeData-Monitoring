from dash import callback, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash_iconify import DashIconify

from utils.cache_df import get_df_cached

def get_callback_update_grid():
    @callback(
        Output('grid_table','children'),
        Input('pretable-data-btn', 'n_clicks'),
        State('storage_database_raw', "data"),   # <- agora é a CHAVE do cache
        prevent_initial_call=True
    )
    def update_dropdown(nclicks, df_key):
        if not nclicks or not df_key:
            raise PreventUpdate

        # 1) Busca do cache e saneamento básico
        df = get_df_cached(df_key).copy()
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index, errors="coerce")
        df = df[~df.index.isna()].sort_index()

        # 2) Amostragem e coluna 'data' textual para a Grid
        dfx = df.iloc[::1].copy()
        dfx["data"] = dfx.index.strftime("%Y-%m-%d %H:%M:%S")

        # 3) Ordem das colunas: 'data' à esquerda, depois as demais
        value_cols = [c for c in dfx.columns if c != "data"]
        columns_order = ["data"] + value_cols

        # 4) Definições de filtro por tipo (sem tupla acidental)
        date_col_def = {
            "field": "data",
            "headerName": "data",
            "pinned": "left",
            "lockPinned": True,
            "filter": "agDateColumnFilter",
            "browserDatePicker": True,
        }

        columnDefs = [date_col_def]
        for col in value_cols:
            col_def = {
                "field": col,
                "headerName": col,
                "sortable": True,
                "resizable": True,
            }
            if pd.api.types.is_numeric_dtype(dfx[col]):
                col_def["filter"] = "agNumberColumnFilter"
                # formatação opcional com d3
                col_def["valueFormatter"] = {
                    "function": "isFinite(params.value) ? d3.format('.5~f')(params.value) : params.value"
                }
            else:
                col_def["filter"] = "agTextColumnFilter"
            columnDefs.append(col_def)

        defaultColDef = {
            "flex": 1,
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
            "filter": True,
            "sortable": True,
            "resizable": True,
        }

        grid = dag.AgGrid(
            className="ag-theme-quartz-dark",
            id="consultas_base_geral_aggrid",
            rowData=dfx[columns_order].to_dict("records"),
            columnDefs=columnDefs,
            columnSize="autoSize",
            defaultColDef=defaultColDef,
            persistence=True,
            persisted_props=["filterModel","sortModel","columnState"],
            suppressDragLeaveHidesColumns=False,
            dashGridOptions={"pagination": True, "tooltipShowDelay": 100, "animateRows": False},
            csvExportParams={"fileName": "Consultas_Tabela_Geral.csv"},
        )

        return html.Div(children=[
            dmc.ActionIcon(
                DashIconify(icon="vscode-icons:file-type-excel2", width=60),
                size="lg",
                id="excel_download_base_geral",
                n_clicks=0,
                mb=10,
            ),
            grid
        ])

    return
