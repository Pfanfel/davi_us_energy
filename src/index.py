from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components.navbar import Navbar
from layouts import (
    debug_data_table,
    time_slider,
    map_container,
    pick_consumption_or_production,
    test_div_bar_chart,
    stacked_area_chart_percentage,
)
from pages import layout_about_energy_page, layout_about_dataset_page
from app import app
import os
from helpers.filter import get_all_categories_at_same_level
import data.data as dt
import callbacks

# Import server for deployment
app_name = os.getenv("DASH_APP_PATH", "/davi_us_energy/")

nav = Navbar()

# TODO: To we even need a header?
header = html.Div(
    [
        html.H4(children="Same header for all pages"),
    ]
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])
container = dbc.Container([header, content])


# Menu callback, set and return
# Declare function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname in [app_name, app_name + "/"]:
        return html.Div(
            [
                time_slider,
                pick_consumption_or_production,
                map_container,
                debug_data_table,
                stacked_area_chart_percentage,
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
level, nodes = get_all_categories_at_same_level("renewable energy", dt.production)
print(f"Level: {level}, Nodes at same level: {nodes}")

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
