from dash import html, dcc
import plotly.graph_objects as go


def StackedAreaChart_Percentage():
    return html.Div(
        [
            dcc.Graph(
                id="stacked-area-chart-percentage",
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )

def StackedAreaChart():
    return html.Div(
        [
            dcc.Graph(
                id="stacked-area-chart",
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )

