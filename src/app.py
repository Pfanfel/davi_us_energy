# Import packages
from dash import Dash, html, dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from components import navbar, footer, timeSlider, map
import feffery_antd_components as fac
import pandas as pd
from dash import Input, Output, State, ALL
from src.helpers.filter import find_root_node, filterData, filterByValues, filterByValue
from src.data import data as dt


# Initialize the app
app = dash.Dash(
    __name__,
    use_pages=True,  # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],  # fetch the proper css items we want
    meta_tags=[
        {  # check if device is a mobile device. This is a must if you do any mobile styling
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
        }
    ],
    suppress_callback_exceptions=True,
    title="🇺🇸 Awesome Data Visualization for US Energy Production and Consumption by State",
)


# @app.callback(
#     Output('stads_id', 'data'),
#     Input(dt.col_names[0], 'value'),
#     Input(dt.col_names[1], 'value'),
#     Input('stads_id', 'data'),
#     Input('year-slider', 'value'),
#     Input('choropleth-map', 'clickData'),  # Add this input
#     prevent_initial_call=True
# )
# def handle_select_event_energy_type(selected_energy_types, selected_energy_activity, current_data, time_range, click_data):
#     current_data_df = pd.DataFrame(dt.stads_df)  # Convert the data to a DataFrame
#     if not selected_energy_types and not selected_energy_activity and not time_range and not click_data:
#         return current_data_df.to_dict('records')  # No filters selected, return the current data as is
#
#     filtered_data = current_data_df.copy()  # Make a copy of the current data
#
#     if click_data:
#         print("Map was clicked")
#         state_code = click_data['points'][0]['location']
#         print(f"Clicked state {state_code}")
#         filtered_data = filterData([state_code], filtered_data, 'StateCode')
#
#     if selected_energy_types:
#         filtered_data = filterData(selected_energy_types, filtered_data, dt.col_names[0])
#
#     if selected_energy_activity:
#         filtered_data = filterData(selected_energy_activity, filtered_data, dt.col_names[1])
#
#     filtered_data_copy = filtered_data.copy()  # Make a copy of the current data
#
#     # Handle when the checkbox is selected, and the range is empty, but a single year is selected
#     if len(time_range) == 1:
#         single_year = time_range[0]
#         single_year = int(single_year)
#         filtered_data = filtered_data[filtered_data['Year'] == single_year]
#         if not filtered_data.empty:
#             return filtered_data.to_dict('records')
#         else:
#             return ["No data selected"]
#
#     if time_range and len(time_range) == 2:
#         min_year, max_year = time_range
#         min_year = int(min_year)
#         max_year = int(max_year)
#
#         filtered_data_copy = filtered_data_copy[
#             (filtered_data_copy['Year'] >= min_year) & (filtered_data_copy['Year'] <= max_year)
#             ]
#         filtered_data = filtered_data_copy
#
#     return filtered_data.to_dict('records')

@app.callback(
    Output('stads_id_consumption', 'data'),
    Input('stads_id_consumption', 'data'),
    Input('consumption-filter', 'value'),
    Input('year-slider', 'value'),
    Input('choropleth-map', 'clickData'),  # Add this input
    prevent_initial_call=True
)
def handle_select_event_consumption(selected_consumption, time_range, click_data):
    current_data_df = pd.DataFrame(dt.stads_df)  # Convert the data to a DataFrame

    if not selected_consumption and not time_range and not click_data:
        return current_data_df.to_dict('records')  # No filters selected, return the current data as is

    filtered_data = current_data_df.copy()  # Make a copy of the current data

    if click_data:
        print("Map was clicked")
        state_code = click_data['points'][0]['location']
        print(f"Clicked state {state_code}")
        filtered_data = filterData([state_code], filtered_data, 'StateCode')

    if selected_consumption:
        filtered_data = filterByValues(selected_consumption, filtered_data)



    filtered_data_copy = filtered_data.copy()  # Make a copy of the current data

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        filtered_data = filtered_data[filtered_data['Year'] == single_year]
        if not filtered_data.empty:
            return filtered_data.to_dict('records')
        else:
            return ["No data selected"]

    if time_range and len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        filtered_data_copy = filtered_data_copy[
            (filtered_data_copy['Year'] >= min_year) & (filtered_data_copy['Year'] <= max_year)
            ]
        filtered_data = filtered_data_copy

    return filtered_data.to_dict('records')


