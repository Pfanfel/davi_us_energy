import dash_bootstrap_components as dbc
from dash import dcc


layout_about_energy_page = dbc.Container(
    children=[
        dcc.Markdown(
            """
            
            # About Energy TODO: Source of this text Maggie?
                
            ## What is energy?
                
            Scientists define energy as the ability to do work. Modern civilization is possible because people have
            learned how to change energy from one form to another and then use it to do work.
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

            """
        ),
    ]
)
