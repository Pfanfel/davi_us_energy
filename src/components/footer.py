# notes
"""
This file is for creating a simple footer element.
This component will sit at the bottom of each page of the application.
"""

# package imports
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Footer():
    footer = html.Footer(
        html.Div(
            [
                html.Hr(),  # horizontal line
                html.P(
                    [
                        "Made with ❤️ by : Michael Smirnov | Silvia Conte | Meggi Ceka | Michalina Janik",  # TODO: Add links to github and linkedin
                    ],
                ),
            ],
            className="footer mx-5",  # margin left and right
        ),
    )
    return footer
