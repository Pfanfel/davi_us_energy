from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from data import data as dt


d = {
    "Age": ["0-19", "20-29", "30-39", "40-49", "50-59", "60-Inf"],
    "Male": [1000, 2000, 4200, 5000, 3500, 1000],
    "Female": [1000, 2500, 4000, 4800, 2000, 1000],
}
df = pd.DataFrame(d)

test_year = 2000

test_type = "production"

test_variable = "biofuels"

test_variable_code = "BFPRB"

test_state = "Arizona"
test_state_code = "AZ"

test_date_range = [test_year, test_year]

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


def DivergingBarChart():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=-df["Male"].values,
            y=df["Age"],
            orientation="h",
            name="Male",
            customdata=df["Male"],
            hovertemplate="Age: %{y}<br>Pop:%{customdata}<br>Gender:Male<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Female"],
            y=df["Age"],
            orientation="h",
            name="Female",
            hovertemplate="Age: %{y}<br>Pop:%{x}<br>Gender:Female<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="relative",
        height=400,
        width=700,
        yaxis_autorange="reversed",
        bargap=0.01,
        legend_orientation="h",
        legend_x=-0.05,
        legend_y=1.1,
    )

    return html.Div(
        [dcc.Graph(id="diverging-bar-chart", figure=fig)],
        className="pretty_container",
    )
