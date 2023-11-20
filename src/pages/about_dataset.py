import dash_bootstrap_components as dbc
from dash import dcc


layout_about_dataset_page = dbc.Container(
    children=[
        dcc.Markdown(
            """
            # About the Datasets used in this project
            
            - [SEDS](https://www.eia.gov/state/seds/)
            - Population TODO: LINK
            - GDP TODO: LINK
            
            ## About SEDS
            
           The State Energy Data System (SEDS) is the source of the U.S. Energy Information Administration's (EIA) 
           comprehensive state energy statistics. EIA's goal in maintaining SEDS is to create historical time series of energy production,
           consumption, prices, and expenditures by state that are defined as consistently as possible over time and across
           sectors for analysis and forecasting purposes.

            ## Dimensions of SEDS estimates
            
            
            ### Production
            - by state and for the United States
            - by primary energy source
            - in physical units and Btu
            - annual time-series back to 1960

            
            ### Consumption
            - by state and for the United States
            - by energy source
            - by sector
            - in physical units and Btu
            - annual time-series back to 1960
            
            #### Additional information
            While some SEDS data series come directly from surveys conducted by EIA,
            many are estimated using other available information. These estimations are necessary 
            for the compilation of "total energy" estimates. The data sources and estimation procedures 
            are described in the [technical notes](https://www.eia.gov/state/seds/seds-technical-notes-complete.php?sid=US). We welcome your suggestions on ways to improve our estimation methodologies.
            

        """
        ),
    ]
)
