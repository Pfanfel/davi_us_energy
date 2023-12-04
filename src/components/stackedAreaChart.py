from dash import html, dcc
import plotly.graph_objects as go


def StackedAreaChart_Percentage(name):
    return html.Div(
        [
            dcc.Graph(
                id=name,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )

def StackedAreaChart(name):
    return html.Div(
        [
            dcc.Graph(
                id=name,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )

