from dash import dcc
from dash import html
import plotly.express as px


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


def USmapHEX(name):
    return html.Div(
        [
            dcc.Graph(
                id=name,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )
