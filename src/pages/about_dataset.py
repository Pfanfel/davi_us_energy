import dash_bootstrap_components as dbc
from dash import dcc



# Custom CSS styles
custom_styles = {
    'container': {
        'fontSize': '14px',
        'lineHeight': '1.6',
        'color': '#333',
        'backgroundColor': '#f8f8f8',  # Light gray background color
        'margin': '20px',              # Add margin for spacing
        'padding': '20px',             # Add padding for spacing
        'text-align': 'justify',       # Set text alignment to justify
        'border': '1px solid #ddd',    # Add a border
        'borderRadius': '8px',         # Add border radius for rounded corners
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Add a subtle box shadow
    },
}




layout_about_dataset_page = dbc.Container(
    children=[
        dcc.Markdown(
            """
            ## The Datasets used in this project
            
            - [Energy Consumption and Production](https://www.eia.gov/state/seds/)
            - [Population totals per state](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html)
            - [GDP per state](https://www.bea.gov/data/gdp/gdp-state)
            
            ## About SEDS
            
            The **State Energy Data System (SEDS)** is a program by the *U.S. Energy Information Administration (EIA)* that delivers comprehensive state-level energy statistics for the United States. It covers aspects such as energy production, consumption, prices, and expenditures, providing valuable insights for policymakers, researchers, and the public to understand and analyze energy trends at the state level. SEDS plays a crucial role in supporting informed decision-making and policy analysis in the field of energy.

            In crafting this insightful data visualization, we have leveraged the rich and extensive dataset sourced from the Energy Information Administration (EIA). This dataset encompasses energy-related variables for all 51 units in the United States, including states and the District of Columbia, each uniquely represented by two-character codes following the U.S. Postal Service State abbreviations.

            The structure of the dataset follows a tabular format, where each row represents a unique observation of a specific variable for a particular country in a given year.
            
            | Variable    | Country    | Year    | Value                  |
            |-------------|------------|---------|------------------------|
            | Variable_1  | Country_1  | Year_1  | Value_1_of_Variable_1  |
            | Variable_1  | Country_1  | Year_2  | Value_2_of_Variable_1  |
            | ...         | ...        | ...     | ...                    |
            | Variable_1  | Country_2  | Year_2  | Value_2_of_Variable_1  |
            | ...         | ...        | ...     | ...                    |
            | Variable_N  | Country_N  | Year_T  | Value_T_of_Variable_N  |

            As for the classification of variables, they are categorized into two distinct classes:

            **Consumptions:**
            
            These variables provide a detailed perspective on energy consumption patterns, encompassing sources and end-use sectors.

            - **Total Energy Consumption (TETCB):** An overarching metric reflecting the nation's aggregate energy usage.
            - **Fossil Fuels Breakdown:**
                - Coal (CLTCB)
                - Natural Gas (NNTCB)
                - Petroleum (PMTCB)
                - Total Fossil Fuels (FFTCB): Summation of coal, natural gas, and petroleum consumption.
                - Nuclear Electric Power (NUETB): Quantifies the consumption of energy derived from nuclear sources.
                - Renewable Energy Sources (RETCB): Encompasses a spectrum of renewable sources contributing to the energy mix.
                - Net Interstate Flow of Electricity (ELISB): Tracks the movement of electricity between states.
                - Electricity Net Imports (ELNIB): Measures the net inflow or outflow of electricity.
            - **End-Use Sectors:**
                - Residential (TERCB)
                - Commercial (TECCB)
                - Industrial (TEICB)
                - Transportation (TEACB): Captures energy consumption patterns in distinct sectors.

            **Production Variables:**

            These variables shed light on primary energy production, offering insights into the contributions of various sources.
            
            - **Fossil Fuels Breakdown:**
                - Coal (CLPRB)
                - Natural Gas (NGMPB)
                - Petroleum (PAPRB)
                - Nuclear Electric Power (NUETP): Reflects the production of energy through nuclear means.
            - **Renewable Energy Sources:**
                - Biofuels (BFPRB)
                - Wood and Waste (WWPRB)
                - Other Renewables (NCPRB)
                - Total Renewable Energy (REPRB): Aggregation of various renewable sources.
            - **Total Production (TEPRB):** Provides an overarching view of the nation's total energy production.
            
            
            ### Normalization
            To provide a more nuanced perspective, two additional datasets have been incorporated into the analysis:

            - Population Totals:
            Yearly population data for each state has been integrated to normalize energy consumption per capita. This normalization enables a more accurate assessment of energy usage patterns relative to the population size.

            - GDP Per State:
            The Gross Domestic Product (GDP) per state has been added to normalize various data variables, allowing for a comprehensive understanding of energy metrics in relation to economic activities. This normalization facilitates a deeper exploration of the impact of energy consumption and production on state economies.  
            
            #### Additional information
            
            While some SEDS data series come directly from surveys conducted by EIA,
            many are estimated using other available information. These estimations are necessary 
            for the compilation of "total energy" estimates. The data sources and estimation procedures 
            are described in the [technical notes](https://www.eia.gov/state/seds/seds-technical-notes-complete.php?sid=US). We welcome your suggestions on ways to improve our estimation methodologies.

           
            """,
            style=custom_styles['container']
        ),
    ]
)
