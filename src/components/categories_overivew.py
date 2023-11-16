import feffery_antd_components as fac
from dash import html

def CreateCategoryFilteringTree(categories, id, placeHolder, defaultSelected=[]):
    antd_tree_select = fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
        defaultValue=defaultSelected,
    )
    return html.Div(
        children=[html.H4(placeHolder), antd_tree_select],
        className="pretty_container",
    )
