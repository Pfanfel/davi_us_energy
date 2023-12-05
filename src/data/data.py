from src.helpers import filter as flt
import pandas as pd
import geopandas as gpd
from shapely import wkt


import geopandas as gpd
import pandas as pd

stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")
stads_df = stads_df[~stads_df['StateCode'].isin(['X3', 'X5'])]

min_energy_data, max_energy_data = stads_df['Data'].min(), stads_df['Data'].max()

min_energy_GDP, max_energy_GDP = stads_df['EnergyPerGDP'].min(), stads_df['EnergyPerGDP'].max()
min_energy_PerCapita, max_energy_PerCapita = stads_df['EnergyPerCapita'].min(), stads_df['EnergyPerCapita'].max()


geoData = gpd.read_file("data/us_states_hexgrid.geojson.json")
geoData['geometry'] = geoData['geometry'].simplify(tolerance=0.01)
col_to_del_geo = ['cartodb_id', 'created_at', 'updated_at', 'label', 'bees', 'google_name']
geoData.drop(columns=col_to_del_geo, inplace=True)

# # Load the regular DataFrame
# stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")
# # Load the GeoDataFrame
# geo_data_us_states_hexgrid = gpd.read_file("data/us_states_hexgrid.geojson.json")
# # Perform the merge operation using the merge method of GeoDataFrame
# base_data = geo_data_us_states_hexgrid.merge(stads_df, left_on='iso3166_2', right_on='StateCode', how='inner')
# # Drop unnecessary columns

#
# # Save as GeoJSON
# output_file_path = 'data/stads_data_with_hexgrid.geojson'
# base_data.to_file(output_file_path, driver='GeoJSON')

production_hirarchie_icicle = {
    "parents": [
        "",
        "total energy production",
        "total energy production",
        "total energy production",
        "total energy production",
        "total energy production",
        "production of renewable energy",
        "production of renewable energy",
        "production of renewable energy",
    ],# todo: change a labels here to match ith unique titles for MSN values
    "labels": [
        "total energy production",
        "production of coal",
        "production of natural gas",
        "production of petroleum",
        "production of nuclear electric power",
        "production of renewable energy",
        "production of biofuels",
        "production of wood and waste",
        "other production",
    ],
}


consumption_hirarchie_icicle = {
    "parents": [
        "",
        "total energy consumption",
        "consumption of fossil fuels",
        "consumption of fossil fuels",
        "consumption of fossil fuels",
        "total energy consumption",
        "total energy consumption",
        "consumption of renewable energy",
        "consumption of renewable energy",
        "consumption of biomass",
        "consumption of biomass",
        "consumption of biomass",
        "consumption of biomass",
        "consumption of biomass",
        "consumption of renewable energy",
        "consumption of renewable energy",
        "consumption of renewable energy",
        "total energy consumption",
        "total energy consumption",
    ],
    "labels": [
        "total energy consumption",
        "consumption of fossil fuels",
        "consumption of coal",
        "consumption of natural gas",
        "consumption of petroleum",
        "consumption of nuclear electric power",
        "consumption of renewable energy",
        "consumption of hydroelectric power",
        "consumption of biomass",
        "consumption of wood and waste",
        "consumption of ethanol",
        "consumption of biodiesel",
        "consumption of renewable diesel",
        "energy losses and co-products",
        "consumption of geothermal energy",
        "consumption of solar energy",
        "consumption of wind energy",
        "consumption of interstate flow of electricity",
        "consumption of electricity net imports",
    ],
}

# Hardcoded list of values for a ui element

