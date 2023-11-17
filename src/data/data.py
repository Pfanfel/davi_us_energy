"""
This file is used to load data from the data folder and perform any data manipulation that is needed during the lifecycle of the app.
"""

# Import Pandas
import pandas as pd


stads_df = pd.read_csv(
    "C:/Users/Michalina/Deep_Learning/davi_us_energy/src/data/stads_data_parsed_cleaned_pop_gdp_v1_only_from_1998.csv"
)


# Hardcoded list of values for a ui element

col_names = ["energy_type", "energy_activity"]
production = [{
    'title': "total energy production",
    'key': "production",
    'value': "production",
    'children':
            [{
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
            },
            {
                'title': "nuclear electric power",
                'key': "nuclear electric power",
                'value': "nuclear electric power"
            },
            {
                'title': "renewable energy",
                'key': "renewable energy",
                'value': "renewable energy",
                'children': [
                    {
                        'title': "biofuels",
                        'key': "biofuels",
                        'value': "biofuels"
                    },
                    {
                        'title': "wood and waste",
                        'key': "wood and waste",
                        'value': "wood and waste"
                    },
                    {
                        'title': "other",
                        'key': "renewable_energy_other",
                        'value': "renewable_energy_other"

                }],
            }]
}]

consumption = [{
    'title': "total energy consumption",
    'key': "total_energy_consumption",
    'value': "total_energy_consumption",
    'children': [
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
            'title': "renewable energy",
            'key': "renewable energy",
            'value': "renewable energy",
            'children': [
                {
                    'title': "hydroelectric power",
                    'key': "hydroelectric power",
                    'value': "hydroelectric power"
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
                        },
                        {
                            'title': "biodiesel",
                            'key': "biodiesel",
                            'value': "biodiesel"
                        },
                        {
                            'title': "renewable diesel",
                            'key': "renewable diesel",
                            'value': "renewable diesel"
                        },
                        {
                            'title': "energy losses and co-products (biofuels only)",
                            'key': "energy losses and co-products (biofuels only)",
                            'value': "energy losses and co-products (biofuels only)"
                        },
                    ]
                },
                {
                    'title': "geothermal energy",
                    'key': "geothermal energy",
                    'value': "geothermal energy"
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
            'title': "interstate flow (electricity only)",
            'key': "interstate flow (electricity only)",
            'value': "interstate flow (electricity only)"
        },
        {
            'title': "net imports",
            'key': "net imports",
            'value': "net imports"
        }
    ]
}]


#
# production = [
#     {
#         "title": "total energy production",
#         "key": "production",
#         "value": 0,
#         "children": [
#             {"title": "coal", "key": "coal", "value": 1},  # Update the value to the level value
#             {
#                 "title": "natural gas, including supplemental gaseous fuels",
#                 "key": "natural gas, including supplemental gaseous fuels",
#                 "value": 1,
#             },
#             {
#                 "title": "natural gas, excluding supplemental gaseous fuels",
#                 "key": "natural gas, excluding supplemental gaseous fuels",
#                 "value": 1,
#             },
#             {
#                 "title": "nuclear electric power",
#                 "key": "nuclear electric power",
#                 "value": 1,
#             },
#             {
#                 "title": "renewable energy",
#                 "key": "renewable energy",
#                 "value": 1,
#                 "children": [
#                     {"title": "biofuels", "key": "biofuels", "value": 2},
#                     {
#                         "title": "wood and waste",
#                         "key": "wood and waste",
#                         "value": 2,
#                     },
#                     {
#                         "title": "other",
#                         "key": "renewable_energy_other",
#                         "value": 2,
#                     },
#                 ],
#             },
#         ],
#     }
# ]
#
#
# consumption = [
#     {
#         "title": "total energy consumption",
#         "key": "total_energy_consumption",
#         "value": 0,
#         "children": [
#             {
#                 "title": "fossil fuels",
#                 "key": "fossil fuels",
#                 "value": 1,
#                 "children": [
#                     {"title": "coal", "key": "coal", "value": 2},
#                     {
#                         "title": "natural gas, including supplemental gaseous fuels",
#                         "key": "natural gas, including supplemental gaseous fuels",
#                         "value": 2,
#                     },
#                     {
#                         "title": "natural gas, excluding supplemental gaseous fuels",
#                         "key": "natural gas, excluding supplemental gaseous fuels",
#                         "value": 2,
#                     },
#                 ],
#             },
#             {
#                 "title": "nuclear electric power",
#                 "key": "nuclear electric power",
#                 "value": 1,
#             },
#             {
#                 "title": "renewable energy",
#                 "key": "renewable energy",
#                 "value": 1,
#                 "children": [
#                     {
#                         "title": "hydroelectric power",
#                         "key": "hydroelectric power",
#                         "value": 2,
#                     },
#                     {
#                         "title": "biomass",
#                         "key": "biomass",
#                         "value": 2,
#                         "children": [
#                             {
#                                 "title": "wood and waste",
#                                 "key": "wood and waste",
#                                 "value": 3,
#                             },
#                             {
#                                 "title": "fuel ethanol, excluding denaturant",
#                                 "key": "fuel ethanol, excluding denaturant",
#                                 "value": 3,
#                             },
#                             {
#                                 "title": "biodiesel",
#                                 "key": "biodiesel",
#                                 "value": 3,
#                             },
#                             {
#                                 "title": "renewable diesel",
#                                 "key": "renewable diesel",
#                                 "value": 3,
#                             },
#                             {
#                                 "title": "energy losses and co-products (biofuels only)",
#                                 "key": "energy losses and co-products (biofuels only)",
#                                 "value": 3,
#                             },
#                         ],
#                     },
#                     {
#                         "title": "geothermal energy",
#                         "key": "geothermal energy",
#                         "value": 2,
#                     },
#                     {
#                         "title": "photovoltaic and solar thermal energy",
#                         "key": "photovoltaic and solar thermal energy",
#                         "value": 2,
#                     },
#                     {"title": "wind", "key": "wind", "value": 2},
#                 ],
#             },
#             {
#                 "title": "interstate flow (electricity only)",
#                 "key": "interstate flow (electricity only)",
#                 "value": 1,
#             },
#             {"title": "net imports", "key": "net imports", "value": 1},
#         ],
#     }
# ]


