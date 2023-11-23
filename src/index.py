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


# Import server for deployment


# app_name = os.getenv("DASH_APP_PATH", "/dash-baseball-statistics")

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
