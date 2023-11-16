import feffery_antd_components as fac
from dash import html


def CreateCategoryFilteringTree(categories, id, placeHolder):
    antd_tree_selector = fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
        style={"width": "auto"},  # Set the width to 'auto'
    )

    return html.Div(
        children=[antd_tree_selector],
        className="pretty_container",
    )
