from dash import html
import dash_daq as daq
from src.components.stackedItemContainer import StackedItemContainer
from src.components.multiStateSwitch import MultiStateSwitch


def VariablePickerAndToggle(consumption_filters, production_filters):
    container = StackedItemContainer(consumption_filters, production_filters)
    multi_state_switch = MultiStateSwitch('multi-state-switch')
    return html.Div(
        [
            html.P("Select category:"),
            multi_state_switch,
            html.Div(id="production-output"),
            html.Div(id="consumption-output"),
            container,
        ]
    )

