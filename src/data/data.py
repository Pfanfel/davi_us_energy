from helpers import filter as flt
import pandas as pd
import geopandas as gpd
from shapely import wkt


import geopandas as gpd
import pandas as pd

stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

min_energy_data, max_energy_data = stads_df["Data"].min(), stads_df["Data"].max()

min_energy_GDP, max_energy_GDP = (
    stads_df["EnergyPerGDP"].min(),
    stads_df["EnergyPerGDP"].max(),
)
min_energy_PerCapita, max_energy_PerCapita = (
    stads_df["EnergyPerCapita"].min(),
    stads_df["EnergyPerCapita"].max(),
)


geoData = gpd.read_file("data/us_states_hexgrid.geojson.json")
geoData["geometry"] = geoData["geometry"].simplify(tolerance=0.01)
col_to_del_geo = [
    "cartodb_id",
    "created_at",
    "updated_at",
    "label",
    "bees",
    "google_name",
]
geoData.drop(columns=col_to_del_geo, inplace=True)

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
    ],
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
    "marker_colors": [
        "#E0ECED",
        "#C8A3D9",
        "#DD9DC6",
        "#E19FAA",
        "#FDB883",
        "#7CA460",
        "#96AF5E",
        "#A3C166",
        "#8CD891",
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
    "marker_colors": [
        "#E0ECED",
        "#C096BE",
        "#C8A3D9",
        "#DD9DC6",
        "#E19FAA",
        "#FDB883",
        "#7CA460",
        "#23BAA3",
        "#4FB88A",
        "#62D39F",
        "#8ACF84",
        "#72D0A5",
        "#89BD8F",
        "#6CC0A2",
        "#76B571",
        "#96AF5E",
        "#B1A859",
        "#38a8c5",
        "#e7de9e",
    ],
}


production = [
    {
        "title": "total energy production",
        "key": "TEPRB",
        "value": "TEPRB",
        "color": "#E0ECED",
        "children": [
            {
                "title": "production of coal",
                "key": "CLPRB",
                "value": "CLPRB",
                "color": "#C8A3D9",
            },
            {
                "title": "production of natural gas",
                "key": "NGMPB",
                "value": "NGMPB",
                "color": "#DD9DC6",
            },
            {
                "title": "production of petroleum",
                "key": "PAPRB",
                "value": "PAPRB",
                "color": "#E19FAA",
            },
            {
                "title": "production of nuclear electric power",
                "key": "NUEGB",
                "value": "NUEGB",
                "color": "#FDB883",
            },
            {
                "title": "production of renewable energy",
                "key": "REPRB",
                "value": "REPRB",
                "color": "#7CA460",
                "children": [
                    {
                        "title": "production of biofuels",
                        "key": "BFPRB",
                        "value": "BFPRB",
                        "color": "#96AF5E",
                    },
                    {
                        "title": "production of wood and waste",
                        "key": "WWPRB",
                        "value": "WWPRB",
                        "color": "#A3C166",
                    },
                    {
                        "title": "other production",
                        "key": "NCPRB",
                        "value": "NCPRB",
                        "color": "#8CD891",
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
        "color": "#E0ECED",
        "children": [
            {
                "title": "consumption of fossil fuels",
                "key": "FFTCB",
                "value": "FFTCB",
                "color": "#C096BE",
                "children": [
                    {
                        "title": "consumption of coal",
                        "key": "CLTCB",
                        "value": "CLTCB",
                        "color": "#C8A3D9",
                    },
                    {
                        "title": "consumption of natural gas",
                        "key": "NNTCB",
                        "value": "NNTCB",
                        "color": "#DD9DC6",
                    },
                    {
                        "title": "consumption of petroleum",
                        "key": "PMTCB",
                        "value": "PMTCB",
                        "color": "#E19FAA",
                    },
                ],
            },
            {
                "title": "consumption of nuclear electric power",
                "key": "NUETB",
                "value": "NUETB",
                "color": "#FDB883",
            },
            {
                "title": "consumption of renewable energy",
                "key": "RETCB",
                "value": "RETCB",
                "color": "#7CA460",
                "children": [
                    {
                        "title": "consumption of hydroelectric power",
                        "key": "HYTCB",
                        "value": "HYTCB",
                        "color": "#23BAA3",
                    },
                    {
                        "title": "consumption of biomass",
                        "key": "BMTCB",
                        "value": "BMTCB",
                        "color": "#4FB88A",
                        "children": [
                            {
                                "title": "consumption of wood and waste",
                                "key": "WWTCB",
                                "value": "WWTCB",
                                "color": "#62D39F",
                            },
                            {
                                "title": "consumption of ethanol",
                                "key": "EMTCB",
                                "value": "EMTCB",
                                "color": "#8ACF84",
                            },
                            {
                                "title": "consumption of biodiesel",
                                "key": "BDTCB",
                                "value": "BDTCB",
                                "color": "#72D0A5",
                            },
                            {
                                "title": "consumption of renewable diesel",
                                "key": "B1TCB",
                                "value": "B1TCB",
                                "color": "#89BD8F",
                            },
                            {
                                "title": "energy losses and co-products",
                                "key": "EMLCB",
                                "value": "EMLCB",
                                "color": "#6CC0A2",
                            },
                        ],
                    },
                    {
                        "title": "consumption of geothermal energy",
                        "key": "GETCB",
                        "value": "GETCB",
                        "color": "#76B571",
                    },
                    {
                        "title": "consumption of solar energy",
                        "key": "SOTCB",
                        "value": "SOTCB",
                        "color": "#96AF5E",
                    },
                    {
                        "title": "consumption of wind energy",
                        "key": "WYTCB",
                        "value": "WYTCB",
                        "color": "#B1A859",
                    },
                ],
            },
            {
                "title": "consumption of interstate flow of electricity",
                "key": "ELISB",
                "value": "ELISB",
                "color": "#38a8c5",
            },
            {
                "title": "consumption of electricity net imports",
                "key": "ELNIB",
                "value": "ELNIB",
                "color": "#e7de9e",
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


def get_allCategories_for(node, allNodes):
    allNodes.append(node["key"])

    if "children" in node:
        for child in node["children"]:
            get_allCategories_for(child, allNodes)

    return allNodes


def get_state_name(code):
    if code == "US":
        return "USA"
    else:
        return states_dict[code]


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
