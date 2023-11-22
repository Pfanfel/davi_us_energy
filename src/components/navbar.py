# Import Bootstrap from Dash
import os
import dash_bootstrap_components as dbc

# app_name = os.getenv("DASH_APP_PATH", "/dash-baseball-statistics")

app_name = "/davi_us_energy"


# Navigation Bar fucntion
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("About the dataset", href=f"{app_name}/about_dataset")
            ),
            dbc.NavItem(
                dbc.NavLink("About energy in the US", href=f"{app_name}/about_energy")
            ),
        ],
        brand="Visualisation",
        brand_href=f"{app_name}/",
        sticky="top",
        color="light",
        dark=False,
        expand="lg",
    )
    return navbar
