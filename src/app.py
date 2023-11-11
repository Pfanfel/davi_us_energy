# Import packages
from dash import Dash, html, dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from components import navbar, footer
import feffery_antd_components as fac
import pandas as pd
from dash import Input, Output, State, ALL
from src.helpers.filter import find_root_node, filterData
from src.data import data




# Initialize the app
app = dash.Dash(
    __name__,
    use_pages=True,  # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],  # fetch the proper css items we want
    meta_tags=[
        {  # check if device is a mobile device. This is a must if you do any mobile styling
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
        }
    ],
    suppress_callback_exceptions=True,
    title="🇺🇸 Awesome Data Visualization for US Energy Production and Consumption by State",
)


@app.callback(
    Output('stads_id', 'data'),
    Input(data.col_names[0], 'value'),
    Input(data.col_names[1], 'value'),
    Input('stads_id', 'data'),
    prevent_initial_call=True
)
def handle_select_event_energy_type(selected_energy_types, selected_energy_activity, current_data):
    current_data_df = pd.DataFrame(current_data)  # Convert the data to a DataFrame

    if not selected_energy_types and not selected_energy_activity:
        return current_data_df.to_dict('records')  # No categories selected, return the current data as is

    filtered_data = current_data_df.copy()  # Make a copy of the current data

    if selected_energy_types:
        filtered_data = filterData(selected_energy_types, filtered_data, data.col_names[0])

    if selected_energy_activity:
        filtered_data = filterData(selected_energy_activity, filtered_data, data.col_names[1])

    return filtered_data.to_dict('records')

def CreateCategoryFilteringTree(categories, id, placeHolder):
    return fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
    )



# define the navbar and footer
nav = navbar.Navbar()
footer = footer.Footer()

data_table = dash_table.DataTable(
    id='stads_id',
    data=data.stads_df.to_dict('records'),
    page_size=10,  # Number of rows per page
    page_current=0,  # Current page
)

#define the energy_types filter

energy_types_filter = CreateCategoryFilteringTree(data.energy_categories_types, data.col_names[0], "Select Energy Type")
energy_types_filter.className = "category-tree"
energy_activity_filter = CreateCategoryFilteringTree(data.energy_activities, data.col_names[1],"Select Energy Activity")
energy_activity_filter.className = "category-tree"


# set the main layout
app.layout = html.Div(
    [
        nav,
        html.Div([energy_types_filter, html.Div(style={'width': '20px'}), energy_activity_filter],
                 style={'display': 'flex'}),
        data_table,
        footer,
    ]
)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
