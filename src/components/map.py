from dash import dcc
from dash import html
import plotly.express as px

def USmap(dataframe):
    colorscale = ['#f1a340', '#f7f7f7', '#998ec3']

    fig = px.choropleth(dataframe,
                        geojson=px.data.gapminder().query("country == 'USA'").to_dict("records"),
                        locations='StateCode',
                        locationmode='USA-states',
                        hover_name='full_state_code',
                        scope="usa")



    # Update the layout to include the hover template
    fig.update_layout(title="US State Choropleth Map")


    return html.Div([
        dcc.Graph(id='choropleth-map', figure=fig, style={'width': '100%', 'height': '500px'})
    ])
