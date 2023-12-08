import numpy as np
import plotly.express as px
import pandas as pd
from helpers.filter import (
    filterData,
    filterByValues,
    get_all_categories_at_same_level,
    get_MSN_code_from_title,
    get_all_children_of_category, get_title_from_MSN_code,
)
from data import data as dt
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
from app import app
import statistics


def calculate_mean_for_US_for(selected_category, selected_years):
    print(f'Selected years {selected_years} ')
    current_data_df = pd.DataFrame(dt.stads_df)
    current_data_df = filterData([selected_category], current_data_df, "MSN")
    current_data_df = filterData(['US'], current_data_df, "StateCode")
    if len(selected_years) == 1:
        single_year = selected_years[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]
        data_value = current_data_df['Data'].iloc[0]
        return data_value / 50

    elif len(selected_years) == 2:
        min_year, max_year = selected_years
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
            ]
        data_values = current_data_df['Data'].tolist()
        return statistics.mean(data_values) / 50


def calculate_relative_value_for(filtered_data, mean_US_val):
    # Check if filtered_data is empty or mean_US_val is None
    if filtered_data.empty:
        print(f'FILTERED DATA IS EMPTY')
        return None
    if mean_US_val is None:
        print('mean_US_val is None')
        return None
    if filtered_data['Data'].isnull().any():
        filtered_data['Data'].fillna(0, inplace=True)

    # Calculate the relative value
    data = filtered_data['Data'].iloc[0]
    print(f' Data value: {data}, mean US value {mean_US_val}')
    relative_value = ((data - mean_US_val) / mean_US_val) * 100
    print(f'Relative data {relative_value}')
    return relative_value