@app.callback(
    Output('stads_id_production', 'data'),
    Input('stads_id_production', 'data'),
    Input('production-filter', 'value'),
    Input('year-slider', 'value'),
    Input('choropleth-map', 'clickData'),  # Add this input
    prevent_initial_call=True
)
def handle_select_event_production(selected_production, time_range, click_data):
    current_data_df = pd.DataFrame(dt.stads_df)  # Convert the data to a DataFrame

    if not selected_production and not time_range and not click_data:
        return current_data_df.to_dict('records')  # No filters selected, return the current data as is

    filtered_data = current_data_df.copy()  # Make a copy of the current data

    if click_data:
        print("Map was clicked")
        state_code = click_data['points'][0]['location']
        print(f"Clicked state {state_code}")
        filtered_data = filterData([state_code], filtered_data, 'StateCode')

    if selected_production:
        filtered_data = filterByValues(selected_production, filtered_data)



    filtered_data_copy = filtered_data.copy()  # Make a copy of the current data

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        filtered_data = filtered_data[filtered_data['Year'] == single_year]
        if not filtered_data.empty:
            return filtered_data.to_dict('records')
        else:
            return ["No data selected"]

    if time_range and len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        filtered_data_copy = filtered_data_copy[
            (filtered_data_copy['Year'] >= min_year) & (filtered_data_copy['Year'] <= max_year)
            ]
        filtered_data = filtered_data_copy

    return filtered_data.to_dict('records')


def CreateCategoryFilteringTree(categories, id, placeHolder):
    return fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
    )


# define the navbar and footer
nav = navbar.Navbar()
footer = footer.Footer()
timeSlider = timeSlider.TimeSlider()

data_table_production = dash_table.DataTable(
    id='stads_id_production',
    data=filterByValue('production', dt.stads_df.copy()).to_dict('records'),
    page_size=10,  # Number of rows per page
    page_current=0,  # Current page
)

data_table_consumption= dash_table.DataTable(
    id='stads_id_consumption',
    data=filterByValue('total_energy_consumption', dt.stads_df.copy()).to_dict('records'),
    page_size=10,  # Number of rows per page
    page_current=0,  # Current page
)

USmap = map.USmap(dt.stads_df)
USmapHEX = map.USHexMap(dt.stads_df)


# define the energy_types filter

energy_types_filter = CreateCategoryFilteringTree(dt.energy_categories_types, dt.col_names[0], "Select Energy Type")
energy_types_filter.className = "category-tree"
energy_activity_filter = CreateCategoryFilteringTree(dt.energy_activities, dt.col_names[1], "Select Energy Activity")
energy_activity_filter.className = "category-tree"

consumption_filters = CreateCategoryFilteringTree(dt.consumption,"consumption-filter", "Energy Consumption")
production_filters = CreateCategoryFilteringTree(dt.consumption,"production-filter", "Energy Production")



@app.callback(
    Output('year-slider', 'disabled'),
    Output('year-slider', 'value'),
    Output('year-toggle', 'label'),  # Add an Output for the label
    Input('year-toggle', 'on')
)
def update_slider_state(on):
    label = setLabel(on)  # Calculate the label based on the toggle state
    if on:
        return False, [1960], label  # Return label as a part of the tuple
    else:
        return False, [1960, 2021], label  # Return label as a part of the tuple


def setLabel(on):
    if on:
        return 'Select Year'
    else:
        return 'Select Time Interval'

@app.callback(
    Output('output-state-click', 'children'),
    Input('choropleth-map', 'clickData')
)
def display_clicked_state(clickData):
    if clickData is not None:
        state_code = clickData['points'][0]['hovertext']
        print(f"Clicked state code: {state_code}")
        return f"Clicked state code: {state_code}"
    else:
        return ""

app.layout = html.Div(
    [
        nav,
        html.Div(
            [
                # Energy filters container with flex layout
                html.Div(
                    [consumption_filters, production_filters],
                    style={'display': 'flex', 'flex': '1'}
                ),
                html.Div(
                    [USmap, USmapHEX],
                    style={'display': 'flex', 'flex': '1'}
                ),


            ],
            style={'display': 'flex', 'flex-direction': 'column'},
        ),
        timeSlider,
        data_table_production,
        data_table_consumption,
        footer,
    ],
    style={'display': 'flex', 'flex-direction': 'column'},
)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
