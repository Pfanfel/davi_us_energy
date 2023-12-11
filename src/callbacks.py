import numpy as np
import plotly.express as px
import pandas as pd
from helpers.filter import (
    filterData,
    filterByValues,
    get_all_categories_at_same_level,
    get_MSN_code_from_title,
    get_all_children_of_category,
    get_title_from_MSN_code,
)
from data import data as dt
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
from app import app
import statistics


def calculate_mean_for_US_for(selected_category, selected_years):
    print(f"Selected years {selected_years} ")
    current_data_df = pd.DataFrame(dt.stads_df)
    current_data_df = filterData([selected_category], current_data_df, "MSN")
    current_data_df = filterData(["US"], current_data_df, "StateCode")
    if len(selected_years) == 1:
        single_year = selected_years[0]
        single_year = int(single_year)
        current_data_df = current_data_df[current_data_df["Year"] == single_year]
        data_value = current_data_df["Data"].iloc[0]
        return data_value / 50

    elif len(selected_years) == 2:
        min_year, max_year = selected_years
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df = current_data_df[
            (current_data_df["Year"] >= min_year)
            & (current_data_df["Year"] <= max_year)
        ]
        data_values = current_data_df["Data"].tolist()
        return statistics.mean(data_values) / 50


def calculate_relative_value_for(filtered_data, mean_US_val):
    # Check if filtered_data is empty or mean_US_val is None
    if filtered_data.empty:
        print(f"FILTERED DATA IS EMPTY")
        return None
    if mean_US_val is None:
        print("mean_US_val is None")
        return None
    if filtered_data["Data"].isnull().any():
        filtered_data["Data"].fillna(0, inplace=True)

    # Calculate the relative value
    data = filtered_data["Data"].iloc[0]
    print(f" Data value: {data}, mean US value {mean_US_val}")
    relative_value = ((data - mean_US_val) / mean_US_val) * 100
    print(f"Relative data {relative_value}")
    return relative_value


def updateStackedEnergyChart_percentage(
    selected_cat,
    selected_years,
    selected_state,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
    is_consumption,
):
    print("updateStackedEnergyChart_percentage method called")
    label_addition = "Consumption" if is_consumption else "Production"
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    children_of_cat = None
    if selected_cat is not None and selected_cat != []:
        print(f"selected_cat is not none: {selected_cat}")
        children_of_cat = get_all_children_of_category(selected_cat[0], tree)
        print(f"Children of selected cat: {children_of_cat}")
    if children_of_cat != [] and children_of_cat is not None:
        select_Categories = children_of_cat
    elif children_of_cat is None or children_of_cat == []:
        select_Categories = selected_cat

    state_code = selected_state if not None else states_def
    print(
        f"updateStackedEnergyChart_percentage: Selected categories : {select_Categories}"
    )

    current_data_df = filterByValues(select_Categories, current_data_df)
    current_data_df = filterData([state_code], current_data_df, "StateCode")

    print(f"State codes:  {state_code}")
    fig = go.Figure()

    # Group by year and calculate sum for each energy type
    current_data_df["label_text"] = current_data_df.apply(
        lambda row: get_title_from_MSN_code(row["MSN"], tree)[0], axis=1
    )
    grouped_data = current_data_df.groupby(["Year", "label_text"]).sum().reset_index()

    # Initialize an empty DataFrame for cumulative data
    cumulative_sum = pd.DataFrame()

    fig = go.Figure()

    # Determine if any click event has occurred
    clicked = clickDataDifferentPlot is not None or clickDataThisPlot is not None

    for energy_type in grouped_data["label_text"].unique():  # here is different
        energy_data = grouped_data[
            grouped_data["label_text"] == energy_type
        ]  # here is different

        if cumulative_sum.empty:
            cumulative_sum = energy_data
        else:
            cumulative_sum = cumulative_sum.merge(
                energy_data, on="Year", how="left", suffixes=("", "_new")
            )
            cumulative_sum["Data"] += cumulative_sum["Data_new"].fillna(0)
            cumulative_sum.drop(columns="Data_new", inplace=True)

        # Determine if this category should be highlighted
        highlight = (
            any(
                msn_code in selected_msn_codes
                for msn_code in energy_data["MSN"].unique()
            )
            if clicked
            else True
        )

        # Set the fill color based on the highlight status
        fill_color = "rgba(128, 128, 128, 0.3)" if not highlight else None

        fig.add_trace(
            go.Scatter(
                x=cumulative_sum["Year"],
                y=cumulative_sum["Data"],
                customdata=cumulative_sum["MSN"],
                fill="tonexty",
                mode="none",
                name=energy_type,
                fillcolor=fill_color,  # Set the fill color for the trace
            )
        )

    fig.update_layout(
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",  # Sets the grid line color for the x-axis
        ),
        plot_bgcolor="white",  # Sets the plot background to white
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


