from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
from data import data as dt
import pandas as pd
from dash import html



def MapContainer(USmapConsumption, USmapProduction):
    return html.Div(
        [
            html.Div(
                [USmapConsumption], id="consumption-map-container", style={"flex": "1"}
            ),
            html.Div(
                [USmapProduction],
                id="conditional-map-container",
                style={"flex": "1", "display": "none"},
            ),
        ],
        style={"display": "flex", "flex-direction": "row", "flex": "1"},
        className="row",
    )
