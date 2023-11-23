from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.components.navbar import Navbar
from src.layouts import (
    debug_data_table,
    time_slider,
    map_container,
    pick_consumption_or_production,
    test_div_bar_chart,
    stacked_area_chart_percentage,
)
from pages import layout_about_energy_page, layout_about_dataset_page
import dash
from callbacks import setUp_callbacks


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app_name = "/davi_us_energy"


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
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
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


app.title = "US Energy Consumption Visualization"
srv = app.server
setUp_callbacks(app)



# Run the app
if __name__ == "__main__":
    app.run(debug=True)
