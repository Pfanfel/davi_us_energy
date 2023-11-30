"""
This file is used to load data from the data folder and perform any data manipulation that is needed during the lifecycle of the app.
"""

# Import Pandas
import pandas as pd

import geopandas as gpd

from helpers import filter as flt

stads_df = pd.read_csv(
    # import stads_data_parsed_cleaned_pop_gdp_v1.csv from the same folder
    "data/stads_data_parsed_cleaned_pop_gdp_v1.csv",
)

# Load the data and transform the data with the centroid function
geo_data_us_states_hexgrid = gpd.read_file("data/us_states_hexgrid.geojson.json")


production_hirarchie_icicle = {
    "parents": [
        "",
        "total energy production",
        "total energy production",
        "total energy production",
        "total energy production",
        "total energy production",
        "renewable energy",
        "renewable energy",
        "renewable energy",
    ],
    "labels": [
        "total energy production",
        "coal",
        "natural gas, including supplemental gaseous fuels",
        "natural gas, excluding supplemental gaseous fuels",
        "nuclear electric power",
        "renewable energy",
        "biofuels",
        "wood and waste",
        "other",
    ],
}


consumption_hirarchie_icicle = {
    "parents": [
        "",
        "total energy consumption",
        "fossil fuels",
        "fossil fuels",
        "fossil fuels",
        "total energy consumption",
        "total energy consumption",
        "renewable energy",
        "renewable energy",
        "biomass",
        "biomass",
        "biomass",
        "biomass",
        "biomass",
        "renewable energy",
        "renewable energy",
        "renewable energy",
        "total energy consumption",
        "total energy consumption",
    ],
    "labels": [
        "total energy consumption",
        "fossil fuels",
        "coal",
        "natural gas, including supplemental gaseous fuels",
        "natural gas, excluding supplemental gaseous fuels",
        "nuclear electric power",
        "renewable energy",
        "hydroelectric power",
        "biomass",
        "wood and waste",
        "fuel ethanol, excluding denaturant",
        "biodiesel",
        "renewable diesel",
        "energy losses and co-products (biofuels only)",
        "geothermal energy",
        "photovoltaic and solar thermal energy",
        "wind",
        "interstate flow (electricity only)",
        "net imports",
    ],
}

# Hardcoded list of values for a ui element

col_names = ["energy_type", "energy_activity"]
production = [
    {
        "title": "total energy production",
        "key": "production",
        "value": "production",
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
            {
                "title": "nuclear electric power",
                "key": "nuclear electric power",
                "value": "nuclear electric power",
            },
            {
                "title": "renewable energy",
                "key": "renewable energy",
                "value": "renewable energy",
                "children": [
                    {"title": "biofuels", "key": "biofuels", "value": "biofuels"},
                    {
                        "title": "wood and waste",
                        "key": "wood and waste",
                        "value": "wood and waste",
                    },
                    {
                        "title": "other",
                        "key": "renewable_energy_other",
                        "value": "renewable_energy_other",
                    },
                ],
            },
        ],
    }
]


consumption = [
    {
        "title": "total energy consumption",
        "key": "total_energy_consumption",
        "value": "total_energy_consumption",
        "children": [
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
                "title": "renewable energy",
                "key": "renewable energy",
                "value": "renewable energy",
                "children": [
                    {
                        "title": "hydroelectric power",
                        "key": "hydroelectric power",
                        "value": "hydroelectric power",
                    },
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
                            {
                                "title": "biodiesel",
                                "key": "biodiesel",
                                "value": "biodiesel",
                            },
                            {
                                "title": "renewable diesel",
                                "key": "renewable diesel",
                                "value": "renewable diesel",
                            },
                            {
                                "title": "energy losses and co-products (biofuels only)",
                                "key": "energy losses and co-products (biofuels only)",
                                "value": "energy losses and co-products (biofuels only)",
                            },
                        ],
                    },
                    {
                        "title": "geothermal energy",
                        "key": "geothermal energy",
                        "value": "geothermal energy",
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
                "title": "interstate flow (electricity only)",
                "key": "interstate flow (electricity only)",
                "value": "interstate flow (electricity only)",
            },
            {"title": "net imports", "key": "net imports", "value": "net imports"},
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

    print(f"state_code: {state_code}, date_range: {date_range}, variable: {variable}")
    # Filter the data frame by state code, date range and variable

    # Filtering not properly working
    filtered_data = flt.filterByValues(state_code)
    print(f"filtered_data: {filtered_data}")
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
# print(state_codes)
# Create a DataFrame from the dictionary
df_states = pd.DataFrame(
    list(states_dict.items()), columns=["StateCode", "full_state_name"]
)
