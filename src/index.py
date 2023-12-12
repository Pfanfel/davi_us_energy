from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components.navbar import Navbar
from layouts import (
    is_selected_state_pro,
    is_selected_category_pro,
    is_selected_state_con,
    is_selected_category_con,
    time_slider_checkboxes_container,
    stack_area_chart_div_chart_container_con,
    stack_area_chart_div_chart_container_pro,
    storage_consumption_overview,
    storage_consumption_detailed,
    storage_production_detailed,
    storage_production_overview,
    selected_category_overview_con,
    selected_years_overview_con,
    selected_states_con,
    selected_category_overview_pro,
    selected_years_overview_pro,
    selected_states_pro,
    default_data_for_map_con,
    consumption_map_icicle_plot_container,
    production_map_icicle_plot_container,
    selected_msn_codes_pro,
    selected_msn_codes_con
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



content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")],  style={'backgroundColor': 'white', 'maxWidth': '100%', 'margin': 'auto'})
container = dbc.Container([content], fluid=True)



# Menu callback, set and return
# Declare function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname in [app_name, app_name + "/"]:
        return html.Div(
            [
                selected_msn_codes_pro,
                selected_msn_codes_con,
                time_slider_checkboxes_container,
                consumption_map_icicle_plot_container,
                production_map_icicle_plot_container,
                stack_area_chart_div_chart_container_con,
                stack_area_chart_div_chart_container_pro,
                storage_consumption_overview,
                storage_consumption_detailed,
                storage_production_overview,
                storage_production_detailed,
                selected_category_overview_con,
                selected_years_overview_con,
                selected_states_con,
                selected_category_overview_pro,
                selected_years_overview_pro,
                selected_states_pro,
                default_data_for_map_con,
                is_selected_state_pro,
                is_selected_category_pro,
                is_selected_state_con,
                is_selected_category_con,
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
    layout = html.Div([nav, container], style={'backgroundColor': 'white', 'width': '100%', 'height' : '100vh'})
    return layout


# Set layout to index function
app.layout = index()
level, nodes = get_all_categories_at_same_level("REPRB", dt.production)
print(f"Level: {level}, Nodes at same level: {nodes}")

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
