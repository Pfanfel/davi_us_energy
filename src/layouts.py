from dash import dash_table
import plotly.graph_objects as go
from src.data import data as dt
import pandas as pd
from components.mapContainer import MapContainer
from dash import html
from components.timeSlider import TimeSlider
from components.map import USmapHEX
from components.iciclePlotAPI import IciclePlot_API
from components.variablePickerAndToggle import VariablePickerAndToggle
from components.divergingBarChart import DivergingBarChart
from components.stackedAreaChart import StackedAreaChart

"""
This file contains the navbar component of the app.
This component will sit at the top of each page of the application.
"""

time_slider = TimeSlider()
USmapConsumption = USmapHEX("choropleth-map-consumption")
USmapProduction = USmapHEX("choropleth-map-production")
map_container = MapContainer(USmapConsumption, USmapProduction)

icicle_plot_production = IciclePlot_API(
    dt.production_hirarchie_icicle, "icicle-plot-production"
)

icicle_plot_consumption = IciclePlot_API(
    dt.consumption_hirarchie_icicle, "icicle-plot-consumption"
)

pick_consumption_or_production = VariablePickerAndToggle(
    icicle_plot_production, icicle_plot_consumption
)

test_div_bar_chart = DivergingBarChart()

### Debug table ###

debug_data_table = html.Div(
    dash_table.DataTable(
        id="stads_id",
        data=dt.stads_df.copy().to_dict("records"),
        page_size=10,  # Number of rows per page
        page_current=0,  # Current page
    ),
    className="pretty_container",
)

stacked_area_chart_percentage = StackedAreaChart()
