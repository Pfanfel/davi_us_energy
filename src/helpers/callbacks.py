import pandas as pd
from dash import Input, Output, State, ALL, dash
from src.app import app
from src.helpers.filter import find_root_node, filterData
from data import data_origninal as dt


@app.callback(
    Output("stads_id", "data"),
    Input(dt.col_names[0], "value"),
    Input(dt.col_names[1], "value"),
    Input("stads_id", "data"),
    Input("year-slider", "value"),
    Input("choropleth-map", "clickData"),  # Add this input
    prevent_initial_call=True,
)
def handle_select_event_energy_type(
    selected_energy_types,
    selected_energy_activity,
    current_data,
    time_range,
    click_data,
):
    current_data_df = pd.DataFrame(dt.stads_df)  # Convert the data to a DataFrame
    if (
        not selected_energy_types
        and not selected_energy_activity
        and not time_range
        and not click_data
    ):
        return current_data_df.to_dict(
            "records"
        )  # No filters selected, return the current data as is

    filtered_data = current_data_df.copy()  # Make a copy of the current data

    if click_data:
        print("Map was clicked")
        state_code = click_data["points"][0]["location"]
        print(f"Clicked state {state_code}")
        filtered_data = filterData([state_code], filtered_data, "StateCode")

    if selected_energy_types:
        filtered_data = filterData(
            selected_energy_types, filtered_data, dt.col_names[0]
        )

    if selected_energy_activity:
        filtered_data = filterData(
            selected_energy_activity, filtered_data, dt.col_names[1]
        )

    filtered_data_copy = filtered_data.copy()  # Make a copy of the current data

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        filtered_data = filtered_data[filtered_data["Year"] == single_year]
        if not filtered_data.empty:
            return filtered_data.to_dict("records")
        else:
            return ["No data selected"]

    if time_range and len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        filtered_data_copy = filtered_data_copy[
            (filtered_data_copy["Year"] >= min_year)
            & (filtered_data_copy["Year"] <= max_year)
        ]
        filtered_data = filtered_data_copy

    return filtered_data.to_dict("records")


@app.callback(
    Output("year-slider", "disabled"),
    Output("year-slider", "value"),
    Output("year-toggle", "label"),  # Add an Output for the label
    Input("year-toggle", "on"),
)
def update_slider_state(on):
    label = setLabel(on)  # Calculate the label based on the toggle state
    if on:
        return False, [1960], label  # Return label as a part of the tuple
    else:
        return False, [1960, 2021], label  # Return label as a part of the tuple


def setLabel(on):
    if on:
        return "Select Year"
    else:
        return "Select Time Interval"


def update_slider_state(on):
    label = setLabel(on)  # Calculate the label based on the toggle state
    if on:
        return False, [1960], label
    else:
        return False, [1960, 2021], label
