"""
This file is used to load data from the data folder and perform any data manipulation that is needed during the lifecycle of the app.
"""

# Import Pandas
import pandas as pd

stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

pop_by_year_df = pd.read_csv("data/pop_year.csv")

gdp_by_year_df = pd.read_csv("data/gdp_year.csv")

# Hardcoded list of values for a ui element

col_names = ['energy_type', 'energy_activity']


energy_activities = [
    {
        'title': "energy activities",
        'key': "energy_activity",
        'value': "energy_activity",
        'children': [
            {
                'title': "energy generation",
                'key': "energy generation",
                'value': "energy generation",
                'children': [
                    {
                        'title': "production",
                        'key': "production",
                        'value': "production",
                        'children': [
                            {
                                'title': "marketed production",
                                'key': "marketed production",
                                'value': "marketed production"
                            }
                        ]
                    }
                ]
            },
            {
                'title': "energy consumption",
                'key': "energy consumption",
                'value': "energy consumption",
                'children': [
                    {
                        'title': "total consumption of all energy-consuming sectors",
                        'key': "total consumption of all energy-consuming sectors",
                        'value': "total consumption of all energy-consuming sectors",
                        'children': [
                            {
                                'title': "residential sector consumption",
                                'key': "residential sector consumption",
                                'value': "residential sector consumption"
                            },
                            {
                                'title': "commercial sector consumption",
                                'key': "commercial sector consumption",
                                'value': "commercial sector consumption"
                            },
                            {
                                'title': "industrial sector consumption",
                                'key': "industrial sector consumption",
                                'value': "industrial sector consumption"
                            },
                            {
                                'title': "transportation sector consumption",
                                'key': "transportation sector consumption",
                                'value': "transportation sector consumption"
                            }
                        ]
                    },
                    {
                        'title': "total consumption for electricity generation (nuclear only)",
                        'key': "total consumption for electricity generation (nuclear only)",
                        'value': "total consumption for electricity generation (nuclear only)"
                    }
                ]
            },
            {
                'title': "interstate flow (electricity only)",
                'key': "interstate flow (electricity only)",
                'value': "interstate flow (electricity only)"
            },
            {
                'title': "net imports",
                'key': "net imports",
                'value': "net imports"
            },
            {
                'title': "energy losses and co-products (biofuels only)",
                'key': "energy losses and co-products (biofuels only)",
                'value': "energy losses and co-products (biofuels only)"
            }
        ]
    }
]

energy_categories_types = [
    {
        'title': "energy types",
        'key': "energy_type",
        'value': "energy_type",
        'children': [
            {
                'title': "renewable energy",
                'key': "renewable energy",
                'value': "renewable energy",
                'children': [
                    {
                        'title': "renewable diesel",
                        'key': "renewable diesel",
                        'value': "renewable diesel"
                    },
                    {
                        'title': "biodiesel",
                        'key': "biodiesel",
                        'value': "biodiesel"
                    },
                    {
                        'title': "biofuels",
                        'key': "biofuels",
                        'value': "biofuels"
                    },
                    {
                        'title': "biomass",
                        'key': "biomass",
                        'value': "biomass",
                        'children': [
                            {
                                'title': "wood and waste",
                                'key': "wood and waste",
                                'value': "wood and waste"
                            },
                            {
                                'title': "fuel ethanol, excluding denaturant",
                                'key': "fuel ethanol, excluding denaturant",
                                'value': "fuel ethanol, excluding denaturant"
                            }
                        ]
                    },
                    {
                        'title': "geothermal energy",
                        'key': "geothermal energy",
                        'value': "geothermal energy"
                    },
                    {
                        'title': "hydroelectric power",
                        'key': "hydroelectric power",
                        'value': "hydroelectric power"
                    },
                    {
                        'title': "photovoltaic and solar thermal energy",
                        'key': "photovoltaic and solar thermal energy",
                        'value': "photovoltaic and solar thermal energy"
                    },
                    {
                        'title': "wind",
                        'key': "wind",
                        'value': "wind"
                    }
                ]
            },
            {
                'title': "fossil fuels",
                'key': "fossil fuels",
                'value': "fossil fuels",
                'children': [
                    {
                        'title': "coal",
                        'key': "coal",
                        'value': "coal"
                    },
                    {
                        'title': "natural gas, including supplemental gaseous fuels",
                        'key': "natural gas, including supplemental gaseous fuels",
                        'value': "natural gas, including supplemental gaseous fuels"
                    },
                    {
                        'title': "natural gas, excluding supplemental gaseous fuels",
                        'key': "natural gas, excluding supplemental gaseous fuels",
                        'value': "natural gas, excluding supplemental gaseous fuels"
                    }
                ]
            },
            {
                'title': "nuclear electric power",
                'key': "nuclear electric power",
                'value': "nuclear electric power"
            },
            {
                'title': "all petroleum products",
                'key': "all petroleum products",
                'value': "all petroleum products",
                'children': [
                    {
                        'title': "all petroleum products excluding ethanol blended into motor gasoline",
                        'key': "all petroleum products excluding ethanol blended into motor gasoline",
                        'value': "all petroleum products excluding ethanol blended into motor gasoline"
                    }
                ]
            }
        ]
    }
]


category_trees = [energy_activities, energy_categories_types]


# For derived values or values that need to be calculated from the data
def some_calculation(param1, param2):
    return param1 + param2