def update_diverging_bar_chart(selected_cat, selected_state, selected_years, is_consumption):
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    children_of_cat = None
    select_Categories = selected_cat
    if selected_cat is not None and selected_cat != []:
        print(f'selected_cat is not none: {selected_cat}')
        children_of_cat = get_all_children_of_category(selected_cat[0], tree)
        print(f'Children of selected cat: {children_of_cat}')
    if children_of_cat != [] and children_of_cat is not None:
        select_Categories = select_Categories + children_of_cat

    current_data_df = filterByValues(select_Categories, current_data_df)
    current_data_df = filterData([selected_state], current_data_df, "StateCode")
    current_data_df = filterByValues(selected_years, current_data_df)

    for category in current_data_df['MSN'].unique():
        mean_US_val = calculate_mean_for_US_for(category, selected_years)
        filtered_data = current_data_df[current_data_df['MSN'] == category]
        relative_values = calculate_relative_value_for(filtered_data, mean_US_val)
        current_data_df.loc[current_data_df['MSN'] == category, 'RelativeData'] = relative_values

    fig = go.Figure()
    # y=current_data_df['MSN'] --> change to to titles and the list of titles
    # Adding the trace for the d
    # iverging bar chart
    fig.add_trace(
        go.Bar(
            x=current_data_df['RelativeData'],
            y=current_data_df['energy_type'],  # Assuming 'MSN' column has the categories
            orientation="h",
            marker=dict(color=current_data_df['RelativeData'].apply(lambda x: 'blue' if x >= 0 else 'red')),
            hovertemplate="Category: %{y}<br>Year: " + str(selected_years) + "<br>Relative Value: %{x}<extra></extra>",
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
        xaxis=dict(
            title='Relative Data (%)',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        yaxis=dict(
            title='Category'
        )
    )

    # Centering the diverging bars
    max_abs_value = current_data_df['RelativeData'].abs().max()
    fig.update_xaxes(range=[-max_abs_value, max_abs_value])

    return fig


@app.callback(
    Output("diverging-bar-chart-consumption", "figure"),
    [
        Input("selected_category_overview_con", "data"),
        Input("selected_states_con", "data"),
        Input("selected_years_con", "data"),

    ],
    prevent_initial_call=True
)
def update_diverging_bar_chart_cons(selected_category, selected_state, selected_year):
    return update_diverging_bar_chart(selected_category, selected_state, selected_year, True)


@app.callback(
    Output("diverging-bar-chart-production", "figure"),
    [
        Input("selected_category_overview_pro", "data"),
        Input("selected_states_pro", "data"),
        Input("selected_years_pro", "data"),
    ],
    prevent_initial_call=True
)
def update_diverging_bar_chart_prod(selected_category, selected_state, selected_year):
    return update_diverging_bar_chart(selected_category, selected_state, selected_year, False)


@app.callback(
    Output("stacked-area-chart-consumption", "figure"),
    [
        Input("selected_category_overview_con", "data"),
        Input("selected_years_con", "data"),
        Input("selected_states_con", "data"),
    ],
    prevent_initial_call=True
)
def updateStackedEnergyChart_percentage_consumption(selected_cat, selected_years, selected_state):
    return updateStackedEnergyChart_percentage(selected_cat, selected_years, selected_state, True)


@app.callback(

    Output("stacked-area-chart-production", "figure"),
    [
        Input("selected_category_overview_pro", "data"),
        Input("selected_years_pro", "data"),
        Input("selected_states_pro", "data"),
    ],
    prevent_initial_call=True
)
def updateStackedEnergyChart_percentage_production(selected_cat, selected_years, selected_state):
    return updateStackedEnergyChart_percentage(selected_cat, selected_years, selected_state, False)


# TODO: fix CATEGORIES FILTERING --> DOES NOT WORK CORRECTLY
# orint when it is called and if it is called on category change!!!
# then see what categories are selected for that bar chart if it correctly takes children
def updateStackedEnergyChart_percentage(selected_cat, selected_years, selected_state, is_consumption):
    print('updateStackedEnergyChart_percentage method called')
    label_addition = 'Consumption' if is_consumption else 'Production'
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    children_of_cat = None
    if selected_cat is not None and selected_cat != []:
        print(f'selected_cat is not none: {selected_cat}')
        children_of_cat = get_all_children_of_category(selected_cat[0], tree)
        print(f'Children of selected cat: {children_of_cat}')
    if children_of_cat != [] and children_of_cat is not None:
        select_Categories = children_of_cat
    elif children_of_cat is None or children_of_cat == []:
        select_Categories = selected_cat

    state_code = selected_state if not None else states_def
    print(f'updateStackedEnergyChart_percentage: Selected categories : {select_Categories}')

    current_data_df = filterByValues(select_Categories, current_data_df)
    current_data_df = filterData([state_code], current_data_df, "StateCode")

    print(f'State codes:  {state_code}')
    fig = go.Figure()

    # Group by year and calculate sum for each energy type
    grouped_data = current_data_df.groupby(["Year", "MSN"]).sum().reset_index()

    # Initialize an empty DataFrame for cumulative data
    cumulative_sum = pd.DataFrame()

    for energy_type in grouped_data["MSN"].unique():
        # Filter data for the current energy type
        energy_data = grouped_data[grouped_data["MSN"] == energy_type]

        if cumulative_sum.empty:
            # If cumulative_sum is empty, start with the first energy type
            cumulative_sum = energy_data
        else:
            # Merge the energy data with cumulative sum and update the 'Data' column
            cumulative_sum = cumulative_sum.merge(energy_data, on='Year', how='left', suffixes=('', '_new'))
            cumulative_sum['Data'] += cumulative_sum['Data_new'].fillna(0)
            cumulative_sum.drop(columns='Data_new', inplace=True)

        # Add a trace to the figure for the current cumulative sum
        fig.add_trace(
            go.Scatter(
                x=cumulative_sum["Year"],
                y=cumulative_sum["Data"],
                fill="tonexty",
                mode="none",
                name=energy_type,
            )
        )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Data",
        title=f"{label_addition} Energy Data Over Time in Whole {dt.get_state_name(state_code)}",
    )

    if len(selected_years) == 1:
        fig.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=selected_years[0],
                    x1=selected_years[0],
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="grey", width=2),
                )
            ]
        )
        return fig

    min_year, max_year = min(selected_years), max(selected_years)
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


def get_current_data(data_to_update):
    if data_to_update:
        current_data_df = pd.DataFrame(data_to_update)
    else:
        current_data_df = pd.DataFrame(dt.stads_df)
    return current_data_df


def get_unfiltered_years_cats_states(is_consumption):
    if is_consumption:
        return [2021], ['TETCB'], 'US'
    else:
        return [2021], ['TEPRB'], 'US'


