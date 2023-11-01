# Import packages
from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
        html.Div(
            children="Awsome Data Visualization for US Energy Production and Consumption by State"
        ),
        dash_table.DataTable(data=df.to_dict("records"), page_size=10),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
