import pandas as pd
import plotly.graph_objects as go
from constants import *

df_coins = pd.read_csv("data/coins.csv")
list_coins = df_coins.Currency.unique()

def createLineChartCoin( list_coin_names, theme ):
    fig = go.Figure()

    for coin in list_coin_names:
        df_aux = df_coins[ df_coins.Currency == coin ]
        
        fig.add_trace(
            go.Scatter(
                y=df_aux["Closing Price (USD)"], 
                x=df_aux["Date"],
                name=coin,
                mode="lines"
            )
        )

    if theme == 'DARK':
        fig["layout"] = {
                            'title':'Line Chart',
                            'plot_bgcolor': background_graph_color, # background do grafico
                            'paper_bgcolor': background_graph_color, # ao redor do grafico
                            'font':{'color': font_color},
                            'height': default_graphic_height,  
                        }
    elif theme == 'LIGHT':
        fig["layout"] = {
                            'title':'Line Chart',
                            'plot_bgcolor': background_graph_color2, # background do grafico
                            'paper_bgcolor': background_graph_color2, # ao redor do grafico
                            'font':{'color': font_color2},
                            'height': default_graphic_height
                        }
    return fig


def createBarChartCoin( list_coin_names, theme ):
    df_info = pd.DataFrame( columns=['coin', 'min', 'max', 'atual'])
    for coin in list_coin_names:
        df_aux = df_coins.loc[ df_coins.Currency == coin ]

        minimum = float( df_aux['24h Low (USD)'].min() )
        maximum = float( df_aux['24h High (USD)'].max() )        
        last_value = float( df_aux.tail(1).iloc[0, 3] )
        #last_value = float( df_aux.loc[ len(df_aux)-1, 'Closing Price (USD)'] )
        
        df_info.loc[ len(df_info) ] = [ coin, round(minimum, 2), round(maximum, 2), round(last_value, 2) ]

    fig = go.Figure()
    for indice in range( len(df_info) ):
        fig.add_trace(
            go.Bar(
                name= df_info.loc[indice,'coin'], 
                x= ['Minimum', 'Maximum', 'Last Value'], 
                y=df_info.loc[indice, ['min','max', 'atual']], 
                text=df_info.loc[indice,'coin'], 
                textposition='outside',
            )
        )

    if theme == 'DARK':
        fig["layout"] = {
                            'title':'Bar Chart',
                            'plot_bgcolor': background_graph_color, # background do grafico
                            'paper_bgcolor': background_graph_color, # ao redor do grafico
                            'font':{'color': font_color},     
                            'height': default_graphic_height,                   
                        }

    elif theme == 'LIGHT':
        fig["layout"] = {
                            'title':'Bar Chart',
                            'plot_bgcolor': background_graph_color2, # background do grafico
                            'paper_bgcolor': background_graph_color2, # ao redor do grafico
                            'font':{'color': font_color2},     
                            'height': default_graphic_height,                   
                        }

    fig.update_layout(barmode='group')
    return fig