col_names = ["energy_type", "energy_activity"]
# production = [
#     {
#         "title": "total energy production",
#         "key": "production",
#         "value": "production",
#         "children": [
#             {"title": "coal", "key": "coal", "value": "coal"},
#             {
#                 "title": "natural gas, including supplemental gaseous fuels",
#                 "key": "natural gas, including supplemental gaseous fuels",
#                 "value": "natural gas, including supplemental gaseous fuels",
#             },
#             {
#                 "title": "natural gas, excluding supplemental gaseous fuels",
#                 "key": "natural gas, excluding supplemental gaseous fuels",
#                 "value": "natural gas, excluding supplemental gaseous fuels",
#             },
#             {
#                 "title": "nuclear electric power",
#                 "key": "nuclear electric power",
#                 "value": "nuclear electric power",
#             },
#             {
#                 "title": "renewable energy",
#                 "key": "renewable energy",
#                 "value": "renewable energy",
#                 "children": [
#                     {"title": "biofuels", "key": "biofuels", "value": "biofuels"},
#                     {
#                         "title": "wood and waste",
#                         "key": "wood and waste",
#                         "value": "wood and waste",
#                     },
#                     {
#                         "title": "other",
#                         "key": "renewable_energy_other",
#                         "value": "renewable_energy_other",
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
#         "value": "total_energy_consumption",
#         "children": [
#             {
#                 "title": "fossil fuels",
#                 "key": "fossil fuels",
#                 "value": "fossil fuels",
#                 "children": [
#                     {"title": "coal", "key": "coal", "value": "coal"},
#                     {
#                         "title": "natural gas, including supplemental gaseous fuels",
#                         "key": "natural gas, including supplemental gaseous fuels",
#                         "value": "natural gas, including supplemental gaseous fuels",
#                     },
#                     {
#                         "title": "natural gas, excluding supplemental gaseous fuels",
#                         "key": "natural gas, excluding supplemental gaseous fuels",
#                         "value": "natural gas, excluding supplemental gaseous fuels",
#                     },
#                 ],
#             },
#             {
#                 "title": "nuclear electric power",
#                 "key": "nuclear electric power",
#                 "value": "nuclear electric power",
#             },
#             {
#                 "title": "renewable energy",
#                 "key": "renewable energy",
#                 "value": "renewable energy",
#                 "children": [
#                     {
#                         "title": "hydroelectric power",
#                         "key": "hydroelectric power",
#                         "value": "hydroelectric power",
#                     },
#                     {
#                         "title": "biomass",
#                         "key": "biomass",
#                         "value": "biomass",
#                         "children": [
#                             {
#                                 "title": "wood and waste",
#                                 "key": "wood and waste",
#                                 "value": "wood and waste",
#                             },
#                             {
#                                 "title": "fuel ethanol, excluding denaturant",
#                                 "key": "fuel ethanol, excluding denaturant",
#                                 "value": "fuel ethanol, excluding denaturant",
#                             },
#                             {
#                                 "title": "biodiesel",
#                                 "key": "biodiesel",
#                                 "value": "biodiesel",
#                             },
#                             {
#                                 "title": "renewable diesel",
#                                 "key": "renewable diesel",
#                                 "value": "renewable diesel",
#                             },
#                             {
#                                 "title": "energy losses and co-products (biofuels only)",
#                                 "key": "energy losses and co-products (biofuels only)",
#                                 "value": "energy losses and co-products (biofuels only)",
#                             },
#                         ],
#                     },
#                     {
#                         "title": "geothermal energy",
#                         "key": "geothermal energy",
#                         "value": "geothermal energy",
#                     },
#                     {
#                         "title": "photovoltaic and solar thermal energy",
#                         "key": "photovoltaic and solar thermal energy",
#                         "value": "photovoltaic and solar thermal energy",
#                     },
#                     {"title": "wind", "key": "wind", "value": "wind"},
#                 ],
#             },
#             {
#                 "title": "interstate flow (electricity only)",
#                 "key": "interstate flow (electricity only)",
#                 "value": "interstate flow (electricity only)",
#             },
#             {"title": "net imports", "key": "net imports", "value": "net imports"},
#         ],
#     }
# ]

production = [
    {
        "title": "total energy production",
        "key": "TEPRB",
        "value": "TEPRB",
        "children": [
            {
                "title": "production of coal",
                "key": "CLPRB",
                "value": "CLPRB"
            },
            {
                "title": "production of natural gas",
                "key": "NGMPB",
                "value": "NGMPB",
            },
            {
                "title": "production of petroleum",
                "key": "PAPRB",
                "value": "PAPRB",
            },
            {
                "title": "production of nuclear electric power",
                "key": "NUEGB",
                "value": "NUEGB",
            },
            {
                "title": "production of renewable energy",
                "key": "REPRB",
                "value": "REPRB",
                "children": [
                    {
                        "title": "production of biofuels",
                        "key": "BFPRB",
                        "value": "BFPRB"},
                    {
                        "title": "production of wood and waste",
                        "key": "WWPRB",
                        "value": "WWPRB",
                    },
                    {
                        "title": "other production",
                        "key": "NCPRB",
                        "value": "NCPRB",
                    },
                ],
            },
        ],
    }
]



