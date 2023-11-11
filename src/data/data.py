"""
This file is used to load data from the data folder and perform any data manipulation that is needed during the lifecycle of the app.
"""

# Import Pandas
import pandas as pd

stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

pop_by_year_df = pd.read_csv("data/pop_year.csv")

gdp_by_year_df = pd.read_csv("data/gdp_year.csv")

# Hardcoded list of values for a ui element

energy_activities = [
    {
        'title': "Energy Generation",
        'key': "Energy Generation",
        'children': [
            {
                'title': "Production",
                'key': "Production",
                'children': [
                    {
                        'title': "Marketed Production",
                        'key': "Marketed Production"
                    }
                ]
            }
        ]
    },
    {
        'title': "Energy Consumption",
        'key': "Energy Consumption",
        'children': [
            {
                'title': "Total Consumption of All Energy-Consuming Sectors",
                'key': "Total Consumption of All Energy-Consuming Sectors",
                'children': [
                    {
                        'title': "Residential Sector Consumption",
                        'key': "Residential Sector Consumption"
                    },
                    {
                        'title': "Commercial Sector Consumption",
                        'key': "Commercial Sector Consumption"
                    },
                    {
                        'title': "Industrial Sector Consumption",
                        'key': "Industrial Sector Consumption"
                    },
                    {
                        'title': "Transportation Sector Consumption",
                        'key': "Transportation Sector Consumption"
                    }
                ]
            },
            {
                'title': "Total Consumption for Electricity Generation (Nuclear Only)",
                'key': "Total Consumption for Electricity Generation (Nuclear Only)"
            }
        ]
    },
    {
        'title': "Interstate Flow (Electricity Only)",
        'key': "Interstate Flow (Electricity Only)"
    },
    {
        'title': "Net Imports",
        'key': "Net Imports"
    },
    {
        'title': "Energy Losses and Co-Products (Biofuels Only)",
        'key': "Energy Losses and Co-Products (Biofuels Only)"
    }
]


# tree structure of the energy types
energy_categories_types = [
    {
        'title': "Energy Types",
        'key': "Energy Types",
        'children': [
            {
                'title': "Renewable Energy",
                'key': "Renewable Energy",
                'children': [
                    {
                        'title': "Renewable Diesel",
                        'key': "Renewable Diesel"
                    },
                    {
                        'title': "Biodiesel",
                        'key': "Biodiesel"
                    },
                    {
                        'title': "Biofuels",
                        'key': "Biofuels"
                    },
                    {
                        'title': "Biomass",
                        'key': "Biomass",
                        'children': [
                            {
                                'title': "Wood and Waste",
                                'key': "Wood and Waste"
                            },
                            {
                                'title': "Fuel Ethanol, Excluding Denaturant",
                                'key': "Fuel Ethanol, Excluding Denaturant"
                            }
                        ]
                    },
                    {
                        'title': "Geothermal Energy",
                        'key': "Geothermal Energy"
                    },
                    {
                        'title': "Hydroelectric Power",
                        'key': "Hydroelectric Power"
                    },
                    {
                        'title': "Photovoltaic and Solar Thermal Energy",
                        'key': "Photovoltaic and Solar Thermal Energy"
                    },
                    {
                        'title': "Wind",
                        'key': "Wind"
                    }
                ]
            },
            {
                'title': "Fossil Fuels",
                'key': "Fossil Fuels",
                'children': [
                    {
                        'title': "Coal",
                        'key': "Coal"
                    },
                    {
                        'title': "Natural Gas, Including Supplemental Gaseous Fuels",
                        'key': "Natural Gas, Including Supplemental Gaseous Fuels"
                    },
                    {
                        'title': "Natural Gas, Excluding Supplemental Gaseous Fuels",
                        'key': "Natural Gas, Excluding Supplemental Gaseous Fuels"
                    }
                ]
            },
            {
                'title': "Nuclear Electric Power",
                'key': "Nuclear Electric Power"
            },
            {
                'title': "All Petroleum Products",
                'key': "All Petroleum Products",
                'children': [
                    {
                        'title': "All Petroleum Products Excluding Ethanol Blended into Motor Gasoline",
                        'key': "All Petroleum Products Excluding Ethanol Blended into Motor Gasoline"
                    }
                ]
            }
        ]
    }
]



# For derived values or values that need to be calculated from the data
def some_calculation(param1, param2):
    return param1 + param2
