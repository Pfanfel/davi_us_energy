from dash import (
    html,
    register_page,
    dash_table,
    dcc,
    callback,
    Output,
    Input,
)  # , callback # If you need callbacks, import it here.
import dash_bootstrap_components as dbc

from data import data
import plotly.express as px

import pandas as pd


register_page(
    __name__,
    name="MCV (multiple coordinated view - not a dashboard!",
    top_nav=True,
    path="/",
)


#### ONLY AN EXAMPLE ####
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

example_elemets_graph_with_slider = html.Div(
    [
        dcc.Graph(id="graph-with-slider"),
        dcc.Slider(
            df["year"].min(),
            df["year"].max(),
            step=None,
            value=df["year"].min(),
            marks={str(year): str(year) for year in df["year"].unique()},
            id="year-slider",
        ),
    ]
)


def layout():
    layout = dcc.Loading(  # <- Wrap App with Loading Component
        id="loading_page_content",
        children=[
            example_elemets_graph_with_slider,
            dash_table.DataTable(
                data=data.pop_by_year_df.to_dict("records"), page_size=10
            ),
        ],
        debug=False,  # <- show the refresh button when loading takes longer than 5 seconds.
        color="primary",  # <- Color of the loading spinner
        fullscreen=False,  # <- Loading Spinner should take up full screen
    )
    return layout


@callback(Output("graph-with-slider", "figure"), Input("year-slider", "value"))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
    )

    fig.update_layout(transition_duration=500)

    return fig
