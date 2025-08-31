import pandas as pd
import germanCreditFairness.decision_functions as decision_functions
from pathlib import Path
import inspect
import yaml
from itertools import product
import numpy as np


ROOT = Path(__file__).resolve().parent.parent.parent
PATH_ASSETS =  ROOT / Path("assets")
PATH_CONF = ROOT / Path("conf")
DECISIONS_YAML = ROOT / Path("conf") / Path("decisions.yaml")
TRAIN_YAML = ROOT / Path("conf") / Path("train.yaml")

IMPLEMENTED_FUNCTIONS = [name for name, _ in inspect.getmembers(decision_functions, inspect.isfunction)]



def get_active_columns(new_column_names: list[str], old_column_name: list[str]) -> list[str]:
    pass

def get_required_args(func_name):
    """
    Returns a list of required argument names for a function.
    """
    if not hasattr(decision_functions, func_name):
        raise AttributeError(f"Function '{func_name}' not found in scriptA")

    func = getattr(decision_functions, func_name)
    sig = inspect.signature(func)

    required_params = [
        name for name, param in sig.parameters.items()
        if param.default == inspect.Parameter.empty
    ]
    
    return required_params

def call_function_by_name(func_name: str, args: dict = None):
    """
    Call a function by the string representation of its name.
    """
    if not hasattr(decision_functions, func_name):
        raise AttributeError(f"Function {func_name} not found in decision_functions.py")
    
    func = getattr(decision_functions, func_name)
    args = args or {}  # default to empty dict    
    
    return func(**args)   # unpack dict as kwargs




def snake_to_camel(snake_string: str) -> str:
    """Turn snake case string into camel case string."""
    parts = snake_string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def  check_function_exists(function_name: str) -> bool:

    return function_name in IMPLEMENTED_FUNCTIONS

def yaml_to_dictionary(path:str | Path = DECISIONS_YAML) -> dict:

    with path.open("r") as f:
        dictionary =  yaml.safe_load(f)
        dictionary = {snake_to_camel(k): v for k,v in dictionary.items()}

    return dictionary

def flatten_dict(dictionary):

    flattened = [(k,v) for k, values in dictionary.items() for v in values]

    return flattened

def flatten(item: list, acc = []):
    """
    Consume the list from left to right until empty.
    Accumulator is extended with flattened dictionary but appended with single element list because
    a single string would be extended character by charcter.
    """
    while item: # true if not empty
        head = item.pop(0)
        if isinstance(head, dict):
            acc.extend(flatten_dict(head))
        else:
            acc.append(head)
    return acc        

def dictionary_to_frame(decision_dict:dict) -> pd.DataFrame:
    df = pd.DataFrame()
    for covariate, entry in decision_dict.items():
        flat_list = flatten(entry, [])
        frame = pd.DataFrame([{"covariate": snake_to_camel(covariate), "category": "default", "decision": ""}])
        df = pd.concat([df, frame], ignore_index = True)
        for item in flat_list:
            if isinstance(item, tuple):
                frame = pd.DataFrame([{"covariate": snake_to_camel(covariate), "category": item[0], "decision": item[1]}])
            else:
                frame = pd.DataFrame([{"covariate": snake_to_camel(covariate),"category": item, "decision": ""}])
            df = pd.concat([df,frame], ignore_index = True)
    return df


def combine_category_decision(decision_frame: pd.DataFrame) -> pd.DataFrame:

    def func(row):
        decision = row["decision"]
        category = row["category"]
        if decision == "":
            return category
        else:
            return category + "_" + decision

    decision_frame[["category", "decision"]] = decision_frame[["category", "decision"]].astype("string")
    
    decision = decision_frame.apply(func, axis = 1)
    decision_frame = pd.DataFrame({"covariate": decision_frame["covariate"], "decision": decision})

    return decision_frame

