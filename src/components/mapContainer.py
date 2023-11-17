from dash import dcc
from dash import html
import plotly.express as px


# components/mapContainer.py
from dash import dcc, html

def MapContainer():
    return html.Div([
        html.Div(id='consumption-map-container', style={"flex": "1"}),
        html.Div(id='conditional-map-container', style={"flex": "1", "display": "none"}),
    ], style={"display": "flex", "flex-direction": "row", "flex": "1"}, className='row')
