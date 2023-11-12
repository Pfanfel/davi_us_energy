import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from src.app import app



def WarningAlert(msg):
    alert = dbc.Alert(
        msg,
        color="warning",
        id="warning-alert",
        is_open=False,  # Set is_open to True initially
        dismissable=True,
    )
    return alert


@app.callback(
    Output("warning-alert", "is_open"),
    Output('dismissed-store', 'data'),
    Input("warning-alert", "dismissed"),
    Input('dismissed-store', 'data'),
    prevent_initial_call=True
)
def close_alert(dismissed_alert, dismissed_store):
    if dismissed_alert:
        # Alert was dismissed; set the store data
        return False, True
    else:
        # Check if the alert has not been dismissed via store data
        if dismissed_store:
            return False, True
        return True, False
