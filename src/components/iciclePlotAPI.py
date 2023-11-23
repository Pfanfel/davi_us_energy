from dash import html, dcc
import plotly.graph_objects as go



def IciclePlot_API(data, plot_id):
    # Docu for icicle:
    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Icicle.html
    # https://plotly.com/python/reference/icicle/
    fig = go.Figure(
        go.Icicle(
            labels=data["labels"],
            parents=data["parents"],
        )
    )

    fig.update_traces(
        tiling_orientation="v", selector=dict(type="icicle")
    )  # otherwise it is horizontal
    fig.update_traces(
        root_color="#fee8c8", selector=dict(type="icicle")
    )  # otherwise it is white
    # Update the traces so every level has a different color
    fig.update_traces(
        branchvalues="total",
        selector=dict(type="icicle"),
    )

    # increasing the font size of the labels
    fig.update_traces(textfont_size=18, selector=dict(type="icicle"))

    return html.Div(
        [
            dcc.Graph(
                id=plot_id,
                figure=fig,
                style={"width": "100%", "height": "500px"},
            )
        ],
        className="pretty_container",
    )
