from dash import html
import dash_daq as daq
from src.components.stackedItemContainer import StackedItemContainer


def VariablePickerAndToggle(consumption_filters, production_filters):
    container = StackedItemContainer(consumption_filters, production_filters)
    return html.Div(
        [
            html.P("Toggle consumption icicle plot on/off:"),
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
            html.Div(id="production-output"),
            html.Div(id="consumption-output"),
            container,
        ]
    )

