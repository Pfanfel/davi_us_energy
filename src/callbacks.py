import numpy as np
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
from app import app


# TODO: FOR KIDS CATEGORIES OR WHAT
def update_diverging_bar_chart(data_production, data_consumption, selected_category):
    filtered_data_production = pd.DataFrame(data_production)
    filtered_data_consumption = pd.DataFrame(data_consumption)
    # state_code = current_data_df['StateCode'].unique()[0]
    # time_range = current_data_df['Year'].unique()
    #
    # calc_avg = dt.calculate_avg_value(
    #     current_data_df, state_code, time_range, selected_category
    # )
    # print(f"the calc_avg: {calc_avg}")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=-filtered_data_production["energy_types"].values,
            y=filtered_data_production["Year"],
            orientation="h",
            name="Production",
            customdata=filtered_data_production["energy_types"],
            hovertemplate="Year: %{y}<br>Pop:%{customdata}<br>Production:energy_types<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=filtered_data_consumption["energy_types"].values,
            y=filtered_data_consumption["Year"],
            orientation="h",
            name="Consumption",
            hovertemplate="Year: %{y}<br>Pop:%{x}<br>Consumption:energy_types<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="relative",
        height=400,
        width=700,
        yaxis_autorange="reversed",
        bargap=0.01,
        legend_orientation="h",
        legend_x=-0.05,
        legend_y=1.1,
    )

    return fig


@app.callback(
    Output("diverging-bar-chart", "figure"),
    [Input("production_detailed_data_storage", "data"),
     Input("consumption_detailed_data_storage", "data"),
     State("selected_category_overview_prod", "data"),
     State("selected_category_overview_con", "data")
     ],
    prevent_initial_call=True
)
def update_diverging_bar_chart_prod_cons(filtered_data_prod, filtered_data_cons, selected_category_prod, selected_category_con):
    return update_diverging_bar_chart(filtered_data_prod, filtered_data_cons, selected_category[0])


# @app.callback(
#     Output("diverging-bar-chart_production", "figure"),
#     [Input("production_detailed_data_storage", "data"),
#      State("selected_category_overview", "data")]
# )
# def update_diverging_bar_chart_production(filtered_data, selected_category):
#     return update_diverging_bar_chart(filtered_data, selected_category[0])

# DETAILED PLOT -> FIXED
@app.callback(
    Output("stacked-area-chart-consumption", "figure"),
    Input("consumption_detailed_data_storage", "data"),
    State("selected_category_overview_con", "data"),
    prevent_initial_call=True
)
def updateStackedEnergyChart_percentage_consumption(filtered_data, selected_category):
    return updateStackedEnergyChart_percentage(filtered_data, selected_category, dt.consumption)


@app.callback(
    Output("stacked-area-chart-production", "figure"),
    Input("production_detailed_data_storage", "data"),
    State('selected_category_overview_pro', 'data'),
    prevent_initial_call=True
)
def updateStackedEnergyChart_percentage_production(filtered_data, selected_category):
    return updateStackedEnergyChart_percentage(filtered_data, selected_category, dt.production)


def updateStackedEnergyChart_percentage(filtered_data, selected_category, tree):
    print('updateStackedEnergyChart_percentage method called')
    data_to_show = pd.DataFrame(filtered_data)
    state_code = data_to_show["StateCode"].unique()
    print(f'State codes:  {state_code}')
    years = data_to_show["Year"].unique()
    print(f'Years:  {years}')
    categories_energy_type = data_to_show["energy_type"].unique()
    print(f'categories_energy_type in data {categories_energy_type}')
    categories_energy_activity = data_to_show["energy_activity"].unique()
    print(f'categories_energy_activity in data {categories_energy_activity}')

    fig = go.Figure()

    selected_categories = [get_all_children_of_category(selected_category, tree)]
    # Group by year and calculate sum for each energy type
    grouped_data = data_to_show.groupby(["Year", selected_categories]).sum().reset_index()

    # Initialize an empty DataFrame for cumulative data
    cumulative_data = pd.DataFrame()

    for category in selected_categories:
        # Filter data for the current energy type
        energy_data = grouped_data[grouped_data["energy_type"] == category]

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
                name=category,
            )
        )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Data",
        title=f"Energy Data Over Time in {state_code}",
    )

    unique_years = data_to_show["Year"].unique()
    if len(unique_years) == 1:
        fig.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=unique_years[0],
                    x1=unique_years[0],
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="grey", width=2),
                )
            ]
        )
        return fig

    min_year, max_year = min(unique_years), max(unique_years)
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