@app.callback(
    Output("stacked-area-chart-production", "figure"),
    [
        Input("selected_category_overview_pro", "data"),
        Input("selected_years_pro", "data"),
        Input("selected_states_pro", "data"),
        State("diverging-bar-chart-production", "clickData"),
        State("stacked-area-chart-production", "clickData"),
        Input("selected_msn_codes_pro", "data"),
    ],
    prevent_initial_call=True,
)
def update_stacked_energy_chart_percentage_production(
    selected_cat,
    selected_years,
    selected_state,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
):
    return updateStackedEnergyChart_percentage(
        selected_cat,
        selected_years,
        selected_state,
        clickDataDifferentPlot,
        clickDataThisPlot,
        selected_msn_codes,
        False,
    )


@app.callback(
    Output("stacked-area-chart-consumption", "figure"),
    [
        Input("selected_category_overview_con", "data"),
        Input("selected_years_con", "data"),
        Input("selected_states_con", "data"),
        State("stacked-area-chart-consumption", "clickData"),
        State("diverging-bar-chart-consumption", "clickData"),
        Input("selected_msn_codes_con", "data"),
    ],
    prevent_initial_call=True,
)
def update_stacked_energy_chart_percentage_con(
    selected_cat,
    selected_years,
    selected_state,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
):
    return updateStackedEnergyChart_percentage(
        selected_cat,
        selected_years,
        selected_state,
        clickDataDifferentPlot,
        clickDataThisPlot,
        selected_msn_codes,
        True,
    )


@app.callback(
    Output("selected_msn_codes_con", "data"),
    [
        State("selected_msn_codes_con", "data"),
        Input("stacked-area-chart-consumption", "clickData"),
        Input("diverging-bar-chart-consumption", "clickData"),
    ],
    prevent_initial_call=True,
)
def update_state_of_selected_MSN_codes_con(
    selected_MSN_codes, clickData_stackChart, clickData_DivChart
):
    return update_state_of_selected_MSN_codes(
        selected_MSN_codes, clickData_stackChart, clickData_DivChart
    )


@app.callback(
    Output("selected_msn_codes_pro", "data"),
    [
        State("selected_msn_codes_pro", "data"),
        Input("stacked-area-chart-production", "clickData"),
        Input("diverging-bar-chart-production", "clickData"),
    ],
    prevent_initial_call=True,
)
def update_state_of_selected_MSN_codes_pro(
    selected_MSN_codes, clickData_stackChart, clickData_DivChart
):
    return update_state_of_selected_MSN_codes(
        selected_MSN_codes, clickData_stackChart, clickData_DivChart
    )


def update_state_of_selected_MSN_codes(
    selected_msn_codes, clickData_stackChart, clickData_DivChart
):
    print(f"Initial MSN codes: {selected_msn_codes}")

    if clickData_stackChart:
        clicked_msn_code = clickData_stackChart["points"][0]["customdata"]
        print(f"Clicked MSN (Stack Chart): {clicked_msn_code}")
        # Toggle selection
        if clicked_msn_code in selected_msn_codes:
            selected_msn_codes.remove(clicked_msn_code)  # Deselect
            print(
                f"Removed {clicked_msn_code}, Updated MSN codes: {selected_msn_codes}"
            )
        else:
            selected_msn_codes.append(clicked_msn_code)  # Select
            print(f"Added {clicked_msn_code}, Updated MSN codes: {selected_msn_codes}")

    if clickData_DivChart:
        clicked_msn_code = clickData_DivChart["points"][0]["customdata"]
        print(f"Clicked MSN (Div Chart): {clicked_msn_code}")
        # Toggle selection
        if clicked_msn_code in selected_msn_codes:
            selected_msn_codes.remove(clicked_msn_code)  # Deselect
            print(
                f"Removed {clicked_msn_code}, Updated MSN codes: {selected_msn_codes}"
            )
        else:
            selected_msn_codes.append(clicked_msn_code)  # Select
            print(f"Added {clicked_msn_code}, Updated MSN codes: {selected_msn_codes}")

    return selected_msn_codes


