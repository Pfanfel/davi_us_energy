import dash_bootstrap_components as dbc
from dash import dcc



custom_styles = {
    'container': {
        'fontSize': '14px',
        'lineHeight': '1.8',
        'color': '#333',
        'backgroundColor': '#f8f8f8',
        'margin': '20px',
        'padding': '20px',
        'text-align': 'justify',
        'border': '1px solid #ddd',
        'borderRadius': '8px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    'heading': {
        'fontFamily': 'Helvetica',
        'fontSize': '20px',  # Adjust the heading size
        'fontWeight': 'bold',
        'color': '#555',     # Darker color for headings
        'marginBottom': '10px',
    },
}




layout_about_energy_page = dbc.Container(
    children=[
        dcc.Markdown(
            """
            

                
            ### Understanding Energy
                
            In its most common definition, energy is the ability to do work. In other words, everything that can do work has energy. 
            In the case of energy, doing work is also known as causing or making change. 
            Energy is either transformed or transferred every time work is being done. This means that since it changes forms every time it’s used, 
            the amount of energy in the universe will forever remain the same. 
            There are many different sources of energy, but they can all be divided into two categories:
            
            
            1. Non-renewable energy sources
            2. Renewable energy sources
            
            
            Renewable and non-renewable energy sources can be used as primary energy sources to produce useful energy such as heat,
            or they can be used to produce secondary energy sources such as electricity and hydrogen.
            
            ### Non-renewable energy sources
            
            In the United States and many other countries, most energy sources used for doing work are non-renewable energy sources:
            
            - Petroleum
            - Hydrocarbon gas liquids
            - Natural gas
            - Coal
            - Nuclear energy
            
            These energy sources are called non-renewable because their supplies are limited to the amounts
            that we can mine or extract from the earth.
            
            
            ### Renewable energy sources
            
            There are five major renewable energy sources which are naturally replenished:
            
            - Solar energy from the sun
            - Geothermal energy from heat inside the earth
            - Wind energy
            - Biomass from plants
            - Hydropower from flowing water
            
            
            ## Units and Calculatons
            
            We use different physical units to measure different types of energy or fuels.
            
            To compare fuels with each other, we need to convert their measurements to the same units a popular unit for comparing energy is British thermal units (Btu).
            
            In the United States, Btu, a measure of heat energy, is the most common unit for comparing energy sources or fuels.
            
            One Btu is the quantity of heat required to raise the temperature of one pound of liquid water by 1° Fahrenheit (F)
            at the temperature that water has its greatest density (approximately 39° F).
    
            EIA collects data on the physical amounts (volume or weight) of energy sources
            produced, imported, exported, and consumed. EIA converts those amounts into Btu
            equivalents to compare the sources on an equal basis.
            
            ## U.S. Energy Facts
            
            The United States uses and produces many different types and sources of energy,
            which can be grouped into general categories such as primary and secondary, renewable, and fossil fuels.
            
            Primary energy sources include fossil fuels (petroleum, natural gas, and coal), nuclear energy, and renewable sources of energy.
            
            The State Energy Data System provides annual time-series estimates of state-level energy consumption,
            prices, expenditures, and production. The full set of tables and data files are updated annually.
            
            Many sources of energy are used in homes, businesses, industry, and power plants and to travel and transport goods.
            These energy sources are used by five main energy use sectors:
            
            - Residential
            - Commercial
            - Industrial
            - Transportation
            - Electric power
            
            For a comprehensive understanding of various energy types and their applications, please refer to the following source page:
            [The source page](https://www.eia.gov/energyexplained/)

            """,
            style=custom_styles['container']
        ),
    ]
)
