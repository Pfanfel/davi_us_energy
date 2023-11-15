import feffery_antd_components as fac


def CreateCategoryFilteringTree(categories, id, placeHolder):
    return fac.AntdTreeSelect(
        id=id,
        treeData=categories,
        multiple=True,
        treeCheckable=True,
        treeLine=True,
        treeDefaultExpandAll=True,
        placeholder=placeHolder,
        style={'width': 'auto'}  # Set the width to 'auto'
    )
