import plotly.express as px
import pandas as pd
from helpers.filter import (
    filterData,
    filterByValues,
    get_all_categories_at_same_level,
    get_all_children_of_category,
)
from data import data as dt
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
import geopandas as gpd
from app import app


@app.callback(
    Output("category-toggle", "label"),
    Input("category-toggle", "on"),
)
def setLabel_categories_switch(on):
    if on:
        return "Combined Analysis"
    else:
        return "Separate Analysis"


@app.callback(
    Output("stacked-area-chart", "figure"),
    [
        Input("icicle-plot-production", "clickData"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
    ],
)
def updateStackedEnergyChart_percentage(
    clicked_icicle_plot_production,
    clicked_icicle_plot_consumption,
    time_range,
    click_data,
):
    state_code = "US"
    data_to_show = pd.DataFrame(dt.stads_df)
    selected_categories = [
        get_all_children_of_category("total_energy_consumption", dt.consumption)
    ]

    # should we take the children or on the same level?
    if clicked_icicle_plot_production:
        _, selected_categories = get_all_categories_at_same_level(
            clicked_icicle_plot_production["points"][0]["label"], dt.production
        )

        data_to_show = filterByValues(selected_categories, data_to_show)

    elif clicked_icicle_plot_consumption:
        _, selected_categories = get_all_categories_at_same_level(
            clicked_icicle_plot_consumption["points"][0]["label"], dt.consumption
        )
        data_to_show = filterByValues(selected_categories, data_to_show)

    if click_data:
        state_code = click_data["points"][0]["text"]
        data_to_show = filterData([state_code], data_to_show, "StateCode")

    fig = go.Figure()

    # Group by year and calculate sum for each energy type
    grouped_data = data_to_show.groupby(["Year", "energy_type"]).sum().reset_index()

    # Initialize an empty DataFrame for cumulative data
    cumulative_data = pd.DataFrame()

    for energy_type in grouped_data["energy_type"].unique():
        # Filter data for the current energy type
        energy_data = grouped_data[grouped_data["energy_type"] == energy_type]

        if cumulative_data.empty:
            # If cumulative_data is empty, start with the first energy type
            cumulative_data = energy_data
        else:
            for year in energy_data["Year"].unique():
                cumulative_data.loc[
                    cumulative_data["Year"] == year, "Data"
                ] += energy_data.loc[energy_data["Year"] == year, "Data"].values[0]

        # Add a trace to the figure
        fig.add_trace(
            go.Scatter(
                x=cumulative_data["Year"],
                y=cumulative_data["Data"],
                fill="tonexty",
                mode="none",
                name=energy_type,
            )
        )

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
        selected_year = time_range[0]
        fig.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=selected_year,
                    x1=selected_year,
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="grey", width=2),
                )
            ]
        )
        return fig

    # if two years are selected, then we have two vertical lines that create and the area
    # in the middle is highlighted

    if len(time_range) == 2:
        min_year, max_year = time_range
        fig.update_layout(
            shapes=[
                dict(
                    type="rect",
                    x0=min_year,
                    x1=max_year,
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    fillcolor="rgba(0,100,80,0.2)",  # Set the fill color for the selected interval
                    line=dict(width=0),
                )
            ]
        )
        return fig

    return fig


@app.callback(
    Output("stads_id", "data"),
    [
        Input("icicle-plot-production", "clickData"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
        Input("choropleth-map-production", "clickData"),
    ],
    prevent_initial_call=True,
)
def handle_select_event(
    selected_production,
    selected_consumption,
    time_range,
    click_data_consumption,
    click_data_production,
):
    current_data_df = pd.DataFrame(
        dt.stads_df.copy()
    )  # Convert the data to a DataFrame

    if (
        not selected_production
        and not selected_consumption
        and not time_range
        and not click_data_consumption
        and not click_data_production
    ):
        return current_data_df.to_dict(
            "records"
        )  # No filters selected, return the current data as is

    if selected_production:
        select_Category = selected_production["points"][0]["label"]
        current_data_df = filterByValues([select_Category], current_data_df)

        if click_data_production:
            print("Map was clicked")
            state_code = click_data_production["points"][0]["text"]
            print(f"Clicked state {state_code}")
            current_data_df = filterData([state_code], current_data_df, "StateCode")

    elif selected_consumption:
        select_Category = selected_consumption["points"][0]["label"]
        current_data_df = filterByValues([select_Category], current_data_df)

        if click_data_consumption:
            print("Map was clicked")
            state_code = click_data_consumption["points"][0]["text"]
            print(f"Clicked state {state_code}")
            current_data_df = filterData([state_code], current_data_df, "StateCode")

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]

    if time_range and len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
        ]

    if current_data_df.empty:
        return dt.stads_df.to_dict("records")

    return current_data_df.to_dict("records")


#
# @app.callback(
#     Output("consumption-filter", "value"),
#     [Input("production-filter", "value"),
#      Input("category-toggle", "on")],
#     [State("consumption-filter", "value")]
# )
# def clear_consumption_filter(selected_production, toggle_on, current_consumption_value):
#     # If production filter is selected, clear the consumption filter
#     if not toggle_on and selected_production:
#         return []
#
#     return current_consumption_value


