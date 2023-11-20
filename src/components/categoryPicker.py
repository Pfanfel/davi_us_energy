from dash import html
import dash_daq as daq

def Container(id1, id2):
    return html.Div([
        html.Div([id1], style={"flex": "1"}),
        html.Div([id2], style={"flex": "1"}),
    ], style={"display": "flex", "flex-direction": "row", "flex": "1"}, className='row')


def CategoryPicker(consumption_filters, production_filters):
    container = Container(consumption_filters, production_filters)
    return html.Div([
        html.H2("Select Category"),
        daq.BooleanSwitch(
            id="category-toggle",
            on=False,
            label=True,
            labelPosition="bottom",
            style={
                "display": "inline-block",
                "vertical-align": "middle",
                "margin-left": "10px",
                "transform": "scale(0.8)",
            },
        ),
        container,
    ])
