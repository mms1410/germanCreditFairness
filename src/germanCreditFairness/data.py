from sklearn.datasets import fetch_openml
import pandas as pd


def snake_to_camel(snake_string: str) -> str:
    """Turn snake case string into camel case string."""
    parts = snake_string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def get_german_credit():

    german_credit = fetch_openml(name="credit-g", version=1, as_frame=True)
    credit = german_credit.frame

    to_category = ["num_dependents", "existing_credits", "residence_since", "installment_commitment"]
    for column_name in to_category:
        credit[column_name] = credit[column_name].astype("category")
    
    credit.rename(columns = lambda col: snake_to_camel(col), inplace = True)

    return credit

def set_equal(list1:list, list2:list) -> bool:

    return set(list1) == set(list2)

def assert_categories(data:pd.DataFrame, column_name:str, expected_categories:list[str]) -> None:


    assert column_name in data.columns, f"Column '{column_name}' not found."
    col_to_check = data.loc[:, column_name]  # should return a Series that has .unique()

    assert isinstance(col_to_check, pd.Series), f"Need a Series object for further checks, got {type(col_to_check)}."
    actual_categories = list(col_to_check.unique())
    
    assert set_equal(actual_categories, expected_categories), f"Expected categories {expected_categories} but got {actual_categories}."