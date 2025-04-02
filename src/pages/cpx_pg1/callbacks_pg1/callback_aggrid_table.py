from dash import callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import numpy as np
import pandas as pd
import dash
import plotly.graph_objs as go
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import json
import dash_ag_grid as dag
import dash_mantine_components as dmc


def get_callback_update_grid():
    @callback(
            Output('grid_table','children'),
            
            [Input('pretable-data-btn', 'n_clicks')],
            [State('storage_database_raw', "data")],
            prevent_initial_call=True

        )
    def update_dropdown(nclicks,df_storage_database_json):
        # try:
        if True:
            if nclicks is None:
                raise PreventUpdate
            if df_storage_database_json is None:
                raise PreventUpdate
            
            df = pd.read_json(df_storage_database_json, orient='split')
            df['data']=df.index
            # print(df.index,'dfhai')

            tags_ = df.columns.to_list()

            tags_mask = df.columns.to_list()

            nominal_filter_simple = {
                "filterOptions": ["contains", "notContains",'equals','notEqual','startsWith','endsWith','blank'],
                "debounceMs": 200,
                "maxNumConditions": 1,
                "buttons": ["apply", "reset"],
                "closeOnApply": True,
            }

            # "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
            numerical_filter = {"defaultOption":'inRange', 'inRangeInclusive':True,
                        "buttons": ["apply", "reset"],
                        "closeOnApply": True}
            numerical_nominal_filter ={'allowedCharPattern':False,
                        "buttons": ["apply", "reset"],
                        "closeOnApply": True}
            date_filter =     {
                "headerName": "data",
                "filter": "agDateColumnFilter", 
                "valueGetter": {"function": f"d3.timeParse('%Y-%m-%d %H:%M:%S')(params.data.{'data'})"},
                "valueFormatter": {"function": f"params.data.{'data'}"},
                "buttons": ["apply", "reset"],
                "closeOnApply": True
                }

            date_filter = {
                    "headerName": "data",
                    "filter": "agDateColumnFilter",
                    "browserDatePicker": True,
                    "buttons": ["apply", "reset"],
                    # "closeOnApply": True
                    # "minValidYear": 2000,
                    # "maxValidYear": 2025,
                    },
            
            filtercls = ["agDateColumnFilter"]+["agNumberColumnFilter"]*(df.shape[0]-1)
            filterparams = [date_filter]+[numerical_filter]*(df.shape[0]-1)

            columnDefsx =  [{'field':i, 'headerName':j,"headerTooltip":j,'filter':k, 'filterParams':l} for (i,j,k,l) in zip(tags_,tags_mask,filtercls,filterparams)]
            
            for col in columnDefsx:
                if col['headerName'] == 'data':
                    col["pinned"] = "left"
                    col["lockPinned"] = True

            defaultColDef = {
                "initialWidth": 200,
                "wrapHeaderText": True,
                "autoHeaderHeight": True,
            }

            dfx = df.iloc[::10] #df.loc[:,tags_]
            dfx["data"] = pd.to_datetime(dfx['data'], infer_datetime_format=True).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            grid = dag.AgGrid(
                className="ag-theme-quartz-dark", #'ag-theme-balham-dark',#'ag-theme-alpine-dark', #"dbc dbc-ag-grid",
                id="consultas_base_geral_aggrid",
                rowData=dfx.to_dict("records"),
                columnDefs=columnDefsx, #[{"field": i} for i in dfx.columns],
                columnSize="autoSize",#'sizeToFit',#"responsiveSizeToFit",
                defaultColDef=defaultColDef,
                suppressDragLeaveHidesColumns=False,
                persistence=True,
                persisted_props=["filterModel"],
                dashGridOptions={"pagination": True,"tooltipShowDelay": 100, "animateRows": False},
                csvExportParams={
                "fileName": "Consultas_Tabela_Geral.csv",
                }
            )


            return html.Div(children=[dmc.ActionIcon(
                            DashIconify(icon="vscode-icons:file-type-excel2", width=60),
                            size="lg",
                            # variant="filled",
                            id="excel_download_base_geral",
                            n_clicks=0,
                            mb=10,
                        ),grid])
        
        # except Exception as e:
        #     raise PreventUpdate

    return