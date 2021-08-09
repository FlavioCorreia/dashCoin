import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import dash_auth

import pandas_datareader.data as web
import pandas as pd
import os
os.environ["IEX_API_KEY"] = "pk_df3fd3aad7314d2aa65d76ae16147ade"
#https://iexcloud.io/console/tokens

USERNAME_PASSWORD_PAIRS = [['admin', 'admin'], ['user','user']]

app = dash.Dash()
auth = dash_auth.BasicAuth( app, USERNAME_PASSWORD_PAIRS)

nsdq = pd.read_csv("data/NASDAQcompanylist.csv", sep=",")
nsdq.set_index('Symbol', inplace=True)
options = []

for tic in nsdq.index:
    mydict = {} # {'label':'user sees', 'value':'script sees'}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic
    mydict['value'] = tic
    options.append( mydict )

app.layout = html.Div([
                html.H1("Stock Dashboard"),
                html.Div([
                    html.H3(
                        "Enter a stockc symbol", 
                        style={'paddingRight':'30px'}
                        ),
                    dcc.Dropdown(
                        id='my_stock_picker',
                        value=['TSLA'],
                        options=options,
                        multi=True,
                        style={'fontSize':24, 'width':'30%'}
                    ),
                ], style={'display':'inline-block', 
                            'verticalAlign':'top',
                                'width':'60%'}),
                               
                html.Div([
                    html.H3('Select Start and End Date:'),
                    dcc.DatePickerRange(
                        id='my_date_picker',
                        min_date_allowed=datetime(2015,1,1),
                        max_date_allowed=datetime.today(),
                        start_date=datetime(2020,1,1),
                        end_date=datetime.today()
                    )
                ], style={'display':'inline-block'}),
                
                html.Div([
                    html.Button(
                        id='submit-button', 
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':24, 'marginLeft':'30px'}
                    )
                ], style={'display':'inline-block'}),
                dcc.Graph(
                    id='my_graph',
                    figure={
                        'data':[{
                                'x':[1,2,3], 
                                'y':[3,2,1]
                            }
                        ],
                        'layout':{
                            'title':'Df Title'
                        }}

                )
])

@app.callback( Output('my_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my_stock_picker', 'value'),
               State('my_date_picker','start_date'),
               State('my_date_picker','end_date')])
def update_graph( n_clicks, stock_ticker, start_date, end_date ):
    start = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end = datetime.strptime(end_date[:10], "%Y-%m-%d")
    #end = datetime.today()

    traces = []
    for tic in stock_ticker:
        df = web.DataReader( tic, 'iex', start, end) 
        traces.append( {'x':df.index, 'y':df['close'], 'name':tic} )

    fig = {
        'data': traces,
        'layout':{
                'title': stock_ticker
                }
    }
    return fig

if __name__ == '__main__':
    app.run_server( host='0.0.0.0', port=8082)