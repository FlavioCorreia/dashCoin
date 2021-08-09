import dash
from dash.dependencies import Output, Input, State
from dash_bootstrap_components._components.Label import Label
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
from dash_html_components.Div import Div
import pandas as pd
from pandas.core.indexes import multi
from datetime import datetime

from constants import *
from data import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row( 
            [
                dbc.Col( 
                    html.Div([ html.H1('COIN DASH', id='titulo-pagina',) ], style={'text-align':'center'}), 
                    {"size": 5, "offset": 5} 
                ),
                dbc.Button(
                    "Theme", outline=True, color="dark", className="mr-1", id='btn-dark-light'
                )
            ],
            justify="center"
        ),

        html.Div([
            dbc.Row(
                [
                    dbc.Row( dbc.Col( html.H3("COINS") ), justify="end"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='drop-coins',
                            options=[
                                {'label': coin_name, 'value': coin_name.upper()} for coin_name in list_coins
                            ],
                            value= [list_coins[0]],
                            multi= True,
                            style= {'color':'black', 'font-size':20}
                        ),
                        lg=6, sm= 8
                    ),
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='date-picker-coin',
                            min_date_allowed=datetime(2015,1,1),
                            max_date_allowed=datetime(2021,8,4),

                            #start_date=datetime(2015,1,1),
                            #end_date=datetime(2021,8,4),
                            style={'color':'black', 'font-size':14}
                        ),
                        lg=4, sm=8
                    ),
                    
                ],
                justify="center"
            )], 
            style={'text-align':'center'}        
        ),
        
        html.Br(),
    
        html.H1( id='teste' ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(id='line-chart-coins'),
                        style={
                            'text-align':'center', 
                            'box-shadow': '2px 2px 10px #888888',
                            }
                    ),         
                    lg=5, md=10
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(id='bar-chart-coins'),
                        style={
                            'text-align':'center',
                            'box-shadow': '2px 2px 10px #888888',
                            }
                    ),         
                    lg=5, md=10
                )
            ],
            justify="center",          
            
        )

    ],
    id='main-div',
    style={
        'backgroundColor': background_color,
        'color': font_color,
        'height':'100%', 
        'padding': default_padding
    }
)

@app.callback( Output('titulo-pagina', 'children'),
              [Input('btn-dark-light', 'n_clicks')],
              [State('btn-dark-light', 'n_clicks')])
def callbackBtnDarkLight( n_clicks, n_clicks2 ):
    global theme    
    if n_clicks is None or int(n_clicks) % 2  == 0:
        theme = "DARK"
        return "NIGHT THEME"

    theme = "LIGHT"
    return "LIGHT THEME"

@app.callback(Output('line-chart-coins', 'figure'),
              [Input('drop-coins', 'value')])
def callbackLineChartCoin(value):
    setSelectedCoins(value)
    return createLineChartCoin(value, theme)

@app.callback(Output('bar-chart-coins', 'figure'),
              [Input('drop-coins', 'value')])
def callbackBarChartCoin(value):
    return createBarChartCoin(value, theme)

@app.callback(Output('drop-coins', 'value'),
              [Input('btn-dark-light', 'n_clicks')], # QUANDO O BTN DE TEMA É CLICADO
              [State('btn-dark-light', 'n_clicks')])
def callbackDropCoin(n_clicks, n_clicks2):
    return getSelectedCoins()

###########################################################################################################
@app.callback(Output('teste', 'children'),
              [Input('date-picker-coin', 'start_date'),
               Input('date-picker-coin', 'end_date')])
def callbackTeste( start_date, end_date ):
    print( type(start_date), end_date)
    return str(start_date)+' '+str(end_date)


@app.callback(Output('main-div', 'style'),
              [Input('btn-dark-light', 'n_clicks')], # QUANDO O BTN DE TEMA É CLICADO
              [State('btn-dark-light', 'n_clicks')])
def callbackMainDiv(n_clicks, n_clicks2):
    if theme == 'DARK':
        return {
            'backgroundColor': background_color,
            'color': font_color,
            'height':'100%', 
            'padding': default_padding
        }

    return {
        'backgroundColor': background_color2,
        'color': font_color2,
        'height':'100%', 
        'padding': default_padding
    }

if __name__ == '__main__':
    app.run_server( host='0.0.0.0', port=7788, debug=True)
    #app.run_server( host='0.0.0.0', port=7788) # SEM O BTN AZUL INF DIR