def get_decision_combos(decision_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Create a dataframe for all possible decision combinations.
    
    Each row will give a decision for each covariate in a column.
    """
    groups = {group: data["decision"].tolist() for group, data in decision_frame.groupby("covariate")}
    combos = list(product(*groups.values()))
    combos_df = pd.DataFrame(combos, columns = groups.keys())

    return combos_df

def decision_dict_to_frame(decision_dictionary: dict) -> pd.DataFrame:

    decision_frame = dictionary_to_frame(decision_dictionary)
    decision_frame = combine_category_decision(decision_frame)

    return decision_frame

def check_single_decision_implemented(covariate_string: str, decision_string: str) -> bool:

    if decision_string in ("default", "drop"):
        return True
    
    # split into generic category and detailed decision
    category, decision = tuple(decision_string.split("_"))
    specific_category_name = covariate_string + "_" + category  # e.g. age_bin
    generic_category_name = "covariate" + "_" + category        # e.g. covariate_bin
    specific_decision_name = covariate_string + "_" + category + "_" + decision # e.g. age_bin_quantile
    
    if specific_decision_name in IMPLEMENTED_FUNCTIONS:
        return True
    elif specific_category_name in IMPLEMENTED_FUNCTIONS:
        return True
    elif generic_category_name in IMPLEMENTED_FUNCTIONS:
        return True
    else:
        raise ValueError(f"There is no specific or generic function implemented for '{specific_decision_name}'.")


def preprocess_covariate(covariate_string: str, decision_string: str,data: pd.DataFrame) -> pd.DataFrame:
    
    if decision_string == "default":
        return data
    if decision_string == "drop":
        # covariate specific fucntions need 2 arguments: data, covariate_name
        # e.g. 'covariate_<drop>'(data, <covartiate_name>)
        args_to_give = {"data": data, "covariate_name": covariate_string}
        new_data = call_function_by_name("covariate_drop", args_to_give)
        return new_data
    
    category, decision = tuple(decision_string.split("_"))
    # e.g. bin_noneLower100Above100
    complete_name = covariate_string + "_" + category + "_" + decision
    # e.g. savingStatus_bin_noneLower100Above100
    category_name = "covariate" + "_" + category
    # e.g covariate_bin

    if complete_name in IMPLEMENTED_FUNCTIONS:
        # individual functions need 1 argument: data
        # e.g. 'checkingStatus_bin_positiveNegativeNone'(data)
        new_data = call_function_by_name(complete_name, {"data": data})
        return new_data
    elif category_name in IMPLEMENTED_FUNCTIONS:
        num_args = len(get_required_args(category_name))
        if num_args == 3:
            # covariate and decision specific functions need 3 arguments: data, covariate_name, decision
            # e.g. 'covariate_<bin>'(data, <covariate_name>, <quantile>)
            if category == "bin":
                args_to_give = {"data": data,
                                "covariate_name": covariate_string,
                                "bin": decision}
            elif category == "scale":
                args_to_give = {"data": data,
                                 "covariate_name": covariate_string,
                                 "scale": decision}
            else:
                raise ValueError(f"Expected to have 2 or 3 arguments for {category_name} but got {num_args}")
            
            new_data = call_function_by_name(category_name,args_to_give)
            return new_data    
        else:
            raise AttributeError(f"No decision function implemented with 3 arguments for {category_name}.")  
    else:
        raise AttributeError(f"No decision function found for {covariate_string + decision_string} or more general.")


def handle_decision_selection(decisions, data) -> pd.DataFrame:
    
    # decision dataFrame: column names in camle case
    # data dataFrame: column names in snake_case

    covariate_counter = 0
    for covariate, _ in decisions.items():
        covariate_counter += 1
        if covariate not in data.columns:
            raise ValueError(f"Cannot apply decision to '{covariate}' since not found in data frame.")
       
        # get actual string from decisions frame (e.g. 'default', 'drop', 'bin',...)
        decision_string = decisions[covariate].values[0]

        # check whether there is a function implementing the data preprocessing decision for this covariate
        # function raises an error if not implemented
        check_single_decision_implemented(covariate, decision_string)
        # alter covariate in original dataset
        data = preprocess_covariate(covariate, decision_string, data)

    return data


def covariate_scale(data:pd.DataFrame, covariate_name:str, scale: str):
    
    values = data[covariate_name].values

    if scale == "standard":
        mean = np.mean(values)
        std = np.std(values)
        values = values - mean
        values = values / std

    elif scale == "log":
        values = np.log(values)

    else:
        raise AttributeError(f"No implementation to scale for keyword '{scale}'")
    
    data[covariate_name] = values
    
    return data