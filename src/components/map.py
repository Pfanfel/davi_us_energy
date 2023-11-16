from dash import dcc
from dash import html
import plotly.express as px


def USmap(dataframe):
    colorscale = ["#f1a340", "#f7f7f7", "#998ec3"]

    fig = px.choropleth(
        dataframe,
        geojson=px.data.gapminder().query("country == 'USA'").to_dict("records"),
        locations="StateCode",
        locationmode="USA-states",
        hover_name="full_state_name",
        scope="usa",
    )

    # Update the layout to include the hover template
    fig.update_layout(title="US State Choropleth Map")

    return html.Div(
        [
            dcc.Graph(
                id="choropleth-map",
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )


def USHexMap(dataframe):
    colorscale = ["#f1a340", "#f7f7f7", "#998ec3"]

    fig = px.scatter_geo(
        dataframe,
        locations="StateCode",
        locationmode="USA-states",
        color_continuous_scale=colorscale,
        title="US Hexbin Map",
        scope="usa",
    )

    fig.update_geos(
        lataxis_showgrid=True,
        lonaxis_showgrid=True,
        lataxis_range=[25, 50],  # Latitude range for the U.S.
        lonaxis_range=[-130, -65],  # Longitude range for the U.S.
    )

    return html.Div(
        [
            dcc.Graph(
                id="hexbin-map", figure=fig, style={"width": "100%", "height": "500px"}
            )
        ],
        className="pretty_container",
    )