# CALLBACK FOR DATA FILTERING FOR OVERVIEW (MAP)
def update_overview_data_storage(current_selected_category, current_selected_state, selected_cat, time_range,
                                 click_data_map, is_consumption):
    current_data_df_overview = pd.DataFrame(dt.stads_df)
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)
    tree = dt.consumption if is_consumption else dt.production
    if not selected_cat and not time_range and not click_data_map:
        return current_data_df_overview.to_dict("records"), years_def, cats_def, states_def

    if selected_cat:
        select_Category = get_MSN_code_from_title(selected_cat["points"][0]["label"], tree)

        print(f'Cat was selected, update_overview_data_storage: Selected category: {select_Category}')
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

    current_data_df_overview = filterByValues(select_Category, current_data_df_overview)
    current_data_df_overview = filterData([state_code], current_data_df_overview, "StateCode")

    if current_data_df_overview.empty:
        return dt.stads_df.to_dict("records"), time_range, select_Category, state_code

    print(f'Selected category from the filtering overview {select_Category}')
    return current_data_df_overview.to_dict("records"), time_range, select_Category, state_code


@app.callback(
    [
        Output("consumption_overview_data_storage", "data"),
        Output("selected_years_con", "data"),
        Output("selected_category_overview_con", "data"),
        Output("selected_states_con", "data"),
    ],
    [
        State("selected_category_overview_con", "data"),
        State("selected_states_con", "data"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
    ], prevent_initial_call=True)
def update_consumption_overview_data_storage(current_selected_category, current_selected_state,
                                             selected_consumption, time_range, click_data_consumption_map):
    return update_overview_data_storage(current_selected_category, current_selected_state,
                                        selected_consumption, time_range, click_data_consumption_map, True)


@app.callback(
    [
        Output("production_overview_data_storage", "data"),
        Output("selected_years_pro", "data"),
        Output("selected_category_overview_pro", "data"),
        Output("selected_states_pro", "data")
    ],
    [
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ], prevent_initial_call=True)
def update_production_overview_data_storage(current_selected_category, current_selected_state,
                                            selected_production, time_range, click_data_production_map):
    return update_overview_data_storage(current_selected_category, current_selected_state,
                                        selected_production,
                                        time_range, click_data_production_map, False)


# CALLBACK FOE DETAILED DAATA STORAGE FOR CONSUMPTION
@app.callback(
    Output("consumption_detailed_data_storage", "data"),
    [
        State("selected_category_overview_con", "data"),
        State("selected_states_con", "data"),
        Input("icicle-plot-consumption", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-consumption", "clickData"),
    ],
    prevent_initial_call=True)
def update_consumption_detailed_data_storage(current_selected_category,
                                             current_selected_state, selected_consumption,
                                             time_range, click_data_consumption_map):
    return update_detailed_data_storage(current_selected_category,
                                        current_selected_state,
                                        selected_consumption, time_range,
                                        click_data_consumption_map, True)


@app.callback(
    Output("production_detailed_data_storage", "data"),
    [
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ],
    prevent_initial_call=True)
def update_production_detailed_data_storage(current_selected_category,
                                            current_selected_state,
                                            selected_production, time_range, click_data_production_map):
    return update_detailed_data_storage(current_selected_category,
                                        current_selected_state,
                                        selected_production, time_range,
                                        click_data_production_map, False)


def update_detailed_data_storage(current_selected_category, current_selected_state,
                                 selected_cat, time_range,
                                 click_data_map, is_consumption):
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    if not selected_cat and not time_range and not click_data_map:
        return current_data_df.to_dict("records")

    children_of_cat = None
    if selected_cat:
        children_of_cat = get_all_children_of_category(selected_cat["points"][0]["label"], tree)
        print(children_of_cat)
    if children_of_cat is not None:
        select_Category = children_of_cat
    elif children_of_cat is None:
        select_Category = current_selected_category

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

    current_data_df = filterByValues(select_Category, current_data_df)
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


@app.callback(
    [
        Output("data_for_map_con", "data"),
        Output("consumption-map-switch", "label")
    ],
    Input("consumption-map-switch", "on"),
)
def update_map_switch(on):
    if on:
        return 'EnergyPerGDP', "Consumption per GDP"
    else:
        return 'EnergyPerCapita', "Consumption per Capita"


def update_map(clickData, selected_category, selected_years, is_selected_state, columnNameData_to_use="Data"):
    geoData = dt.geoData
    tree = dt.consumption if columnNameData_to_use != "Data" else dt.production
    title_cat = get_title_from_MSN_code(selected_category[0], tree)
    print(f'Title category {title_cat}, column data to use: {columnNameData_to_use}')
    ##FILTERING
    current = pd.DataFrame(dt.stads_df)
    current = filterData(selected_category, current, "MSN")
    current = filterData(selected_years, current, "Year")



    merged_data = geoData.merge(current, left_on="iso3166_2", right_on='StateCode')
    merged_data["centroid"] = merged_data["geometry"].apply(lambda x: x.centroid)

    merged_data['hover_text'] = merged_data.apply(lambda row: f"State Code: {row['StateCode']}\n"
                                                              f"\nFull State Name: {row['full_state_code']}\n"
                                                              f"\n{title_cat[0]}: {row[columnNameData_to_use]} BTU",
                                                  axis=1)

    annotations_trace = go.Scattermapbox(
        lon=merged_data["centroid"].apply(lambda x: x.x),
        lat=merged_data["centroid"].apply(lambda x: x.y),
        mode="text",
        text=merged_data["StateCode"],
        textposition="middle center",
        showlegend=False,
        textfont=dict(size=10, color="black"),
        hoverinfo="text",
        hovertext=merged_data["hover_text"],
    )

    if is_selected_state:
        # Draw the map using plotly express
        fig = px.choropleth_mapbox(
            merged_data,
            geojson=merged_data.geometry,
            locations=merged_data.index,
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
        if "points" in clickData:
            selected_state = clickData["points"][0]["text"]
            print("Selected State:", selected_state)

            # Update the opacity for the selected hexagon
            fig.update_traces(
                marker=dict(
                    opacity=[
                        1.0 if state_code == selected_state else 0.3
                        for state_code in merged_data["StateCode"]
                    ],
                ),
            )
    else:
        min_range, max_range = merged_data[columnNameData_to_use].min(), merged_data[columnNameData_to_use].max()
        print(f'min: {min_range} max: {max_range}')
        fig = px.choropleth_mapbox(
            merged_data,
            geojson=merged_data.geometry,
            locations=merged_data.index,
            mapbox_style="white-bg",
            color=columnNameData_to_use,
            range_color=(min_range, max_range),
            color_continuous_scale='Viridis',
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
    return fig


@app.callback(
    Output("is_selected_category_con", "data"),
    [
        State("is_selected_category_con", "data"),
        State("selected_category_overview_con", "data"),
        Input("icicle-plot-consumption", "clickData"),
    ]
)
def update_is_selected_cat_info_con(is_selected_cat, current_selected_cat, click_icicle):
    return update_is_selected_category_info(is_selected_cat, current_selected_cat, click_icicle)


@app.callback(
    Output("is_selected_category_pro", "data"),
    [
        State("is_selected_category_pro", "data"),
        State("selected_category_overview_pro", "data"),
        Input("icicle-plot-production", "clickData"),
    ]
)
def update_is_selected_cat_info_pro(is_selected_cat, current_selected_cat, click_icicle):
    return update_is_selected_category_info(is_selected_cat, current_selected_cat, click_icicle)


def update_is_selected_category_info(is_selected_cat, current_selected_cat, click_icicle):
    if is_selected_cat or click_icicle:
        print(f'Category was selected')
        clicked_the_same_cat = True if current_selected_cat == click_icicle["points"][0]["label"] else False
        print(f'Was the same cat selected?: {clicked_the_same_cat}')
        return not clicked_the_same_cat
    return False


@app.callback(
    Output("is_selected_state_con", "data"),
    [
        State("is_selected_state_con", "data"),
        State("selected_states_con", "data"),
        Input("choropleth-map-consumption", "clickData"),
    ]
)
def update_is_selected_map_info_con(is_selected_state, current_selected_state, click_map):
    print('update_is_selected_map_info_con was called')
    return update_is_selected_map_info(is_selected_state, current_selected_state, click_map)


@app.callback(
    Output("is_selected_state_pro", "data"),
    [
        State("is_selected_state_pro", "data"),
        State("selected_states_pro", "data"),
        Input("choropleth-map-production", "clickData"),
    ]
)
def update_is_selected_map_info_pro(is_selected_state, current_selected_state, click_map):
    return update_is_selected_map_info(is_selected_state, current_selected_state, click_map)


def update_is_selected_map_info(is_selected_state, current_selected_state, click_map):
    if is_selected_state or click_map:
        print('State was selected!')
        clicked_the_same_state = True if current_selected_state == click_map["points"][0]["text"] else False
        print(f'Was the same state selected?: {clicked_the_same_state}')
        return not clicked_the_same_state
    return False


@app.callback(
    Output("choropleth-map-consumption", "figure"),
    [
        Input("choropleth-map-consumption", "clickData"),
        Input("selected_category_overview_con", "data"),
        Input("selected_years_con", "data"),
        Input("is_selected_state_con", "data"),
        Input("data_for_map_con", "data"),
    ]
)
def update_map_consumption(clickData, selected_category, selected_years, is_selected_state, data_to_use):
    return update_map(clickData, selected_category, selected_years, is_selected_state, data_to_use)


@app.callback(
    Output("choropleth-map-production", "figure"),
    [
        Input("choropleth-map-production", "clickData"),
        Input("selected_category_overview_pro", "data"),
        Input("selected_years_pro", "data"),
        Input("is_selected_state_pro", "data")

    ]
)
def update_map_production(clickData, selected_category, selected_years, is_selected_state_pro):
    return update_map(clickData, selected_category, selected_years, is_selected_state_pro)


def toggle_visibility_consumption_production(multiStateSwitchValue):
    if multiStateSwitchValue == 'display_consumption':
        return {"flex": "0", "display": "flex"}, {"flex": "0", "display": "none"}
    if multiStateSwitchValue == 'display_production':
        return {"flex": "0", "display": "none"}, {"flex": "0", "display": "flex"}
    if multiStateSwitchValue == 'display_both':
        return {"flex": "0", "display": "flex"}, {"flex": "0", "display": "flex"}


###############
@app.callback(
    Output("diverging-bar-chart-consumption", "style"),
    [

        Input("is_selected_state_con", "data"),
        Input("is_selected_category_con", "data"),
    ]
)
def show_diverging_plot_consumption(is_selected_state_con, is_selected_cat_con):
    return show_component_when_category_and_state_selected(is_selected_state_con, is_selected_cat_con)


@app.callback(
    Output("diverging-bar-chart-production", "style"),
    [

        Input("is_selected_state_pro", "data"),
        Input("is_selected_category_pro", "data"),
    ]
)
def show_diverging_plot_consumption(is_selected_state_pro, is_selected_cat_pro):
    return show_component_when_category_and_state_selected(is_selected_state_pro, is_selected_cat_pro)


##########################
@app.callback(
    Output("stacked-area-chart-consumption", "style"),
    [

        Input("is_selected_state_con", "data"),
        Input("is_selected_category_con", "data"),
    ]
)
def show_stacked_plot_consumption(is_selected_state_con, is_selected_cat_con):
    return show_component_when_category_and_state_selected(is_selected_state_con, is_selected_cat_con)


@app.callback(
    Output("stacked-area-chart-production", "style"),
    [

        Input("is_selected_state_pro", "data"),
        Input("is_selected_category_pro", "data"),
    ]
)
def show_stacked_plot_production(is_selected_state_pro, is_selected_cat_pro):
    return show_component_when_category_and_state_selected(is_selected_state_pro, is_selected_cat_pro)


def show_component_when_category_and_state_selected(clicked_map, clicked_icicle_plot):
    if clicked_map and clicked_icicle_plot:
        print('Its time to show diverging plot')
        return {"display": "inline"}
    else:
        return {"display": "none"}


@app.callback(
    [
        Output("choropleth-map-consumption", "style"),
        Output("choropleth-map-production", "style"),
    ],
    Input("multi-state-switch", "value"),
)
def toggle_consumption_map_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)


@app.callback(
    [
        Output("icicle-plot-consumption", "style"),
        Output("icicle-plot-production", "style")
    ],
    Input("multi-state-switch", "value"),
)
def toggle_icicle_plot_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)
