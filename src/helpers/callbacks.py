import pandas as pd
from dash import Input, Output, State, ALL, dash
from src.app import app
from src.helpers.filter import find_root_node, filterData
from src.data import data


@app.callback(
    Output('stads_id', 'data'),
    Input(data.col_names[0], 'value'),
    Input(data.col_names[1], 'value'),
    Input('stads_id', 'data'),
    prevent_initial_call=True
)
def handle_select_event_energy_type(selected_energy_types, selected_energy_activity, current_data):
    current_data_df = pd.DataFrame(current_data)  # Convert the data to a DataFrame

    if not selected_energy_types and not selected_energy_activity:
        return current_data_df.to_dict('records')  # No categories selected, return the current data as is

    filtered_data = current_data_df.copy()  # Make a copy of the current data

    if selected_energy_types:
        filtered_data = filterData(selected_energy_types, filtered_data, data.col_names[0])

    if selected_energy_activity:
        filtered_data = filterData(selected_energy_activity, filtered_data, data.col_names[1])

    return filtered_data.to_dict('records')
