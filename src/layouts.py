# Dash components, html, and dash tables
from dash import dcc
import feffery_antd_components as fac
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


mapContainer = MapContainer(USmapConsumption, USmapProduction)


### FILTER STUFF TODO: Replace with icicle plot ###


def create_icicle_plot_go_api(data):
    fig = go.Figure(
        go.Icicle(
            ids=data["ids"],
            labels=data["labels"],
            parents=data["parents"],
            domain=dict(column=0.1, width=0.8),
            orientation="v",
        )
    )

    fig.update_layout(
        margin=dict(t=10, b=10, r=10, l=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


def flatten_hierarchy_for_plot(data, parent="", icicle_data=None):
    if icicle_data is None:
        icicle_data = {"ids": [], "parents": [], "labels": []}

    icicle_data["ids"].append(parent)
    icicle_data["parents"].append("")
    icicle_data["labels"].append(data["title"])

    if "children" in data:
        for item in data["children"]:
            flatten_hierarchy_for_plot(item, data["title"], icicle_data)

    return icicle_data


# TODO: Not working yet, need to figure out how to get the data in the right format
def create_icicle_plot_go_api(hierarchical_data):
    icicle_data = flatten_hierarchy_for_plot(hierarchical_data)
    icicle_plot = create_icicle_plot_go_api(icicle_data)
    return icicle_plot


def create_icicle_plot(hierarchical_data):
    def flatten_hierarchy(data, parent="", character_list=None):
        if character_list is None:
            character_list = []

        character_list.append({"character": data["title"], "parent": parent})

        if "children" in data:
            for item in data["children"]:
                flatten_hierarchy(item, data["title"], character_list)

        return character_list

    flattened_data = flatten_hierarchy(hierarchical_data[0])

    data_for_icicle = {
        "character": [item["character"] for item in flattened_data],
        "parent": [item["parent"] for item in flattened_data],
    }

    fig = px.icicle(
        data_for_icicle,
        names="character",
        parents="parent",
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


def Container(id1, id2):
    return html.Div(
        [
            html.Div([id1], style={"flex": "1"}),
            html.Div([id2], style={"flex": "1"}),
        ],
        style={"display": "flex", "flex-direction": "row", "flex": "1"},
        className="row",
    )


def CategoryPicker(consumption_filters, production_filters):
    container = Container(consumption_filters, production_filters)
    return html.Div(
        [
            html.H2("Select Category"),
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
            container,
        ]
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
