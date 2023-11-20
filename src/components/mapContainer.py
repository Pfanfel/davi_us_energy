from dash import dcc
from dash import html
import plotly.express as px


# components/mapContainer.py
from dash import dcc, html

def MapContainer(USmapConsumption, USmapProduction):
    return html.Div([
        html.Div([USmapConsumption], id='consumption-map-container', style={"flex": "1"}),
        html.Div([USmapProduction], id='conditional-map-container', style={"flex": "1", "display": "none"}),
    ], style={"display": "flex", "flex-direction": "row", "flex": "1"}, className='row')

