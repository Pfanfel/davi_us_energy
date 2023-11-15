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


def getAllCategoriesValuesAtTheSameLevel(chosen_category_value, tree):
    level_value = 0
    for node in tree:
        if node["key"] == chosen_category_value:
            level_value = node["value"]
    all_neighbors = []
    for node in tree:
        if node["value"] == level_value:
            all_neighbors.append(node["key"])
    return all_neighbors


def getAllChildrenFromCategoryValue(chosen_category_value, tree):
    level_value = 0
    for node in tree:
        if node["key"] == chosen_category_value:
            return node["children"]


def filterData(chosen_categories, data, category_to_filter):
    filter_condition = None
    for cat in chosen_categories:
        condition = data[category_to_filter] == cat
        if filter_condition is None:
            filter_condition = condition
        else:
            filter_condition |= condition
    return data[filter_condition]


def filterByValue(value_to_filter, df):
    data = df.copy()
    filtered = df[df.eq(value_to_filter).any(axis=1)]
    if filtered is []:
        return data
    else:
        return filtered


def filterByValues(values_to_filter, df):
    data = df.copy()
    mask = df.isin(values_to_filter).any(axis=1)
    filtered = df[mask]

    if filtered.empty:
        return data
    else:
        return filtered


def getUniqueValuesOf(columnName, dataframe):
    energy_types = dataframe[columnName].unique()
    unique_values_list = energy_types.tolist()
    return unique_values_list


def getProperColumnValue(selectedCategory):
    return selectedCategory.lower()


def find_closest_string(target, string_list):
    closest_string = min(string_list, key=lambda x: Levenshtein.distance(target, x))
    return closest_string


def getClosestColumnVaueTo(selectedCategory, possibleColumnValues):
    return find_closest_string(selectedCategory, possibleColumnValues)
