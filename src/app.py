# Import packages
import time

from dash import Dash, html, dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from components import navbar, footer, timeSlider, map, stackAreaChart, categories_overivew, mapContainer, sunbursChart
import feffery_antd_components as fac
import pandas as pd
from dash import Input, Output, State
from helpers.filter import (
    filterData,
    filterByValues,
    get_all_categories_at_same_level,
    get_all_children_of_category, filter_dataframe_by_tree
)
from data import data as dt
import plotly.graph_objects as go

from components.categoryPicker import CategoryPicker
from dash.dependencies import ClientsideFunction, Output
import geopandas as gpd

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
    [Input("production-filter", "value"),
     Input("consumption-filter", "value"),
     Input("year-slider", "value"),
     Input("choropleth-map-consumption", "clickData"),
     Input("choropleth-map-production", "clickData")],
    prevent_initial_call=True,
)
def handle_select_event(selected_production, selected_consumption, time_range, click_data_consumption,
                        click_data_production):
    current_data_df = pd.DataFrame(dt.stads_df.copy())  # Convert the data to a DataFrame

    if not selected_production and not selected_consumption and not time_range and not click_data_consumption and not click_data_production:
        return current_data_df.to_dict(
            "records"
        )  # No filters selected, return the current data as is

    if selected_production:
        current_data_df = filterByValues(selected_production, current_data_df)

        if click_data_production:
            print("Map was clicked")
            state_code = click_data_production["points"][0]["text"]
            print(f"Clicked state {state_code}")
            current_data_df = filterData([state_code], current_data_df, "StateCode")


    elif selected_consumption:
        current_data_df = filterByValues(selected_consumption, current_data_df)

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
            & (current_data_df["Year"] <= max_year)]

    if current_data_df.empty:
        return dt.stads_df.to_dict("records")

    return current_data_df.to_dict("records")


# define the navbar and footer
nav = navbar.Navbar()
footer = footer.Footer()
timeSlider = timeSlider.TimeSlider()
USmapConsumption = map.USmapHEX("choropleth-map-consumption")
USmapProduction = map.USmapHEX("choropleth-map-production")
mapContainer = mapContainer.MapContainer(USmapConsumption, USmapProduction)
sunChart = sunbursChart.SunburstChart()
stackChart = stackAreaChart.StackAreaChart()
consumption_filters = categories_overivew.CreateCategoryFilteringTree(
    dt.consumption, "consumption-filter", "Energy Consumption", ["total_energy_consumption"]
)

production_filters = categories_overivew.CreateCategoryFilteringTree(
    dt.consumption, "production-filter", "Energy Production"
)

categoryPicker = CategoryPicker(consumption_filters, production_filters)

data_table = html.Div(dash_table.DataTable(
    id="stads_id",
    data=dt.stads_df.copy().to_dict("records"),
    page_size=10,  # Number of rows per page
    page_current=0,  # Current page
), className="pretty_container")


@app.callback(
    Output("consumption-filter", "value"),
    [Input("production-filter", "value"),
     Input("category-toggle", "on")],
    [State("consumption-filter", "value")]
)
def clear_consumption_filter(selected_production, toggle_on, current_consumption_value):
    # If production filter is selected, clear the consumption filter
    if not toggle_on and selected_production:
        return []

    return current_consumption_value


