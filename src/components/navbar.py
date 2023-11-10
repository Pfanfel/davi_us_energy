"""
This file contains the navbar component of the app.
This component will sit at the top of each page of the application.
"""

# Import necessary libraries
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src="assets/aulogo_uk_var1_white.png",
                                    height="30px",
                                )
                            ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "Awsome US Energy Production and Consumption by State",
                                    className="ms-2",
                                )
                            ),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink("About the dataset", href="/about_dataset")
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "About energy in the US", href="/about_energy"
                                )
                            ),
                        ],
                    ),
                    id="navbar-collapse",
                    navbar=True,
                    class_name="justify-content-end",
                ),
            ]
        ),
        color="dark",
        dark=True,
        expand="lg",
    )
    return navbar


# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
