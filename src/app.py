# import dash and bootstrap components
import dash
import dash_bootstrap_components as dbc


# set app variable with dash, set external style to bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
# set applicaiton title
app.title = "US Energy Consumption Visualization"
# set app server to variable for deployment
srv = app.server

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True
