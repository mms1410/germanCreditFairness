from sklearn.datasets import fetch_openml
import pandas as pd


def get_german_credit():

    german_credit = fetch_openml(name="credit-g", version=1, as_frame=True)
    credit = german_credit.frame

    to_category = ["num_dependents", "existing_credits", "residence_since", "installment_commitment"]
    for column_name in to_category:
        credit[column_name] = credit[column_name].astype("category")
    
    return credit

def set_equal(list1:list, list2:list) -> bool:

    return set(list1) == set(list2)

def assert_categories(data:pd.DataFrame, column_name:str, expected_categories:list[str]) -> None:


    assert column_name in data.columns, f"Column '{column_name}' not found."
    col_to_check = data.loc[:, column_name]  # should return a Series that has .unique()

    assert isinstance(col_to_check, pd.Series), f"Need a Series object for further checks, got {type(col_to_check)}."
    actual_categories = list(col_to_check.unique())
    
    assert set_equal(actual_categories, expected_categories), f"Expected categories {expected_categories} but got {actual_categories}."


if __name__ == "__main__":
    data = get_german_credit()
    credit = data.frame
    expected_categories = ["<0", "0<=X<200", ">=200", "no checking"]
    assert_categories(credit, "checking_status", expected_categories)
