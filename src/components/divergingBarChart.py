from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from data import data as dt


# calc_avg = dt.calculate_avg_value(
#     dt.stads_df, test_state_code, test_date_range, test_variable_code
# )

# print(f"the calc_avg: {calc_avg}")

# Get the selected variables
# Get the selected date or date range
# Based on the selected variables and date, filter the data
# Aggregate the data over the whole US by state, date/date range, and variable to get a avrage value
# Based on that avrage value, create a diverging bar chart in percent.
# Show the raw values (computed avrage and value) on hover


def DivergingBarChart(name):
    return html.Div(
        [
            dcc.Graph(
                id=name,
            )
        ],
    )
