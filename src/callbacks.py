# import dash IO and graph objects
from dash.dependencies import Input, Output

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import dash html, bootstrap components, and tables for datatables
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash import dash_table

# Import app
from app import app

# Import custom data.py
import data


@app.callback(
    [
        Output("year-slider", "disabled"),
        Output("year-slider", "value"),
        Output("year-toggle", "label"),
    ],  # Add an Output for the label
    Input("year-toggle", "on"),
)
def update_slider_state(on):
    label = setLabel(on)  # Calculate the label based on the toggle state
    if on:
        # TODO: Clean up magic numbers and import min and max of dataframe instead.
        return False, [1998], label  # Return label as a part of the tuple
    else:
        return False, [1998, 2021], label  # Return label as a part of the tuple


def setLabel(on):
    if on:
        return "Select Year"
    else:
        return "Select Time Interval"


@app.callback(
    Output("output-state-click", "children"),
    Input("choropleth-map-consumption", "clickData"),
)
# TODO: Not working, fix this
def display_clicked_state(clickData):
    print(clickData)
    if clickData is not None:
        state_code = clickData["points"][0]["hovertext"]
        return f"Clicked state code: {state_code}"
    else:
        return ""


@app.callback(
    [
        Output("icicle-plot-production", "style"),
        Output("icicle-plot-consumption", "style"),
    ],
    Input("category-toggle", "on"),
)
def toggle_consumption_map_visibility(toggle_state):
    # TODO: Make it so, that if the map is not visible, it is full width

    if not toggle_state:
        return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "none"}

    return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "flex"}


"""
This function is used to extract the category from the clickData of the icicle plots which has the ids icicle-plot-production and icicle-plot-consumption.
"""


@app.callback(
    Output(component_id="production-output", component_property="children"),
    Input("icicle-plot-production", "clickData"),
)
def change_clicked_production_value(clickData):
    # TODO: Not working, fix this
    print(clickData)
    if clickData is not None:
        category = clickData["points"][0]["label"]
        return f"Clicked production category: {category}"
    else:
        return ""
