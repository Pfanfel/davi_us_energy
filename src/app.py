import json
import operator
from functools import reduce
from typing import Union

import dash_table
import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

# Incorporate data
df = pd.read_csv("data/stads_data_parsed_cleaned_pop_gdp_v1.csv")

fake_data = {
    "Top Level": [
        "Total energy consumption",
        "Total energy production",
    ],
    "Total energy production": [
        "Fossil fuel",
        "Nuclear energy power",
        "Renewable energy power"
    ],
    "Total energy consumption": [
        "Fossil fuel",
        "Nuclear energy power",
        "Renewable energy power"
    ],
    "Fossil fuel": [
        "Coal",
        "Natural gas",
        "Petroleum"
    ],
    "Renewable energy power": [
        "Hydroelectric power",
        "Biomass"
    ],
    "Biomass": [
        "Wood and waste",
        "Fuel ethanol",
        "Biodiesel",
        "Renewable diesel"
    ]
}

# Store the state of the categories
category_state = {category: False for category in fake_data.keys()}

def set_className_entry(original_className, className_to_toggle, return_has_className=True):
    """
    Sets/unsets a className within a space separated list of classNames

    If return_has_className=True, the returned className will include exactly one of className_to_toggle.
    If return_has_className=False, the returned className will include exactly none of className_to_toggle.

    Returns:
        (str): Updated className
    """
    name_list = original_className.strip().split()

    # Remove all of className in question
    name_list = [x for x in name_list if x != className_to_toggle]

    if return_has_className:
        name_list.append(className_to_toggle)

    return " ".join(name_list)

def get_className_state(full_className, className_to_check):
    name_list = full_className.strip().split()
    return className_to_check in name_list


def generate_checklist_ul_id(path):
    return {"type": "unordered_list", "id": "_".join(path)}


def get_path_to_id_in_serialized_ul(ul: dict, obj_id: str, _upstream_path=None):
    """
    Depth first search of a dict of Plotly objects with children, returning the path to the first obj with the id obj_id
    Args:
        ul (dict):
        obj_id:  Any valid Plotly object id (str, dict)
        _upstream_path: Used for recursion.  Typically should not be defined externally
    Returns:
        (tuple): a tuple defining all steps taken in the ul children dict to get to the item, eg:
                    (index_lvl_1, key_lvl_2, ...)
    """
    _upstream_path = tuple() if not _upstream_path else _upstream_path

    for i, child in enumerate(ul):
        # Iterate on objects in children list.  These will have {'props', 'type'}, with 'props' having 'id' and
        # 'children'
        this_upstream_path = _upstream_path + (i,)
        if child['props']['id'] == obj_id:
            return this_upstream_path
        else:
            # If there are children, go deeper
            if isinstance(child['props']['children'], (tuple, list)):
                returned_from_child = get_path_to_id_in_serialized_ul(child['props']['children'],
                                                                      obj_id,
                                                                      _upstream_path=this_upstream_path + ('props',
                                                                                                           'children'))
                if returned_from_child:
                    return returned_from_child

    # Nothing found, return None
    return None

def get_by_path(obj, path):
    return reduce(operator.getitem, path, obj)

def get_leaves_below_sidebar_obj(ul_children: dict, path_to_obj: Union[str, tuple, list] = None):
    """
    Get all leaf nodes (Li objects without corresponding Ul) from a dict defining the children of a Ul
    Args:
        ul_children: Children attribute of a Ul object, defined as a dictionary. Same format as Dash passes to a
                     callback watching the "children" attribute of a Ul.
        path_to_obj: A tuple of keys and indices defining where to start within ul_children when looking for children.
                     For example:
                        (index_lvl_1, key_lvl_2, ...)
                     The same as returned by get_path_to_id_in_serialized_ul()
    Returns:
        (list): List of references to the leaves found in ul_children (if mutated in place, they will change the
                ul_children instance)
    """
    # Traverse the children of this object, returning any child Li objs that have no paired Ul or any leaves of nested Uls
    if path_to_obj is None:
        path_to_obj = ()

    if not isinstance(path_to_obj, (tuple, list)):
        path_to_obj = (path_to_obj,)

    # Helper function to check if an object is a leaf Li
    def is_leaf(obj):
        return obj['type'] == 'Li'

    def traverse(obj, current_path):
        to_return = []

        for i, child in enumerate(obj):
            child_path = current_path + (i,)

            # Check if the child is a leaf Li
            if is_leaf(child):
                to_return.append(child)
            else:
                # If there are children, go deeper
                if 'props' in child and 'children' in child['props']:
                    to_return.extend(traverse(child['props']['children'], child_path))

        return to_return

    return traverse(ul_children, path_to_obj)


def generate_checklist_li_id(path):
    return {"type": "list_item", "id": "_".join(path)}

