from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd


d = {
    "Age": ["0-19", "20-29", "30-39", "40-49", "50-59", "60-Inf"],
    "Male": [1000, 2000, 4200, 5000, 3500, 1000],
    "Female": [1000, 2500, 4000, 4800, 2000, 1000],
}
df = pd.DataFrame(d)

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