# @app.callback(
#     Output("production-filter", "value"),
#     [Input("consumption-filter", "value"),
#      Input("category-toggle", "on")],
#     [State("production-filter", "value")]
# )
# def clear_production_filter(selected_consumption, toggle_on, current_production_value):
#     # If consumption filter is selected, clear the production filter
#     if not toggle_on and selected_consumption:
#         return []
#
#     return current_production_value
#
#


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
    [
        Output("icicle-plot-production", "style"),
        Output("icicle-plot-consumption", "style"),
    ],
    Input("category-toggle", "on"),
)
def toggle_icicle_plot_visibility(toggle_state):
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


# TODO: Store data in data folder
# Load GeoDataFrame
url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/us_states_hexgrid.geojson.json"
geoData = gpd.read_file(url)
geoData["centroid"] = geoData["geometry"].apply(lambda x: x.centroid)


@app.callback(
    Output("choropleth-map-consumption", "figure"),
    Input("choropleth-map-consumption", "clickData"),
)
def update_map(clickData):
    # Create a Scattermapbox trace for annotations
    annotations_trace = go.Scattermapbox(
        lon=geoData["centroid"].apply(lambda x: x.x),
        lat=geoData["centroid"].apply(lambda x: x.y),
        mode="text",
        text=geoData["iso3166_2"],
        textposition="middle center",
        showlegend=False,
        textfont=dict(size=10, color="black"),
        hoverinfo="text",
        hovertext=geoData["google_name"],
    )

    # Draw the map using plotly express
    fig = px.choropleth_mapbox(
        geoData,
        geojson=geoData.geometry,
        locations=geoData.index,
        mapbox_style="white-bg",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=2.5,
    )

    # Update the map layout
    fig.update_geos(
        fitbounds="locations",  # Adjust the bounds to fit the locations
        visible=False,  # Hide the real map
    )

    # Add the annotations trace to the figure
    fig.add_trace(annotations_trace)

    # Highlight the selected hexagon
    if clickData and "points" in clickData:
        selected_state = clickData["points"][0]["text"]
        print("Selected State:", selected_state)

        # Update the opacity for the selected hexagon
        fig.update_traces(
            marker=dict(
                opacity=[
                    1.0 if state_code == selected_state else 0.3
                    for state_code in geoData["iso3166_2"]
                ],
            ),
        )

    # Update the layout of the entire figure
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig


@app.callback(
    Output("choropleth-map-production", "figure"),
    Input("choropleth-map-production", "clickData"),
)
def update_map_production(clickData):
    # Create a Scattermapbox trace for annotations
    annotations_trace = go.Scattermapbox(
        lon=geoData["centroid"].apply(lambda x: x.x),
        lat=geoData["centroid"].apply(lambda x: x.y),
        mode="text",
        text=geoData["iso3166_2"],
        textposition="middle center",
        showlegend=False,
        textfont=dict(size=10, color="black"),
        hoverinfo="text",
        hovertext=geoData["google_name"],
    )

    # Draw the map using plotly express
    fig = px.choropleth_mapbox(
        geoData,
        geojson=geoData.geometry,
        locations=geoData.index,
        mapbox_style="white-bg",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=2.5,
    )

    # Update the map layout
    fig.update_geos(
        fitbounds="locations",  # Adjust the bounds to fit the locations
        visible=False,  # Hide the real map
    )

    # Add the annotations trace to the figure
    fig.add_trace(annotations_trace)
    # Update the layout of the entire figure
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Highlight the selected hexagon
    if clickData and "points" in clickData:
        selected_state = clickData["points"][0]["text"]
        print("Selected State:", selected_state)

        # Update the opacity for the selected hexagon
        fig.update_traces(
            marker=dict(
                opacity=[
                    1.0 if state_code == selected_state else 0.3
                    for state_code in geoData["iso3166_2"]
                ],
            ),
        )

    return fig


@app.callback(
    [
        Output("consumption-map-container", "style"),
        Output("conditional-map-container", "style"),
    ],
    Input("category-toggle", "on"),
)
def toggle_consumption_map_visibility(toggle_state):
    if not toggle_state:
        return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "none"}

    return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "flex"}


# SUNBURST?
"""
@app.callback(
    Output("sun-chart", "figure"),
    [Input("year-slider", "value"),
     Input("choropleth-map-consumption", "clickData")])
def sun_energy_chart(time_range, click_data):
    state_code = "US"
    current_data_df = pd.DataFrame(dt.stads_df)

    if click_data:
        state_code = click_data["points"][0]["text"]
        print(f"Location was clicked {state_code}")
        current_data_df = filterData([state_code], current_data_df, "StateCode")

    # Handle when the checkbox is selected, and the range is empty, but a single year is selected
    if len(time_range) == 1:
        print(f"Single date selected {time_range[0]}")
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]

        fig = px.sunburst(
            current_data_df,
            path=["energy_type", "energy_activity"],
            values="Data",
            hover_data=["Data"],
            color_continuous_scale="RdBu",
            # color_continuous_midpoint=np.average(df["lifeExp"], weights=df[""]),
        )

    elif time_range and len(time_range) == 2:
        min_year, max_year = int(time_range[0]), int(time_range[1])

        # Filter data based on the time range
        current_data_df = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
            ]

        # Calculate the sum of Data over the time range for each category
        sum_data_df = current_data_df.groupby(["total_energy_consumption"])["Data"].sum().reset_index()

        # Create the sunburst plot using the calculated sum_data_df
        fig = px.sunburst(
            sum_data_df,
            path=["energy_type", "energy_activity"],
            values="Data",
            hover_data=["MSN"],
            color_continuous_scale="RdBu",
            # color_continuous_midpoint=np.average(df["lifeExp"], weights=df[""]),
        )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

"""
