from dash import dcc, html, Input, Output
import dash_daq as daq

def TimeSlider(start_year=1960, end_year=2021):
    marks = {str(year): {'label': '', 'style': {'transform': 'scale(0.5)'}} for year in range(start_year, end_year + 1)}
    year_labels = {str(year): str(year) for year in range(start_year, end_year + 1, 5)}

    slider = dcc.RangeSlider(
        id='year-slider',
        min=start_year,
        max=end_year,
        step=1,
        value=[start_year, end_year],
        marks=year_labels,
        tooltip={"placement": "bottom", "always_visible": True},
        allowCross=False,
    )

    toggle_switch = daq.BooleanSwitch(
        id='year-toggle',
        on=True,
        label=True,
        labelPosition='bottom',
        style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '10px', 'transform': 'scale(0.8)'}
    )

    checkbox = dcc.Checklist(
        id='confirm-checkbox',
        options=[{'label': 'Confirm Selection', 'value': 'confirm'}],
        style={'display': 'inline-block', 'border-radius': '20px', 'vertical-align': 'middle', 'margin-left': '10px', 'transform': 'scale(0.8)'}
    )

    # Create a container for the switch and checkbox with circular edges
    switch_and_checkbox_container = html.Div(
        children=[toggle_switch, html.Br(), checkbox],
        style={
            'display': 'inline-block',
            'border': '1px solid #ccc',
            'border-radius': '20px',
            'padding': '5px',
            'margin-bottom': '20px',  # Add margin to create space between the container and the slider
        }
    )

    # Create a container for the switch, slider, and the switch_and_checkbox container
    slider_container = html.Div(
        children=[switch_and_checkbox_container, slider],
        style={'width': '80%'}
    )

    return html.Div(
        children=[slider_container],
        style={'display': 'block', 'margin-left': '20px'}
    )
