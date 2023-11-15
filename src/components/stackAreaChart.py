from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go



def StackAreaChart():
    return html.Div([dcc.Graph(id="energy-chart")], className="container mt-4")

