from dash import dcc
from dash import html


def MultiStateSwitch(name):
    return html.Div(
        [dcc.RadioItems(
            id=name,
            options=[
                {'label': ' Analyze Consumption', 'value': 'display_consumption'},
                {'label': ' Analyze Production', 'value': 'display_production'},
                {'label': ' Combined Analysis', 'value': 'display_both'},
            ],
            value='display_consumption',
            style={
                "display": "inline-block",
                "vertical-align": "middle",
                "margin-left": "10px",
                "transform": "scale(0.9)",
            },
        )],
    )
