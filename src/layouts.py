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
from src.components.multiStateSwitch import MultiStateSwitch
from src.components.stackedItemContainer import HorizontalItemContainer, HorizontalItemContainer_Custom

"""
This file contains the navbar component of the app.
This component will sit at the top of each page of the application.
"""


map_consumption = USmapHEX_with_switch("choropleth-map-consumption", "consumption-map-switch")
map_production = USmapHEX("choropleth-map-production")
#map_container = MapContainer(map_consumption, map_production)
# PLOTS
icicle_plot_production = IciclePlot_API(dt.production_hirarchie_icicle, "icicle-plot-production")
icicle_plot_consumption = IciclePlot_API(dt.consumption_hirarchie_icicle, "icicle-plot-consumption")

consumption_map_icicle_plot_container = HorizontalItemContainer(map_consumption,icicle_plot_consumption)
production_map_icicle_plot_container = HorizontalItemContainer(map_production,icicle_plot_production)
multi_state_switch = MultiStateSwitch('multi-state-switch')
time_slider = TimeSlider()

time_slider_checkboxes_container = HorizontalItemContainer_Custom(multi_state_switch, time_slider, '15%', '85%')
div_bar_chart_con = DivergingBarChart('diverging-bar-chart-consumption')
div_bar_chart_pro = DivergingBarChart('diverging-bar-chart-production')

stacked_area_chart_percentage_consumption = StackedAreaChart('stacked-area-chart-consumption')
stacked_area_chart_percentage_production = StackedAreaChart('stacked-area-chart-production')

stack_area_chart_div_chart_container_con = HorizontalItemContainer_Custom(div_bar_chart_con, stacked_area_chart_percentage_consumption, '40%', '60%')
stack_area_chart_div_chart_container_pro = HorizontalItemContainer_Custom(div_bar_chart_pro, stacked_area_chart_percentage_production, '40%', '60%')
#pick_consumption_or_production = VariablePickerAndToggle(icicle_plot_production, icicle_plot_consumption)

is_selected_state_pro = dcc.Store(id="is_selected_state_pro", data=False)
is_selected_category_pro = dcc.Store(id="is_selected_category_pro", data=False)
is_selected_state_con = dcc.Store(id="is_selected_state_con", data=False)
is_selected_category_con = dcc.Store(id="is_selected_category_con", data=False)


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
selected_states_pro = dcc.Store(id='selected_states_pro', data='US')

default_data_for_map_con = dcc.Store(id='data_for_map_con', data='EnergyPerCapita')
#EnergyPerGDP

selected_msn_codes_pro = dcc.Store(id='selected_msn_codes_pro', data=['TEPRB'])
selected_msn_codes_con = dcc.Store(id='selected_msn_codes_con', data=['TETCB'])