# CALLBACK FOR DATA FILTEING FOR OVERVIEW (MAP)

@app.callback(
    [
        Output("consumption_overview_data_storage", "data"),
        Output("selected_years_con", "data"),
        Output("selected_category_overview_con", "data"),
        Output("selected_states_con", "data"),
    ],
    [
        State("selected_years_con", "data"),
        State("selected_category_overview_con", "data"),
        State("selected_states_con", "data"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
    ], prevent_initial_call=True)
def update_consumption_overview_data_storage(current_selected_years, current_selected_category, current_selected_state,
                                             selected_consumption, time_range, click_data_consumption_map):
    return update_overview_data_storage(current_selected_years, current_selected_category, current_selected_state,
                                        selected_consumption, time_range, click_data_consumption_map, True)


@app.callback(
    [
        Output("production_overview_data_storage", "data"),
        Output("selected_years_pro", "data"),
        Output("selected_category_overview_pro", "data"),
        Output("selected_states_pro", "data")
    ],
    [
        State("selected_years_pro", "data"),
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ], prevent_initial_call=True)
def update_production_overview_data_storage(current_selected_years,current_selected_category, current_selected_state,
                                            selected_production, time_range, click_data_production_map):

    return update_overview_data_storage(current_selected_years,current_selected_category, current_selected_state,
                                        selected_production,
                                        time_range, click_data_production_map, False)


def get_current_data(data_to_update):
    if data_to_update:
        current_data_df = pd.DataFrame(data_to_update)
    else:
        current_data_df = pd.DataFrame(dt.stads_df)
    return current_data_df


def get_unfiltered_years_cats_states(is_consumption):
    if is_consumption:
        return [2021], dt.all_consumption, dt.state_codes
    else:
        return [2021], dt.all_production, dt.state_codes



def update_overview_data_storage(current_selected_years, current_selected_category, current_selected_state, selected_cat, time_range, click_data_map, is_consumption):
    current_data_df_overview = pd.DataFrame(dt.stads_df)
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    if not selected_cat and not time_range and not click_data_map:
        return current_data_df_overview.to_dict("records"), years_def, cats_def, states_def

    if selected_cat:
        select_Category = selected_cat["points"][0]["label"]
    else:
        select_Category = current_selected_category if not None else cats_def


    if click_data_map:
        state_code = click_data_map["points"][0]["text"]
    else:
        state_code = current_selected_state if not None else states_def


    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df_overview = current_data_df_overview[current_data_df_overview["Year"] == single_year]

    elif len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df_overview = current_data_df_overview[
            (current_data_df_overview["Year"] >= min_year)
            & (current_data_df_overview["Year"] <= max_year)
            ]

    current_data_df_overview = filterByValues([select_Category], current_data_df_overview)
    current_data_df_overview = filterData([state_code], current_data_df_overview, "StateCode")

    if current_data_df_overview.empty:
        return dt.stads_df.to_dict("records"), time_range, select_Category, state_code

    return current_data_df_overview.to_dict("records"), time_range, select_Category, state_code


# CALLBACK FOE DETAILED DAATA STORAGE FOR CONSUMPTION
@app.callback(
    Output("consumption_detailed_data_storage", "data"),
    [
        State("selected_years_con", "data"),
        State("selected_category_overview_con", "data"),
        State("selected_states_con", "data"),
        State("consumption_detailed_data_storage", "data"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
    ],
    prevent_initial_call=True)
def update_consumption_detailed_data_storage(current_selected_years, current_selected_category,
                                             current_selected_state, current_data_detailed, selected_consumption,
                                             time_range, click_data_consumption_map):
    return update_detailed_data_storage(current_selected_years, current_selected_category,
                                        current_selected_state, current_data_detailed,
                                        selected_consumption, time_range,
                                        click_data_consumption_map, True)


@app.callback(
    Output("production_detailed_data_storage", "data"),
    [
        State("selected_years_pro", "data"),
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        State("production_detailed_data_storage", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ],
    prevent_initial_call=True)
def update_production_detailed_data_storage(current_selected_years, current_selected_category,
                                            current_selected_state,current_data_detailed,
                                            selected_production, time_range, click_data_production_map):

    return update_detailed_data_storage(current_selected_years, current_selected_category,
                                        current_selected_state, current_data_detailed,
                                        selected_production, time_range,
                                        click_data_production_map, False)


def update_detailed_data_storage(current_selected_years, current_selected_category, current_selected_state,
                                 current_data_detailed, selected_cat, time_range,
                                 click_data_map, is_consumption):


    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    if not selected_cat and not time_range and not click_data_map:
        return current_data_df.to_dict("records")

    if selected_cat:

        select_Category = get_all_children_of_category(selected_cat["points"][0]["label"], tree)
    else:
        select_Category = get_all_children_of_category(current_selected_category if not None else cats_def, tree)


    if click_data_map:
        state_code = click_data_map["points"][0]["text"]
    else:
        state_code = current_selected_state if not None else states_def


    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]

    elif len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
            ]

    current_data_df = filterByValues([select_Category], current_data_df)
    current_data_df = filterData([state_code], current_data_df, "StateCode")

    if current_data_df.empty:
        return dt.stads_df.to_dict("records"), time_range, select_Category, state_code

    return current_data_df.to_dict("records"), time_range, select_Category, state_code



@app.callback(
    [
        Output("year-slider", "disabled"),
        Output("year-slider", "value"),
        Output("year-toggle", "label"),
    ],  # Add an Output for the label
    Input("year-toggle", "on"),
)
def update_slider_state(on):
    label = set_label_time_slider(on)  # Calculate the label based on the toggle state
    dt.stads_df["Year"] = pd.to_numeric(dt.stads_df["Year"])
    # calc. the maximum and minimum year in the dataframe
    min_year, max_year = dt.stads_df["Year"].min(), dt.stads_df["Year"].max()
    if on:
        return False, [min_year], label  # Return label as a part of the tuple
    else:
        return False, [min_year, max_year], label  # Return label as a part of the tuple


def set_label_time_slider(on):
    if on:
        return "Select Year"
    else:
        return "Select Time Interval"


# DO NOT NEED TO BE FIXED
@app.callback(
    Output("category-toggle", "label"),
    Input("category-toggle", "on"),
)
def setLabel_categories_switch(on):
    if on:
        return "Combined Analysis"
    else:
        return "Separate Analysis"


def update_map(clickData):
    geoData = dt.geo_data_us_states_hexgrid
    geoData["centroid"] = geoData["geometry"].apply(lambda x: x.centroid)
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
    Output("choropleth-map-consumption", "figure"),
    Input("choropleth-map-consumption", "clickData"),
)
def update_map_consumption(clickData):
    return update_map(clickData)


@app.callback(
    Output("choropleth-map-production", "figure"),
    Input("choropleth-map-production", "clickData"),
)
def update_map_production(clickData):
    return update_map(clickData)


def toggle_visibility_consumption_production(toggle_state):
    if not toggle_state:
        return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "none"}

    return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "flex"}


@app.callback(
    [
        Output("consumption-map-container", "style"),
        Output("conditional-map-container", "style"),
    ],
    Input("category-toggle", "on"),
)
def toggle_consumption_map_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)


@app.callback(
    [
        Output("stacked-area-chart-consumption", "style"),
        Output("stacked-area-chart-production", "style"),
    ],
    Input("category-toggle", "on"),
)
def toggle_stacked_area_charts_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)


@app.callback(
    [
        Output("icicle-plot-consumption", "style"),
        Output("icicle-plot-production", "style")
    ],
    Input("category-toggle", "on"),
)
def toggle_icicle_plot_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)