consumption = [
    {
        "title": "total energy consumption",
        "key": "TETCB",
        "value": "TETCB",
        "children": [
            {
                "title": "consumption of fossil fuels",
                "key": "FFTCB",
                "value": "FFTCB",
                "children": [
                    {
                        "title": "consumption of coal",
                        "key": "CLTCB",
                        "value": "CLTCB"},
                    {
                        "title": "consumption of natural gas",
                        "key": "NNTCB",
                        "value": "NNTCB",
                    },
                    {
                        "title": "consumption of petroleum",
                        "key": "PMTCB",
                        "value": "PMTCB",
                    },
                ],
            },
            {
                "title": "consumption of nuclear electric power",
                "key": "NUETB",
                "value": "NUETB",
            },
            {
                "title": "consumption of renewable energy",
                "key": "RETCB",
                "value": "RETCB",
                "children": [
                    {
                        "title": "consumption of hydroelectric power",
                        "key": "HYTCB",
                        "value": "HYTCB",
                    },
                    {
                        "title": "consumption of biomass",
                        "key": "BMTCB",
                        "value": "BMTCB",
                        "children": [
                            {
                                "title": "consumption of wood and waste",
                                "key": "WWTCB",
                                "value": "WWTCB",
                            },
                            {
                                "title": "consumption of ethanol",
                                "key": "EMTCB",
                                "value": "EMTCB",
                            },
                            {
                                "title": "consumption of biodiesel",
                                "key": "BDTCB",
                                "value": "BDTCB",
                            },
                            {
                                "title": "consumption of renewable diesel",
                                "key": "B1TCB",
                                "value": "B1TCB",
                            },
                            {
                                "title": "energy losses and co-products (biofuels only)",
                                "key": "EMLCB",
                                "value": "EMLCB",
                            },
                        ],
                    },
                    {
                        "title": "consumption of geothermal energy",
                        "key": "GETCB",
                        "value": "GETCB",
                    },
                    {
                        "title": "consumption of solar energy",
                        "key": "SOTCB",
                        "value": "SOTCB",
                    },
                    {
                        "title": "consumption of wind energy",
                        "key": "WYTCB",
                        "value": "WYTCB"
                    },
                ],
            },
            {
                "title": "consumption of interstate flow of electricity",
                "key": "ELISB",
                "value": "ELISB",
            },
            {
                "title": "consumption of electricity net imports",
                "key": "ELNIB",
                "value": "ELNIB"
            },
        ],
    }
]


def create_hierarchy_list(node):
    hierarchy_list = [node["key"]]

    if "children" in node:
        children_list = []
        for child in node["children"]:
            child_list = create_hierarchy_list(child)
            children_list.extend(child_list)
        hierarchy_list.append(children_list)

    return hierarchy_list


# Assuming consumption is your hierarchical structure
hierarchy_list = create_hierarchy_list(consumption[0])
# print(hierarchy_list)


energy_activities = [
    {
        "title": "energy activities",
        "key": "energy_activity",
        "value": "energy_activity",
        "children": [
            {
                "title": "energy generation",
                "key": "energy generation",
                "value": "energy generation",
                "children": [
                    {
                        "title": "production",
                        "key": "production",
                        "value": "production",
                        "children": [
                            {
                                "title": "marketed production",
                                "key": "marketed production",
                                "value": "marketed production",
                            }
                        ],
                    }
                ],
            },
            {
                "title": "energy consumption",
                "key": "energy consumption",
                "value": "energy consumption",
                "children": [
                    {
                        "title": "total consumption of all energy-consuming sectors",
                        "key": "total consumption of all energy-consuming sectors",
                        "value": "total consumption of all energy-consuming sectors",
                        "children": [
                            {
                                "title": "residential sector consumption",
                                "key": "residential sector consumption",
                                "value": "residential sector consumption",
                            },
                            {
                                "title": "commercial sector consumption",
                                "key": "commercial sector consumption",
                                "value": "commercial sector consumption",
                            },
                            {
                                "title": "industrial sector consumption",
                                "key": "industrial sector consumption",
                                "value": "industrial sector consumption",
                            },
                            {
                                "title": "transportation sector consumption",
                                "key": "transportation sector consumption",
                                "value": "transportation sector consumption",
                            },
                        ],
                    },
                    {
                        "title": "total consumption for electricity generation (nuclear only)",
                        "key": "total consumption for electricity generation (nuclear only)",
                        "value": "total consumption for electricity generation (nuclear only)",
                    },
                ],
            },
            {
                "title": "interstate flow (electricity only)",
                "key": "interstate flow (electricity only)",
                "value": "interstate flow (electricity only)",
            },
            {"title": "net imports", "key": "net imports", "value": "net imports"},
            {
                "title": "energy losses and co-products (biofuels only)",
                "key": "energy losses and co-products (biofuels only)",
                "value": "energy losses and co-products (biofuels only)",
            },
        ],
    }
]