def update_diverging_bar_chart(
    selected_cat,
    selected_state,
    selected_years,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
    is_consumption,
):
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production

    # Determine the categories to select
    select_Categories = selected_cat
    if selected_cat is not None and selected_cat != []:
        children_of_cat = get_all_children_of_category(selected_cat[0], tree)
        select_Categories += children_of_cat

    # Filter the data based on selected categories, state, and years
    current_data_df = filterByValues(select_Categories, current_data_df)
    current_data_df = filterData([selected_state], current_data_df, "StateCode")
    current_data_df = filterByValues(selected_years, current_data_df)
    current_data_df["label_text"] = current_data_df.apply(
        lambda row: get_title_from_MSN_code(row["MSN"], tree)[0], axis=1
    )

    # Calculate relative values for each category
    for category in current_data_df["MSN"].unique():
        mean_US_val = calculate_mean_for_US_for(category, selected_years)
        filtered_data = current_data_df[current_data_df["MSN"] == category]
        relative_values = calculate_relative_value_for(filtered_data, mean_US_val)
        current_data_df.loc[
            current_data_df["MSN"] == category, "RelativeData"
        ] = relative_values

    # Create the bar plot
    bar = go.Bar(
        x=current_data_df["RelativeData"],
        y=current_data_df["label_text"],
        orientation="h",
        customdata=current_data_df["MSN"],
        marker=dict(
            color=current_data_df["RelativeData"].apply(
                lambda x: "#f1a340" if x >= 0 else "#998ec3"
            )
        ),
        hovertemplate="Category: %{y}<br>Year: "
        + str(selected_years)
        + "<br>Relative Value: {x}%<extra></extra>",
    )

    fig = go.Figure(data=bar)

    # Update layout
    fig.update_layout(
        plot_bgcolor="white",
        barmode="relative",
        yaxis_autorange="reversed",
        bargap=0.01,
        legend_orientation="h",
        legend_x=-0.05,
        legend_y=1.1,
        xaxis=dict(
            title="Relative Data (%)",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            showgrid=True,
            gridcolor="lightgrey",
        ),
        yaxis=dict(title="Category"),
        title=f"Selected categories relative to the mean value of all US states for {dt.get_state_name(selected_state)}",
    )

    # Centering the diverging bars
    max_abs_value = current_data_df["RelativeData"].abs().max()
    fig.update_xaxes(range=[-max_abs_value, max_abs_value])

    if clickDataDifferentPlot or clickDataThisPlot:
        bar_colors = ["gray"] * len(current_data_df)
        # Highlight the selected bars
        counter = 0  # Initialize a counter to keep track of position in bar_colors list
        for idx, row in current_data_df.iterrows():
            if row["MSN"] in selected_msn_codes:
                bar_colors[counter] = (
                    "#f1a340" if row["RelativeData"] >= 0 else "#998ec3"
                )
            counter += 1  # Increment the counter for each row

        # Update the bar trace with the new colors
        fig.data[0].marker.color = bar_colors

    return fig


@app.callback(
    Output("diverging-bar-chart-consumption", "figure"),
    [
        Input("selected_category_overview_con", "data"),
        Input("selected_states_con", "data"),
        Input("selected_years_con", "data"),
        State("stacked-area-chart-consumption", "clickData"),
        State("diverging-bar-chart-consumption", "clickData"),
        Input("selected_msn_codes_con", "data"),
    ],
    prevent_initial_call=True,
)
def update_diverging_bar_chart_con(
    selected_category,
    selected_state,
    selected_year,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
):
    return update_diverging_bar_chart(
        selected_category,
        selected_state,
        selected_year,
        clickDataDifferentPlot,
        clickDataThisPlot,
        selected_msn_codes,
        True,
    )