@app.callback(
    Output("production-filter", "value"),
    [Input("consumption-filter", "value"),
     Input("category-toggle", "on")],
    [State("production-filter", "value")]
)
def clear_production_filter(selected_consumption, toggle_on, current_production_value):
    # If consumption filter is selected, clear the production filter
    if not toggle_on and selected_consumption:
        return []

    return current_production_value


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
    Output("energy-chart", "figure"),
    [Input("production-filter", "value"),
     Input("consumption-filter", "value"),
     Input("year-slider", "value"),
     Input("choropleth-map-consumption", "clickData")]
)
def update_energy_chart(
        selected_production_categories,
        selected_consumption_categories,
        time_range,
        click_data,
):
    state_code = "US"
    data_to_show = pd.DataFrame(dt.stads_df)
    selected_categories = [get_all_children_of_category('total_energy_consumption', dt.consumption)]

    # should we take the children or on the same level?
    if selected_production_categories:
        selected_categories = get_all_categories_at_same_level(
            selected_production_categories[0], dt.production
        )

        data_to_show = filterByValues(selected_categories, data_to_show)

    elif selected_consumption_categories:
        selected_categories = get_all_categories_at_same_level(
            selected_consumption_categories[0], dt.consumption
        )
        data_to_show = filterByValues(selected_categories, data_to_show)

    if click_data:
        state_code = click_data["points"][0]["text"]
        data_to_show = filterData([state_code], data_to_show, "StateCode")

    fig = go.Figure()

    for energy_type in data_to_show["energy_type"].unique():
        energy_type_data = data_to_show[data_to_show["energy_type"] == energy_type]
        fig.add_trace(
            go.Scatter(
                x=list(range(1998, 2021)),
                y=energy_type_data["Data"],
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
    [Output("year-slider", "disabled"),
     Output("year-slider", "value"),
     Output("year-toggle", "label")],  # Add an Output for the label
    Input("year-toggle", "on"),
)
def update_slider_state(on):
    label = setLabel(on)  # Calculate the label based on the toggle state
    if on:
        return False, [1998], label  # Return label as a part of the tuple
    else:
        return False, [1998, 2021], label  # Return label as a part of the tuple


def setLabel(on):
    if on:
        return "Select Year"
    else:
        return "Select Time Interval"


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

        print(dt.hierarchy_dict.values())
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


@app.callback(
    Output("output-state-click", "children"),
    Input("choropleth-map-consumption", "clickData"))
def display_clicked_state(clickData):
    if clickData is not None:
        state_code = clickData["points"][0]["text"]
        return f"Clicked state code: {state_code}"
    else:
        return ""


energy_filters = html.Div(
    [
        # Energy filters container with flex layout
        categoryPicker
    ],
    style={"display": "flex", "flex-direction": "column", "flex": "0.5"},
    className="pretty_container",
)

app.layout = html.Div(
    [
        nav,
        energy_filters,
        mapContainer,
        timeSlider,
        data_table,
        stackChart,
        sunChart,
        footer,
    ],
    style={"display": "flex", "flex-direction": "column"},
)

# Load GeoDataFrame
url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/us_states_hexgrid.geojson.json"
geoData = gpd.read_file(url)
geoData['centroid'] = geoData['geometry'].apply(lambda x: x.centroid)


@app.callback(
    Output('choropleth-map-consumption', 'figure'),
    Input('choropleth-map-consumption', 'clickData')
)
def update_map(clickData):
    # Create a Scattermapbox trace for annotations
    annotations_trace = go.Scattermapbox(
        lon=geoData['centroid'].apply(lambda x: x.x),
        lat=geoData['centroid'].apply(lambda x: x.y),
        mode='text',
        text=geoData['iso3166_2'],
        textposition='middle center',
        showlegend=False,
        textfont=dict(size=10, color='black'),
        hoverinfo='text',
        hovertext=geoData['google_name']
    )

    # Draw the map using plotly express
    fig = px.choropleth_mapbox(
        geoData,
        geojson=geoData.geometry,
        locations=geoData.index,
        mapbox_style="white-bg",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=2.5
    )

    # Update the map layout
    fig.update_geos(
        fitbounds="locations",  # Adjust the bounds to fit the locations
        visible=False,  # Hide the real map
    )

    # Add the annotations trace to the figure
    fig.add_trace(annotations_trace)

    # Highlight the selected hexagon
    if clickData and 'points' in clickData:
        selected_state = clickData['points'][0]['text']
        print("Selected State:", selected_state)

        # Update the opacity for the selected hexagon
        fig.update_traces(
            marker=dict(
                opacity=[1.0 if state_code == selected_state else 0.3 for state_code in geoData['iso3166_2']],
            ),
        )


    # Update the layout of the entire figure
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )



    return fig


@app.callback(
    Output('choropleth-map-production', 'figure'),
    Input('choropleth-map-production', 'clickData')
)
def update_map_production(clickData):
    # Create a Scattermapbox trace for annotations
    annotations_trace = go.Scattermapbox(
        lon=geoData['centroid'].apply(lambda x: x.x),
        lat=geoData['centroid'].apply(lambda x: x.y),
        mode='text',
        text=geoData['iso3166_2'],
        textposition='middle center',
        showlegend=False,
        textfont=dict(size=10, color='black'),
        hoverinfo='text',
        hovertext=geoData['google_name']
    )

    # Draw the map using plotly express
    fig = px.choropleth_mapbox(
        geoData,
        geojson=geoData.geometry,
        locations=geoData.index,
        mapbox_style="white-bg",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=2.5
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
    if clickData and 'points' in clickData:
        selected_state = clickData['points'][0]['text']
        print("Selected State:", selected_state)

        # Update the opacity for the selected hexagon
        fig.update_traces(
            marker=dict(
                opacity=[1.0 if state_code == selected_state else 0.3 for state_code in geoData['iso3166_2']],
            ),
        )

    return fig


@app.callback(
    [Output('consumption-map-container', 'style'),
     Output('conditional-map-container', 'style')],
    Input('category-toggle', 'on')
)
def toggle_consumption_map_visibility(toggle_state):
    if not toggle_state:
        return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "none"}

    return {"flex": "0", "display": "flex"}, {"flex": "1", "display": "flex"}


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
