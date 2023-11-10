"""
This file is used to load data from the data folder and perform any data manipulation that is needed during the lifecycle of the app.
"""

# Import Pandas
import pandas as pd

stads_df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

pop_by_year_df = pd.read_csv("data/pop_year.csv")

gdp_by_year_df = pd.read_csv("data/gdp_year.csv")

# Hardcoded list of values for a ui element
# ui_element_values = [1,2,3,...]


# For derived values or values that need to be calculated from the data
def some_calculation(param1, param2):
    return param1 + param2