def make_sidebar_children(data, top_item, inherited_class="", child_class="", path=None):
    """
    Recursively generate a hierarchical list defined by data, starting at top_item, using Ul and Li objects
    Ul and Li objects ids are defined by Dash id dicts so they can be subscribed to by a callback as a group
    For each node, we generate:
        * An Li object with children=item_name
        * (If node is a middle node with additional children) a Ul object with children=[child_nodes, built recursively]
    Args:
        data (dict): Dict of lists of relationships within the nested list.  For example:
                        {
                            "Item-1": ["Item-1-1", "Item-1-2", ...],
                            "Item-2": ["Item-2-1", "Item-2-2", ...],
                            "Item-1-1": ["Item-1-1-1", "Item-1-1-2", ...],
                            ...
                        }
                     Note that this does not handle repeated names (eg: Item-1-1 cannot have the same name as Item-2)
        top_item (str): The key in data that denotes the head of the hierarchy to generate
        inherited_class (str): HTML class name to apply once to all levels of the list
        child_class (str): HTML class name to apply once per step in the list (so Item 1-1 would have it once,
                           Item 1-1-1 would have it twice, etc.).  Useful for incrementing tab behaviour
        path (list): List representing the path to the current element in the hierarchy
    Returns:
        (list): List of html elements for use as the children attribute of a html.Ul
    """
    this_className = f"{inherited_class} {child_class}"
    content = []

    path = path or []

    for name in data[top_item]:
        leaf_id = generate_checklist_li_id(path + [name])
        content.append(html.Li(
            children=name,
            id=leaf_id,
            className=this_className,
        ))

        if name in data:
            nested_children = make_sidebar_children(data, name, inherited_class=this_className, child_class=child_class, path=path + [name])
            content.append(html.Ul(
                id=generate_checklist_ul_id(path + [name]),
                children=nested_children,
            ))

    return content


def make_sidebar_ul(data, top_item, inherited_class="", child_class=""):
    """
    Returns a sidebar defined using a html.Ul with nested Li and Ul elements
    Optionally can have class names applied recursively to each level of child within the list (eg: for formatting)
    Args:
        See make_sidebar_children
    Returns:
        (html.Ul)
    """
    children = make_sidebar_children(data=data, top_item=top_item, inherited_class=inherited_class, child_class=child_class)

    ul = html.Ul(id="sidebar-ul",
                 children=children,
                 )
    return ul


@app.callback(
    Output("sidebar-ul", "children"),
    [Input({"type": "list_item", "id": ALL}, 'n_clicks')],
    [State("sidebar-ul", "children")]
)
def register_sidebar_list_click(n_clicks, ul_children):
    if dash.callback_context.triggered:
        clicked_li_id = json.loads(dash.callback_context.triggered[0]['prop_id'].split('.')[0])
    else:
        raise dash.exceptions.PreventUpdate()

    # Use the ul_children object as the state for the list. Work on it directly by grabbing references to its mutable
    # components and modifying to form the returned object.

    clicked_li_id_name = clicked_li_id['id']
    paired_ul_id = generate_checklist_ul_id(clicked_li_id_name)

    # Determine whether the clicked Li is a leaf node or a header node that has children by looking for a Ul with a
    # common id
    paired_ul_path = get_path_to_id_in_serialized_ul(ul_children, paired_ul_id)

    if paired_ul_path:
        # Header clicked, get children under this.
        leaves = get_leaves_below_sidebar_obj(ul_children, paired_ul_path)
    else:
        # Leaf clicked, get only the clicked li
        clicked_li_path = get_path_to_id_in_serialized_ul(ul_children, clicked_li_id)
        leaves = [get_by_path(ul_children, clicked_li_path)]

    # Determine whether to click or unclick all leaves
    checked_status = get_leaves_checked_status(leaves)
    new_status = not all(checked_status)

    # Update the state of the clicked category and its children
    category_state[clicked_li_id_name] = new_status

    # Apply new status to leaves
    for leaf in leaves:
        leaf['props']['className'] = set_className_entry(leaf['props']['className'], "checked", new_status)
        leaf['props']['style'] = {'color': 'green' if new_status else 'black'}

    return ul_children


def get_leaves_checked_status(leaves):
    checked_status = []
    for leaf in leaves:
        this_className = leaf['props']['className']
        checked_status.append(get_className_state(this_className, "checked"))
    return checked_status

def get_leaf_ids(leaves):
    return [leaf['props']['id']['id'] for leaf in leaves]

def get_checked_leaves(leaves):
    checked_status = get_leaves_checked_status(leaves)
    leaf_ids = get_leaf_ids(leaves)
    return [leaf_id for leaf_id, checked in zip(leaf_ids, checked_status) if checked]

@app.callback(
    Output("checked-items-p", "children"),
    [Input("sidebar-ul", "children")],
)
def watch_sidebar_children(ul_children):
    leaves = get_leaves_below_sidebar_obj(ul_children, path_to_obj=tuple())
    checked_leaves = get_checked_leaves(leaves)
    return ", ".join(checked_leaves)

# Define the dash app layout
app.layout = html.Div(
    [
html.Div(
            children="Awesome Data Visualization for US Energy Production and Consumption by State"
        ),
        html.Div(id='checked-items',
                         children=[
                             html.H1("Selected categories"),
                             html.P(id="checked-items-p")
                         ]),
        html.Div(id="sidebar-div",
                 children=make_sidebar_ul(fake_data,
                                          "Top Level",
                                          )
                 ),
        dash_table.DataTable(data=df.to_dict("records"), page_size=10),
    ]
)

if __name__ == '__main__':
    # Hacky way to auto pick a port
    ports = range(8850, 8860, 1)
    for port in ports:
        try:
            print(f"TRYING PORT {port}")
            app.run_server(debug=True, port=port)
        except OSError:
            continue
        break
