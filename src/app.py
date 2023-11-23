import dash
import dash_bootstrap_components as dbc

app_name = "/davi_us_energy/"
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], url_base_pathname=app_name
)
app.title = "US Energy Consumption Visualization"
srv = app.server
app.config.suppress_callback_exceptions = True


