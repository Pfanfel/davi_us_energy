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
