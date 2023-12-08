from dash import html

def StackedItemContainer(id1, id2):
    return html.Div(
        [
            html.Div([id1], style={"flex": "1"}),
            html.Div([id2], style={"flex": "1"}),
        ],
        style={"display": "flex", "flex-direction": "column", "flex": "1"},
        className="row",
    )


def HorizontalItemContainer(component1, component2):
    return html.Div(
        children=[
            html.Div(component1, style={'display': 'inline-block', 'width': '50%',  "verticalAlign": "top"}),
            html.Div(component2, style={'display': 'inline-block', 'width': '50%',   "verticalAlign": "top"})
        ],
        style={
            "display": "inline-block",
            "width": "100%",
            "verticalAlign": "top"
        },
    )
def HorizontalItemContainer_Custom(component1, component2):
    return html.Div(
        children=[
            html.Div(component1, style={'display': 'inline-block', 'width': '15%', "verticalAlign": "top"}),
            html.Div(component2, style={'display': 'inline-block', 'width': '85%', "verticalAlign": "top"})
        ],
        style={
            "display": "inline-block",
            "width": "100%",
            "verticalAlign": "top",
            "margin-top": "30px",  # Adds space above the container
            "margin-bottom": "50px"  # Adds space below the container
        },
    )