@app.callback(
    Output("diverging-bar-chart-production", "figure"),
    [
        Input("selected_category_overview_pro", "data"),
        Input("selected_states_pro", "data"),
        Input("selected_years_pro", "data"),
        State("stacked-area-chart-production", "clickData"),
        State("diverging-bar-chart-production", "clickData"),
        Input("selected_msn_codes_pro", "data"),
    ],
    prevent_initial_call=True,
)
def update_diverging_bar_chart_prod(
    selected_cat,
    selected_state,
    selected_years,
    clickDataDifferentPlot,
    clickDataThisPlot,
    selected_msn_codes,
):
    return update_diverging_bar_chart(
        selected_cat,
        selected_state,
        selected_years,
        clickDataDifferentPlot,
        clickDataThisPlot,
        selected_msn_codes,
        False,
    )


def get_current_data(data_to_update):
    if data_to_update:
        current_data_df = pd.DataFrame(data_to_update)
    else:
        current_data_df = pd.DataFrame(dt.stads_df)
    return current_data_df


def get_unfiltered_years_cats_states(is_consumption):
    if is_consumption:
        return [2021], ["TETCB"], "US"
    else:
        return [2021], ["TEPRB"], "US"


# CALLBACK FOR DATA FILTERING FOR OVERVIEW (MAP)
def update_overview_data_storage(
    current_selected_category,
    current_selected_state,
    selected_cat,
    time_range,
    click_data_map,
    is_consumption,
):
    current_data_df_overview = pd.DataFrame(dt.stads_df)
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)
    tree = dt.consumption if is_consumption else dt.production
    if not selected_cat and not time_range and not click_data_map:
        return (
            current_data_df_overview.to_dict("records"),
            years_def,
            cats_def,
            states_def,
        )

    if selected_cat:
        select_Category = get_MSN_code_from_title(
            selected_cat["points"][0]["label"], tree
        )

        print(
            f"Cat was selected, update_overview_data_storage: Selected category: {select_Category}"
        )
    else:
        select_Category = current_selected_category if not None else cats_def

    if click_data_map:
        state_code = click_data_map["points"][0]["text"]
    else:
        state_code = current_selected_state if not None else states_def

    if len(time_range) == 1:
        single_year = time_range[0]
        single_year = int(single_year)
        current_data_df_overview = current_data_df_overview[
            current_data_df_overview["Year"] == single_year
        ]

    elif len(time_range) == 2:
        min_year, max_year = time_range
        min_year = int(min_year)
        max_year = int(max_year)

        current_data_df_overview = current_data_df_overview[
            (current_data_df_overview["Year"] >= min_year)
            & (current_data_df_overview["Year"] <= max_year)
        ]

    current_data_df_overview = filterByValues(select_Category, current_data_df_overview)
    current_data_df_overview = filterData(
        [state_code], current_data_df_overview, "StateCode"
    )

    if current_data_df_overview.empty:
        return dt.stads_df.to_dict("records"), time_range, select_Category, state_code

    print(f"Selected category from the filtering overview {select_Category}")
    return (
        current_data_df_overview.to_dict("records"),
        time_range,
        select_Category,
        state_code,
    )


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
    ],
    prevent_initial_call=True,
)
def update_consumption_overview_data_storage(
    current_selected_category,
    current_selected_state,
    selected_consumption,
    time_range,
    click_data_consumption_map,
):
    return update_overview_data_storage(
        current_selected_category,
        current_selected_state,
        selected_consumption,
        time_range,
        click_data_consumption_map,
        True,
    )


@app.callback(
    [
        Output("production_overview_data_storage", "data"),
        Output("selected_years_pro", "data"),
        Output("selected_category_overview_pro", "data"),
        Output("selected_states_pro", "data"),
    ],
    [
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ],
    prevent_initial_call=True,
)
def update_production_overview_data_storage(
    current_selected_category,
    current_selected_state,
    selected_production,
    time_range,
    click_data_production_map,
):
    return update_overview_data_storage(
        current_selected_category,
        current_selected_state,
        selected_production,
        time_range,
        click_data_production_map,
        False,
    )


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
    prevent_initial_call=True,
)
def update_consumption_detailed_data_storage(
    current_selected_category,
    current_selected_state,
    selected_consumption,
    time_range,
    click_data_consumption_map,
):
    return update_detailed_data_storage(
        current_selected_category,
        current_selected_state,
        selected_consumption,
        time_range,
        click_data_consumption_map,
        True,
    )


