# Import packages
from dash import Dash, html, dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from components import navbar, footer, timeSlider, map, stackAreaChart
import feffery_antd_components as fac
import pandas as pd
from dash import Input, Output
from helpers.filter import (
    filterData,
    filterByValues,
    get_all_categories_at_same_level,
    get_all_children_of_category, filter_dataframe_by_tree
)
from data import data as dt
import plotly.graph_objects as go


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


@app.callback(
    Output("stads_id", "data"),
    Input("production-filter", "value"),
    Input("consumption-filter", "value"),
    Input("year-slider", "value"),
    Input("choropleth-map", "clickData"),
    prevent_initial_call=True,
)

def handle_select_event(selected_production, selected_consumption, time_range, click_data):
    current_data_df = pd.DataFrame(dt.stads_df.copy())  # Convert the data to a DataFrame

    if not selected_production and not selected_consumption and not time_range and not click_data:
        return current_data_df.to_dict(
            "records"
        )  # No filters selected, return the current data as is


    if selected_production:
        current_data_df = filter_dataframe_by_tree(dt.production, current_data_df)
        current_data_df = filterByValues(selected_production, current_data_df)

    elif selected_consumption:
        current_data_df = filter_dataframe_by_tree(dt.consumption, current_data_df)
        current_data_df = filterByValues(selected_consumption, current_data_df)

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]
        if not current_data_df.empty:
            return current_data_df.to_dict("records")
        else:
            return ["No data selected"]

    if time_range and len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        filtered_data_copy = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
        ]
        filtered_data = filtered_data_copy

    if click_data:
        print("Map was clicked")
        state_code = click_data["points"][0]["location"]
        print(f"Clicked state {state_code}")
        current_data_df = current_data_df([state_code], current_data_df, "StateCode")


    return current_data_df.to_dict("records")


# TODO: Move to sepatate file?
def CreateCategoryFilteringTree(categories, id, placeHolder):
    antd_tree_select = fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
    )

    return antd_tree_select


# define the navbar and footer
nav = navbar.Navbar()
footer = footer.Footer()
timeSlider = timeSlider.TimeSlider()
stackChart = stackAreaChart.StackAreaChart()

data_table = html.Div(dash_table.DataTable(
    id="stads_id",
    data=dt.stads_df.copy().to_dict("records"),
    page_size=10,  # Number of rows per page
    page_current=0,  # Current page
),className="pretty_container")



USmap = map.USmap(dt.stads_df)
USmapHEX = map.USHexMap(dt.stads_df)
stackChart = stackAreaChart.StackAreaChart()


consumption_filters = CreateCategoryFilteringTree(
    dt.consumption, "consumption-filter", "Energy Consumption"
)
production_filters = CreateCategoryFilteringTree(
    dt.consumption, "production-filter", "Energy Production"
)


@app.callback(
    Output("energy-chart", "figure"),
    Input("production-filter", "value"),
    Input("consumption-filter", "value"),
    Input("year-slider", "value"),
    Input("choropleth-map", "clickData"),
)
def update_energy_chart(
    selected_production_categories,
    selected_consumption_categories,
    time_range,
    click_data,
):
    state_code = "US"
    data_to_show = pd.DataFrame(dt.stads_df)
    selected_categories = []

    # should we take the children or on the same level?
    if selected_production_categories:
        data_to_show = filter_dataframe_by_tree(dt.production, data_to_show)
        selected_categories = get_all_categories_at_same_level(
            selected_production_categories[0], dt.production
        )
        print(selected_production_categories)
        print(f"Get all on the same level: {selected_categories}")
        data_to_show = filterByValues(selected_categories, data_to_show)

    elif selected_consumption_categories:
        data_to_show = filter_dataframe_by_tree(dt.consumption, data_to_show)
        selected_categories = get_all_categories_at_same_level(
            selected_consumption_categories[0], dt.consumption
        )
        data_to_show = filterByValues(selected_categories, data_to_show)

    if click_data:
        state_code = click_data["points"][0]["location"]
        data_to_show = filterData([state_code], data_to_show, "StateCode")

    fig = go.Figure()

    for energy_type in data_to_show["energy_type"].unique():
        energy_type_data = data_to_show[data_to_show["energy_type"] == energy_type]
        fig.add_trace(
            go.Scatter(
                x=energy_type_data["Year"],
                y=energy_type_data["Data"],
                fill="tonexty",
                mode="none",
                name=energy_type,
            )
        )

    fig = go.Figure()
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Data",
        title=f"Energy Data Over Time in {state_code}",
    )

    if not time_range:
        return fig

    # if a single year is selected, then we have a vertical line on the stacked area chart
    # that highlight that year
    if len(time_range) == 1:
        fig.update_layout()
    # if two years are selected, then we have two vertical lines that create and the area
    # in the middle is highlighted

    if time_range and len(time_range) == 2:
        return fig.update_layout()

    return fig


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


@app.callback(
    Output("output-state-click", "children"), Input("choropleth-map", "clickData")
)
def display_clicked_state(clickData):
    if clickData is not None:
        state_code = clickData["points"][0]["hovertext"]
        print(f"Clicked state code: {state_code}")
        return f"Clicked state code: {state_code}"
    else:
        return ""


energy_filters = html.Div(
    [
        # Energy filters container with flex layout
        html.Div(
            [consumption_filters, production_filters],
            style={"display": "flex", "flex": "1"},
        )
    ],
    style={"display": "flex", "flex-direction": "column"},
    className="pretty_container",
)

app.layout = html.Div(
    [
        nav,
        energy_filters,
        USmap,
        timeSlider,
        data_table,
        stackChart,
        footer,
    ],
    style={"display": "flex", "flex-direction": "column"},
)

print(get_all_categories_at_same_level("coal", dt.production))
print(get_all_children_of_category("renewable energy", dt.production))
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
