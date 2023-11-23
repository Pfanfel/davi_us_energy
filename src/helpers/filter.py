import Levenshtein


def find_root_node(tree, target_title):
    for node in tree:
        if node["title"] == target_title:
            print(f"Root node was found {node['key']}")
            return node["key"]
        if "children" in node:
            result = find_root_node(node["children"], target_title)
            if result is not None:
                return result
    return None


def get_category_value_and_level(category_key, tree, current_level=0):
    for node in tree:
        if node["key"] == category_key:
            return find_level(tree, node["key"]), current_level
        if "children" in node:
            child_value, child_level = get_category_value_and_level(
                category_key, node["children"], current_level + 1
            )
            if child_value is not None:
                return child_value, child_level
    return None, None


def find_level(tree, category, current_level=0):
    for node in tree:
        if node["key"] == category:
            return current_level
        if "children" in node:
            level = find_level(node["children"], category, current_level + 1)
            if level is not None:
                return level
    return None

def get_all_categories_at_same_level(category, tree):
    target_level = find_level(tree, category)
    if target_level is None:
        return None, []  # Category not found

    categories = []

    def traverse_and_collect(node, current_level):
        if current_level == target_level:
            categories.append(node["key"])

        if "children" in node:
            for child in node["children"]:
                traverse_and_collect(child, current_level + 1)

    for node in tree:
        traverse_and_collect(node, 0)

    return target_level, categories





def get_all_children_of_category(category, tree):
    children = []

    def traverse_and_collect_children(node):
        nonlocal category, children

        if node["key"] == category:
            if "children" in node:
                children.extend(child["key"] for child in node["children"])

        if "children" in node:
            for child in node["children"]:
                traverse_and_collect_children(child)

    for node in tree:
        traverse_and_collect_children(node)

    return children


def filterData(chosen_categories, data, category_to_filter):
    filter_condition = data[category_to_filter].isin(chosen_categories)
    filtered_data = data[filter_condition]
    return filtered_data if not filtered_data.empty else data


def filterByValue(value_to_filter, df):
    filtered = df[df.eq(value_to_filter).any(axis=1)]
    return filtered if not filtered.empty else df



def filterByValues(values_to_filter, df):
    mask = df.isin(values_to_filter).any(axis=1)
    filtered = df[mask]
    return filtered if not filtered.empty else df


def getUniqueValuesOf(columnName, dataframe):
    return dataframe[columnName].unique()


def getProperColumnValue(selectedCategory):
    return selectedCategory.lower()


def find_closest_string(target, string_list):
    return min(string_list, key=lambda x: Levenshtein.distance(target, x))



def getClosestColumnValueTo(selectedCategory, possibleColumnValues):
    return min(possibleColumnValues, key=lambda x: Levenshtein.distance(selectedCategory, x))


def find_column_name(df, target_value):
    for column in df.columns:
        if target_value in df[column].values:
            return column
    return None


def filter_dataframe_by_tree(df, tree, parent_condition=None, level=0):
    if not tree:
        return df

    current_level_nodes = [node for node in tree if find_level(tree, node["key"]) == level]
    condition = parent_condition

    for node in current_level_nodes:
        key = node["key"]
        column_name = find_column_name(df, key)

        if column_name is not None:
            if condition is None:
                condition = (df[column_name] == key)
            else:
                condition &= (df[column_name] == key)

            if "children" in node:
                condition &= filter_dataframe_by_tree(df, node["children"], condition, level + 1)

    return df[condition]