@app.callback(
    Output("production_detailed_data_storage", "data"),
    [
        State("selected_category_overview_pro", "data"),
        State("selected_states_pro", "data"),
        Input("icicle-plot-production", "clickData"),
        Input("year-slider", "value"),
        Input("choropleth-map-production", "clickData"),
    ],
    prevent_initial_call=True,
)
def update_production_detailed_data_storage(
    current_selected_category,
    current_selected_state,
    selected_production,
    time_range,
    click_data_production_map,
):
    return update_detailed_data_storage(
        current_selected_category,
        current_selected_state,
        selected_production,
        time_range,
        click_data_production_map,
        False,
    )


def update_detailed_data_storage(
    current_selected_category,
    current_selected_state,
    selected_cat,
    time_range,
    click_data_map,
    is_consumption,
):
    current_data_df = pd.DataFrame(dt.stads_df)
    tree = dt.consumption if is_consumption else dt.production
    years_def, cats_def, states_def = get_unfiltered_years_cats_states(is_consumption)

    if not selected_cat and not time_range and not click_data_map:
        return current_data_df.to_dict("records")

    children_of_cat = None
    if selected_cat:
        children_of_cat = get_all_children_of_category(
            selected_cat["points"][0]["label"], tree
        )
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
    [Output("data_for_map_con", "data"), Output("consumption-map-switch", "label")],
    Input("consumption-map-switch", "on"),
)
def update_map_switch(on):
    if on:
        return "EnergyPerGDP", "Consumption per GDP"
    else:
        return "EnergyPerCapita", "Consumption per Capita"


def update_map(
    clickData,
    selected_category,
    selected_years,
    is_selected_state,
    columnNameData_to_use="Data",
):
    geoData = dt.geoData
    tree = dt.consumption if columnNameData_to_use != "Data" else dt.production
    title_cat = get_title_from_MSN_code(selected_category[0], tree)
    print(f"Title category {title_cat}, column data to use: {columnNameData_to_use}")
    ##FILTERING
    current = pd.DataFrame(dt.stads_df)
    current = filterData(selected_category, current, "MSN")
    current = filterData(selected_years, current, "Year")

    merged_data = geoData.merge(current, left_on="iso3166_2", right_on="StateCode")
    merged_data["centroid"] = merged_data["geometry"].apply(lambda x: x.centroid)

    merged_data["hover_text"] = merged_data.apply(
        lambda row: f"State Code: {row['StateCode']}\n"
        f"\nFull State Name: {row['full_state_code']}\n"
        f"\n{title_cat[0]}: {row[columnNameData_to_use]} BTU",
        axis=1,
    )

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
            # print(f"dir: go.choroplethmapbox.Marker: {dir(go.choroplethmapbox.Marker)}")
            fig.update_traces(
                marker=dict(
                    # line=dict(color="blue"),
                    opacity=[
                        0.7 if state_code == selected_state else 0.2
                        for state_code in merged_data["StateCode"]
                    ],
                ),
            )
    else:
        min_range, max_range = (
            merged_data[columnNameData_to_use].min(),
            merged_data[columnNameData_to_use].max(),
        )
        print(f"min: {min_range} max: {max_range}")
        fig = px.choropleth_mapbox(
            merged_data,
            geojson=merged_data.geometry,
            locations=merged_data.index,
            mapbox_style="white-bg",
            color=columnNameData_to_use,
            range_color=(min_range, max_range),
            color_continuous_scale="Blues",
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
    ],
)
def update_is_selected_cat_info_con(
    is_selected_cat, current_selected_cat, click_icicle
):
    return update_is_selected_category_info(
        is_selected_cat, current_selected_cat, click_icicle
    )


@app.callback(
    Output("is_selected_category_pro", "data"),
    [
        State("is_selected_category_pro", "data"),
        State("selected_category_overview_pro", "data"),
        Input("icicle-plot-production", "clickData"),
    ],
)
def update_is_selected_cat_info_pro(
    is_selected_cat, current_selected_cat, click_icicle
):
    return update_is_selected_category_info(
        is_selected_cat, current_selected_cat, click_icicle
    )


def update_is_selected_category_info(
    is_selected_cat, current_selected_cat, click_icicle
):
    if is_selected_cat or click_icicle:
        print(f"Category was selected")
        clicked_the_same_cat = (
            True
            if current_selected_cat == click_icicle["points"][0]["label"]
            else False
        )
        print(f"Was the same cat selected?: {clicked_the_same_cat}")
        return not clicked_the_same_cat
    return False


