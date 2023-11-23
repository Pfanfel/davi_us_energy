from dash import html, dcc
import plotly.graph_objects as go


def StackedAreaChart_Percentage():
    # TODO: Change so the data is from the dataframe is used instead
    x = ["Winter", "Spring", "Summer", "Fall"]
    fig = go.Figure()
    fig.update_layout(title="Distribution of energy in selected variable in percentage")

    fig.add_trace(
        go.Scatter(
            x=x,
            y=[40, 20, 30, 40],
            mode="lines",
            line=dict(width=0.5, color="rgb(184, 247, 212)"),
            stackgroup="one",
            groupnorm="percent",  # sets the normalization for the sum of the stackgroup
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[50, 70, 40, 60],
            mode="lines",
            line=dict(width=0.5, color="rgb(111, 231, 219)"),
            stackgroup="one",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[70, 80, 60, 70],
            mode="lines",
            line=dict(width=0.5, color="rgb(127, 166, 238)"),
            stackgroup="one",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[100, 100, 100, 100],
            mode="lines",
            line=dict(width=0.5, color="rgb(131, 90, 241)"),
            stackgroup="one",
        )
    )

    fig.update_layout(
        showlegend=True,
        xaxis_type="category",
        yaxis=dict(type="linear", range=[1, 100], ticksuffix="%"),
    )

    return html.Div(
        [
            dcc.Graph(
                id="stacked-area-chart-percentage",
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )

