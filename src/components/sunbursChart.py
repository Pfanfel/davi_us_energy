from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def SunburstChart():
    return html.Div(
        [dcc.Graph(id="sun-chart")],
        className="pretty_container",
    )