@app.callback(
    Output("is_selected_state_con", "data"),
    [
        State("is_selected_state_con", "data"),
        State("selected_states_con", "data"),
        Input("choropleth-map-consumption", "clickData"),
    ],
)
def update_is_selected_map_info_con(
    is_selected_state, current_selected_state, click_map
):
    print("update_is_selected_map_info_con was called")
    return update_is_selected_map_info(
        is_selected_state, current_selected_state, click_map
    )


@app.callback(
    Output("is_selected_state_pro", "data"),
    [
        State("is_selected_state_pro", "data"),
        State("selected_states_pro", "data"),
        Input("choropleth-map-production", "clickData"),
    ],
)
def update_is_selected_map_info_pro(
    is_selected_state, current_selected_state, click_map
):
    return update_is_selected_map_info(
        is_selected_state, current_selected_state, click_map
    )


def update_is_selected_map_info(is_selected_state, current_selected_state, click_map):
    if is_selected_state or click_map:
        print("State was selected!")
        clicked_the_same_state = (
            True if current_selected_state == click_map["points"][0]["text"] else False
        )
        print(f"Was the same state selected?: {clicked_the_same_state}")
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
    ],
)
def update_map_consumption(
    clickData, selected_category, selected_years, is_selected_state, data_to_use
):
    return update_map(
        clickData, selected_category, selected_years, is_selected_state, data_to_use
    )


@app.callback(
    Output("choropleth-map-production", "figure"),
    [
        Input("choropleth-map-production", "clickData"),
        Input("selected_category_overview_pro", "data"),
        Input("selected_years_pro", "data"),
        Input("is_selected_state_pro", "data"),
    ],
)
def update_map_production(
    clickData, selected_category, selected_years, is_selected_state_pro
):
    return update_map(
        clickData, selected_category, selected_years, is_selected_state_pro
    )


def toggle_visibility_consumption_production(multiStateSwitchValue):
    if multiStateSwitchValue == "display_consumption":
        return {"flex": "0", "display": "flex"}, {"flex": "0", "display": "none"}
    if multiStateSwitchValue == "display_production":
        return {"flex": "0", "display": "none"}, {"flex": "0", "display": "flex"}
    if multiStateSwitchValue == "display_both":
        return {"flex": "0", "display": "flex"}, {"flex": "0", "display": "flex"}


###############
@app.callback(
    Output("diverging-bar-chart-consumption", "style"),
    [
        Input("is_selected_state_con", "data"),
        Input("is_selected_category_con", "data"),
    ],
)
def show_diverging_plot_consumption(is_selected_state_con, is_selected_cat_con):
    return show_component_when_category_and_state_selected(
        is_selected_state_con, is_selected_cat_con
    )


@app.callback(
    Output("diverging-bar-chart-production", "style"),
    [
        Input("is_selected_state_pro", "data"),
        Input("is_selected_category_pro", "data"),
    ],
)
def show_diverging_plot_consumption(is_selected_state_pro, is_selected_cat_pro):
    return show_component_when_category_and_state_selected(
        is_selected_state_pro, is_selected_cat_pro
    )


##########################
@app.callback(
    Output("stacked-area-chart-consumption", "style"),
    [
        Input("is_selected_state_con", "data"),
        Input("is_selected_category_con", "data"),
    ],
)
def show_stacked_plot_consumption(is_selected_state_con, is_selected_cat_con):
    return show_component_when_category_and_state_selected(
        is_selected_state_con, is_selected_cat_con
    )


@app.callback(
    Output("stacked-area-chart-production", "style"),
    [
        Input("is_selected_state_pro", "data"),
        Input("is_selected_category_pro", "data"),
    ],
)
def show_stacked_plot_production(is_selected_state_pro, is_selected_cat_pro):
    return show_component_when_category_and_state_selected(
        is_selected_state_pro, is_selected_cat_pro
    )


def show_component_when_category_and_state_selected(clicked_map, clicked_icicle_plot):
    if clicked_map and clicked_icicle_plot:
        print("Its time to show diverging plot")
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
        Output("icicle-plot-production", "style"),
    ],
    Input("multi-state-switch", "value"),
)
def toggle_icicle_plot_visibility(toggle_state):
    return toggle_visibility_consumption_production(toggle_state)
