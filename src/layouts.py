from dash import dash_table, dcc
import plotly.graph_objects as go
from data import data as dt
import pandas as pd
from components.mapContainer import MapContainer
from dash import html
from components.timeSlider import TimeSlider
from components.map import USmapHEX, USmapHEX_with_switch
from components.iciclePlotAPI import IciclePlot_API
from components.variablePickerAndToggle import VariablePickerAndToggle
from components.divergingBarChart import DivergingBarChart
from components.stackedAreaChart import StackedAreaChart

"""
This file contains the navbar component of the app.
This component will sit at the top of each page of the application.
"""

time_slider = TimeSlider()
USmapConsumption = USmapHEX_with_switch("choropleth-map-consumption", "consumption-map-switch")
USmapProduction = USmapHEX("choropleth-map-production")
map_container = MapContainer(USmapConsumption, USmapProduction)
# PLOTS
icicle_plot_production = IciclePlot_API(dt.production_hirarchie_icicle, "icicle-plot-production")
icicle_plot_consumption = IciclePlot_API(dt.consumption_hirarchie_icicle, "icicle-plot-consumption")

div_bar_chart_con = DivergingBarChart('diverging-bar-chart-consumption')
div_bar_chart_pro = DivergingBarChart('diverging-bar-chart-production')

stacked_area_chart_percentage_consumption = StackedAreaChart('stacked-area-chart-consumption')
stacked_area_chart_percentage_production = StackedAreaChart('stacked-area-chart-production')


pick_consumption_or_production = VariablePickerAndToggle(icicle_plot_production, icicle_plot_consumption)

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

#STORAGE
storage_consumption_overview = dcc.Store(id='consumption_overview_data_storage', data=dt.stads_df.to_dict('records'))
storage_consumption_detailed = dcc.Store(id='consumption_detailed_data_storage')

storage_production_overview = dcc.Store(id='production_overview_data_storage')
storage_production_detailed = dcc.Store(id='production_detailed_data_storage')

selected_category_overview_con = dcc.Store(id='selected_category_overview_con', data=['TETCB'])
selected_years_overview_con = dcc.Store(id='selected_years_con', data=[1960])
selected_states_con = dcc.Store(id='selected_states_con', data='US')

selected_category_overview_pro = dcc.Store(id='selected_category_overview_pro', data=['TEPRB'])
selected_years_overview_pro = dcc.Store(id='selected_years_pro', data=[1960])
selected_states_pro = dcc.Store(id='selected_states_pro', data='TX')

default_data_for_map_con = dcc.Store(id='data_for_map_con', data='EnergyPerCapita')
#EnergyPerGDP