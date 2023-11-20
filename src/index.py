# import dash-core, dash-html, dash io, bootstrap
import os

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from navbar import Navbar
from layouts import (
    TimeSlider,
    mapContainer,
    create_icicle_plot,
    create_icicle_plot_go_api,
    CategoryPicker,
    test_div_bar_chart,
)
import callbacks

from data import data as dt

from pages import layout_about_energy_page, layout_about_dataset_page

timeSlider = TimeSlider()

# Import app
from app import app

# Import server for deployment
from app import srv as server


# app_name = os.getenv("DASH_APP_PATH", "/dash-baseball-statistics")
app_name = "/davi_us_energy"

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = html.Div(
    [
        html.H4(children="Same header for all pages"),
    ]
)


plot_production = create_icicle_plot(dt.production)
plot_consumption = create_icicle_plot(dt.consumption)

pick_consumption_or_production = CategoryPicker(plot_production, plot_consumption)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])


# Menu callback, set and return
# Declair function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in [app_name, app_name + "/"]:
        return html.Div(
            [
                timeSlider,
                pick_consumption_or_production,
                mapContainer,
                test_div_bar_chart,
            ],
            className="home",
        )
    elif pathname.endswith("/about_dataset"):
        return layout_about_dataset_page
    elif pathname.endswith("/about_energy"):
        return layout_about_energy_page
    else:
        return "ERROR 404: Page not found!"


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