def get_allCategories_for(node, allNodes):
    allNodes.append(node['key'])

    if "children" in node:
        for child in node["children"]:
            get_allCategories_for(child, allNodes)

    return allNodes

def get_state_name(code):
    if code == 'US':
        return 'USA'
    else:
        return states_dict[code]



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
hierarchy_list_energy_types = create_hierarchy_list(energy_categories_types[0])
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
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
}

state_coordinates = {
    "HI": (0, 1),
    "FL": (16, 1),
    "TX": (7, 2),
    "GA": (15, 2),
    "NM": (6, 3),
    "OK": (8, 3),
    "LA": (10, 3),
    "MS": (12, 3),
    "AL": (14, 3),
    "SC": (16, 3),
    "CA": (3, 4),
    "AZ": (5, 4),
    "UT": (7, 4),
    "KS": (9, 4),
    "AR": (11, 4),
    "TN": (13, 4),
    "VA": (15, 4),
    "NC": (17, 4),
    "OR": (2, 5),
    "NV": (4, 5),
    "CO": (6, 5),
    "NE": (8, 5),
    "MO": (10, 5),
    "KY": (12, 5),
    "WV": (14, 5),
    "MD": (16, 5),
    "DE": (18, 5),
    "DC": (20, 5),
    "ID": (3, 6),
    "WY": (5, 6),
    "SD": (7, 6),
    "IA": (9, 6),
    "IL": (11, 6),
    "IN": (13, 6),
    "OH": (15, 6),
    "PA": (17, 6),
    "NJ": (19, 6),
    "CT": (21, 6),
    "WA": (2, 7),
    "MT": (4, 7),
    "ND": (6, 7),
    "MN": (8, 7),
    "WI": (10, 7),
    "MI": (14, 7),
    "NY": (18, 7),
    "MA": (20, 7),
    "RI": (22, 7),
    "VT": (19, 8),
    "NH": (21, 8),
    "AK": (0, 9),
    "ME": (22, 9),
}


def calculate_avg_value(df, state_code, date_range, variable):
    """Calculate the average value of a variable for a given state and date range.

    Args:
        df (pandas.DataFrame): The data frame containing the data.
        state_code (str): The state code for which the average value should be calculated.
        date_range (list): The date range for which the average value should be calculated.
        variable (str): The variable for which the average value should be calculated.

    Returns:
        float: The average value of the variable for the given state and date range.
    """

    # Filter the data frame by state code, date range and variable

    # Filtering not properly working
    filtered_data = flt.filterByValues(state_code)
    # df_filtered = df[
    #     (df["state_code"] == state_code)
    #     & (df["date"].isin(date_range))
    #     & (df["variable"] == variable)
    # ]
    # Calculate the average value
    avg_value = filtered_data["value"].mean()
    # Return the average value
    return avg_value


def calculate_percantage_deviation_from_avg(df, state_code, date_range, variable):
    """Calculate the percentage deviation of a variable for a given state and date range from the average value.

    Args:
        df (pandas.DataFrame): The data frame containing the data.
        state_code (str): The state code for which the percentage deviation should be calculated.
        date_range (list): The date range for which the percentage deviation should be calculated.
        variable (str): The variable for which the percentage deviation should be calculated.

    Returns:
        float: The percentage deviation of the variable for the given state and date range from the average value.
    """
    # Calculate the average value
    avg_value = calculate_avg_value(df, state_code, date_range, variable)
    # Filter the data frame by state code, date range and variable
    df_filtered = df[
        (df["state_code"] == state_code)
        & (df["date"].isin(date_range))
        & (df["variable"] == variable)
    ]
    # Calculate the percentage deviation
    percentage_deviation = (df_filtered["value"].mean() - avg_value) / avg_value * 100
    # Return the percentage deviation
    return percentage_deviation


state_codes = list(states_dict.keys())
# Create a DataFrame from the dictionary
df_states = pd.DataFrame(
    list(states_dict.items()), columns=["StateCode", "full_state_name"]
)
