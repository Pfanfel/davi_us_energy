# Dash components, html, and dash tables
from dash import dcc, dash_table
from dash import html
from data import data as dt
import plotly.express as px

# Import Bootstrap components
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

from data import data as dt

import pandas as pd

"""
This file contains the navbar component of the app.
This component will sit at the top of each page of the application.
"""

# Import necessary libraries
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc


from dash import dcc, html, Input, Output
import dash_daq as daq


### SLIDER STUFF ###


def TimeSlider(start_year=1960, end_year=2021):
    marks = {
        str(year): {"label": "", "style": {"transform": "scale(0.5)"}}
        for year in range(start_year, end_year + 1)
    }
    year_labels = {str(year): str(year) for year in range(start_year, end_year + 1, 5)}

    slider = dcc.RangeSlider(
        id="year-slider",
        min=start_year,
        max=end_year,
        step=1,
        value=[start_year, end_year],
        marks=year_labels,
        tooltip={"placement": "bottom", "always_visible": True},
        allowCross=False,
    )

    toggle_switch = daq.BooleanSwitch(
        id="year-toggle",
        on=True,
        label=True,
        labelPosition="bottom",
        style={
            "display": "inline-block",
            "vertical-align": "middle",
            "margin-left": "10px",
            "transform": "scale(0.8)",
        },
    )

    # Create a container for the switch, slider, and the switch_and_checkbox container
    slider_container = html.Div(children=[toggle_switch, html.Br(), slider])

    return html.Div(
        children=[slider_container],
        className="pretty_container",
    )


time_slider = TimeSlider()

### MAP STUFF ###


def USmap(dataframe, id, title):
    colorscale = ["#f1a340", "#f7f7f7", "#998ec3"]

    fig = px.choropleth(
        dataframe,
        geojson=px.data.gapminder().query("country == 'USA'").to_dict("records"),
        locations="StateCode",
        locationmode="USA-states",
        hover_name="full_state_name",
        scope="usa",
    )

    # Update the layout to include the hover temsplate
    fig.update_layout(title=title)

    return html.Div(
        [
            dcc.Graph(
                id=id,
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


USmapConsumption = USmap(
    dt.df_states, "choropleth-map-consumption", "US State map consumption"
)
USmapProduction = USmap(
    dt.df_states, "choropleth-map-production", "US State map production"
)


def MapContainer(USmapConsumption, USmapProduction):
    return html.Div(
        [
            html.Div(
                [USmapConsumption], id="consumption-map-container", style={"flex": "1"}
            ),
            html.Div(
                [USmapProduction],
                id="conditional-map-container",
                style={"flex": "1", "display": "none"},
            ),
        ],
        style={"display": "flex", "flex-direction": "row", "flex": "1"},
        className="row",
    )


map_container = MapContainer(USmapConsumption, USmapProduction)


### FILTER STUFF ###


def create_icicle_plot_go_api(data, plot_id):
    # Docu for icicle:
    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Icicle.html
    # https://plotly.com/python/reference/icicle/
    fig = go.Figure(
        go.Icicle(
            labels=data["labels"],
            parents=data["parents"],
        )
    )

    fig.update_traces(
        tiling_orientation="v", selector=dict(type="icicle")
    )  # oterhwise it is horizontal
    fig.update_traces(
        root_color="#fee8c8", selector=dict(type="icicle")
    )  # oterhwise it is white
    # Updaate the traces so every level has a different color
    fig.update_traces(
        branchvalues="total",
        selector=dict(type="icicle"),
    )

    # increasing the font size of the labels
    fig.update_traces(textfont_size=18, selector=dict(type="icicle"))

    return html.Div(
        [
            dcc.Graph(
                id=plot_id,
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


def stacked_2_item_container(id1, id2):
    return html.Div(
        [
            html.Div([id1], style={"flex": "1"}),
            html.Div([id2], style={"flex": "1"}),
        ],
        style={"display": "flex", "flex-direction": "column", "flex": "1"},
        className="row",
    )


def variable_picker_with_toggle(consumption_filters, production_filters):
    container = stacked_2_item_container(consumption_filters, production_filters)
    return html.Div(
        [
            html.P("Toggle consumption icicle plot on/off:"),
            daq.BooleanSwitch(
                id="category-toggle",
                on=False,
                label=True,
                labelPosition="bottom",
                style={
                    "display": "inline-block",
                    "vertical-align": "middle",
                    "margin-left": "10px",
                    "transform": "scale(0.8)",
                },
            ),
            html.Div(id="production-output"),
            html.Div(id="consumption-output"),
            container,
        ]
    )


icicle_plot_production = create_icicle_plot_go_api(
    dt.production_hirarchie_icicle, "icicle-plot-production"
)

icicle_plot_consumption = create_icicle_plot_go_api(
    dt.consumption_hirarchie_icicle, "icicle-plot-consumption"
)

pick_consumption_or_production = variable_picker_with_toggle(
    icicle_plot_production, icicle_plot_consumption
)

### Diverging bar chart ###

d = {
    "Age": ["0-19", "20-29", "30-39", "40-49", "50-59", "60-Inf"],
    "Male": [1000, 2000, 4200, 5000, 3500, 1000],
    "Female": [1000, 2500, 4000, 4800, 2000, 1000],
}
df = pd.DataFrame(d)


def DivergingBarChart():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=-df["Male"].values,
            y=df["Age"],
            orientation="h",
            name="Male",
            customdata=df["Male"],
            hovertemplate="Age: %{y}<br>Pop:%{customdata}<br>Gender:Male<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Female"],
            y=df["Age"],
            orientation="h",
            name="Female",
            hovertemplate="Age: %{y}<br>Pop:%{x}<br>Gender:Female<extra></extra>",
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

    return html.Div(
        [dcc.Graph(id="diverging-bar-chart", figure=fig)],
        className="pretty_container",
    )


test_div_bar_chart = DivergingBarChart()


### Debug table ###

debug_data_table = html.Div(
    dash_table.DataTable(
        id="stads_id",
        data=dt.stads_df.copy().to_dict("records"),
        page_size=10,  # Number of rows per page
        page_current=0,  # Current page
    ),
    className="pretty_container",
)


### Stacked area chart ###


def stacked_area_chart_percentage():
    # TODO: Change so the data is from the dataframe is used instead
    x = ["Winter", "Spring", "Summer", "Fall"]
    fig = go.Figure()
    fig.update_layout(title="Distribution of energy in selected variable in percentage")

    fig.add_trace(
        go.Scatter(
            x=x,
            y=[40, 20, 30, 40],
            mode="lines",
            line=dict(width=0.5, color="rgb(184, 247, 212)"),
            stackgroup="one",
            groupnorm="percent",  # sets the normalization for the sum of the stackgroup
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[50, 70, 40, 60],
            mode="lines",
            line=dict(width=0.5, color="rgb(111, 231, 219)"),
            stackgroup="one",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[70, 80, 60, 70],
            mode="lines",
            line=dict(width=0.5, color="rgb(127, 166, 238)"),
            stackgroup="one",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[100, 100, 100, 100],
            mode="lines",
            line=dict(width=0.5, color="rgb(131, 90, 241)"),
            stackgroup="one",
        )
    )

    fig.update_layout(
        showlegend=True,
        xaxis_type="category",
        yaxis=dict(type="linear", range=[1, 100], ticksuffix="%"),
    )

    return html.Div(
        [
            dcc.Graph(
                id="stacked-area-chart-percentage",
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


stacked_area_chart_percentage = stacked_area_chart_percentage()
