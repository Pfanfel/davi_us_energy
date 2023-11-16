from dash import html
import dash_daq as daq

def CategoryPicker(consumption_filters, production_filters):
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
        html.Div(
            [consumption_filters, production_filters],
            style={"display": "flex", "flex-direction": "row", "flex": "0.5"}
        )
    ])