energy_activities = [
    {
        "title": "energy activities",
        "key": "energy_activity",
        "value": 0,
        "children": [
            {
                "title": "energy generation",
                "key": "energy generation",
                "value": 1,
                "children": [
                    {
                        "title": "production",
                        "key": "production",
                        "value": 2,
                        "children": [
                            {
                                "title": "marketed production",
                                "key": "marketed production",
                                "value": 2,
                            }
                        ],
                    }
                ],
            },
            {
                "title": "energy consumption",
                "key": "energy consumption",
                "value": 1,
                "children": [
                    {
                        "title": "total consumption of all energy-consuming sectors",
                        "key": "total consumption of all energy-consuming sectors",
                        "value": 2,
                        "children": [
                            {
                                "title": "residential sector consumption",
                                "key": "residential sector consumption",
                                "value": 3,
                            },
                            {
                                "title": "commercial sector consumption",
                                "key": "commercial sector consumption",
                                "value": 3,
                            },
                            {
                                "title": "industrial sector consumption",
                                "key": "industrial sector consumption",
                                "value": 3,
                            },
                            {
                                "title": "transportation sector consumption",
                                "key": "transportation sector consumption",
                                "value": 3,
                            },
                        ],
                    },
                    {
                        "title": "total consumption for electricity generation (nuclear only)",
                        "key": "total consumption for electricity generation (nuclear only)",
                        "value": 2,
                    },
                ],
            },
            {
                "title": "interstate flow (electricity only)",
                "key": "interstate flow (electricity only)",
                "value": 1,
            },
            {"title": "net imports", "key": "net imports", "value": "net imports"},
            {
                "title": "energy losses and co-products (biofuels only)",
                "key": "energy losses and co-products (biofuels only)",
                "value": 1,
            },
        ],
    }
]


energy_categories_types = [
    {
        "title": "energy types",
        "key": "energy_type",
        "value": "energy_type",
        "children": [
            {
                "title": "renewable energy",
                "key": "renewable energy",
                "value": "renewable energy",
                "children": [
                    {
                        "title": "renewable diesel",
                        "key": "renewable diesel",
                        "value": "renewable diesel",
                    },
                    {"title": "biodiesel", "key": "biodiesel", "value": "biodiesel"},
                    {"title": "biofuels", "key": "biofuels", "value": "biofuels"},
                    {
                        "title": "biomass",
                        "key": "biomass",
                        "value": "biomass",
                        "children": [
                            {
                                "title": "wood and waste",
                                "key": "wood and waste",
                                "value": "wood and waste",
                            },
                            {
                                "title": "fuel ethanol, excluding denaturant",
                                "key": "fuel ethanol, excluding denaturant",
                                "value": "fuel ethanol, excluding denaturant",
                            },
                        ],
                    },
                    {
                        "title": "geothermal energy",
                        "key": "geothermal energy",
                        "value": "geothermal energy",
                    },
                    {
                        "title": "hydroelectric power",
                        "key": "hydroelectric power",
                        "value": "hydroelectric power",
                    },
                    {
                        "title": "photovoltaic and solar thermal energy",
                        "key": "photovoltaic and solar thermal energy",
                        "value": "photovoltaic and solar thermal energy",
                    },
                    {"title": "wind", "key": "wind", "value": "wind"},
                ],
            },
            {
                "title": "fossil fuels",
                "key": "fossil fuels",
                "value": "fossil fuels",
                "children": [
                    {"title": "coal", "key": "coal", "value": "coal"},
                    {
                        "title": "natural gas, including supplemental gaseous fuels",
                        "key": "natural gas, including supplemental gaseous fuels",
                        "value": "natural gas, including supplemental gaseous fuels",
                    },
                    {
                        "title": "natural gas, excluding supplemental gaseous fuels",
                        "key": "natural gas, excluding supplemental gaseous fuels",
                        "value": "natural gas, excluding supplemental gaseous fuels",
                    },
                ],
            },
            {
                "title": "nuclear electric power",
                "key": "nuclear electric power",
                "value": "nuclear electric power",
            },
            {
                "title": "all petroleum products",
                "key": "all petroleum products",
                "value": "all petroleum products",
                "children": [
                    {
                        "title": "all petroleum products excluding ethanol blended into motor gasoline",
                        "key": "all petroleum products excluding ethanol blended into motor gasoline",
                        "value": "all petroleum products excluding ethanol blended into motor gasoline",
                    }
                ],
            },
        ],
    }
]


category_trees = [energy_activities, energy_categories_types]

states_dict = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "US": "United States",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
    "X3": "Federal Offshore, Gulf of Mexico",
    "X5": "Federa Offshore, Pacific",
}

# Create a DataFrame from the dictionary
df_states = pd.DataFrame(list(states_dict.items()), columns=['StateCode', 'full_state_name'])


# For derived values or values that need to be calculated from the data
def some_calculation(param1, param2):
    return param1 + param2
