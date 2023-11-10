# Import packages
from dash import Dash, html, dash_table
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from data import data

from components import navbar, footer


# Initialize the app
app = dash.Dash(
    __name__,
    use_pages=True,  # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],  # fetch the proper css items we want
    meta_tags=[
        {  # check if device is a mobile device. This is a must if you do any mobile styling
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
        }
    ],
    suppress_callback_exceptions=True,
    title="🇺🇸 Awsome Data Visualization for US Energy Production and Consumption by State",
)

# define the navbar and footer
nav = navbar.Navbar()
footer = footer.Footer()

# set the main layout
app.layout = html.Div(
    [
        nav,
        dash.page_container,
        footer,
    ]
)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
