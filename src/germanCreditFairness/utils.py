import pandas as pd
import germanCreditFairness.decisions as decisions
from omegaconf import OmegaConf
from pathlib import Path
import inspect
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DECISIONS_YAML = PROJECT_ROOT / Path("conf") / Path("decisions.yaml")
IMPLEMENTED_FUNCTIONS = [name for name, _ in inspect.getmembers(decisions, inspect.isfunction)]


def snake_to_camel(snake_string: str) -> str:
    """Turn snake case string into camel case string."""
    parts = snake_string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

def yaml_to_frame(path_yaml: Path = DECISIONS_YAML) -> pd.DataFrame:
    """"""
    decision_mapping = OmegaConf.load(path_yaml)
    decision_mapping = OmegaConf.to_container(decision_mapping, resolve=True)
    
    return decision_mapping
    decisions_list = []
    for covariate in decision_mapping.keys():
        categories_list = decision_mapping.get(covariate)
        for category_item in categories_list:
            if isinstance(category_item, dict):
                # category item: {'bin': [[a,b,c], 'quantile', [x,y,z]} for example
                for category, decision_list in category_item.items():
                    for decision in decision_list:
                        decisions_list.append({"covariate": snake_to_camel(covariate), "category": category, "decision": decision})
            else:
                # if a covariate only has the option drop the category_item will be a single string
                decisions_list.append({"covariate": snake_to_camel(covariate), "category": category, "decision": category})

    decisions = pd.DataFrame(decisions_list)

    return decisions

def  check_function_exists(function_name: str) -> bool:

    return function_name in IMPLEMENTED_FUNCTIONS

def add_implementation_of_function_check_column(decisions: pd.DataFrame) -> pd.DataFrame:
    
    status = []
    for _, row in decisions.iterrows():

        category = row["category"]
        covariate = row["covariate"]
        decision = row["decision"]
        

        if category == "drop":
            function_name = "covariate_drop"
            if check_function_exists(function_name):
                status.append(True)
                continue
            else:
                status.append(False)
                continue

        elif category == "bin":
            function_name = covariate + "_" + category + "_" +  str(decision)
            if check_function_exists(function_name):
                # first check whether specific function available
                # e.g. job_bin_employedUnemployed
                status.append(True)
                continue
            else:
                # if not check for more generic function implementation
                # e.g. job_bin (with binning arguments as decision)
                function_name = "covariate" + "_" + category
                if check_function_exists(function_name):
                    status.append(True)
                    continue
                else:
                    status.append(False)
                    continue
    
        elif category == "scale":
            function_name = covariate + "_" + category + "_" + str(decision)
            if check_function_exists(function_name):
                status.append(True)
                continue
            else:
                function_name = "covariate" + "_" + category
                if check_function_exists(function_name):
                    status.append(True)
                    continue
                else:
                    status.append(False)
                    continue

        # elif category== "merge":
        #     function_name = "covariate_merge"
        else:
            raise ValueError(f"Got an unexpected category '{category}'")
        
        

    decisions["status"] = status

    return decisions




def yaml_to_dictionary(path:str | Path = DECISIONS_YAML) -> dict:

    with path.open("r") as f:

        decisions = yaml.safe_load(f)
        return decisions


def flatten_dict(dictionary):
    flattened = [(k,v) for k, values in dictionary.items() for v in values]
    return flattened

def flatten(item: list, acc = []):
    
    
    # consume the list from left to right until empty
    # by extending accumulator by deflattened dictionary or list item
    while item: # true if not empty
        head = item.pop(0)
        if isinstance(head, dict):
            acc.extend(flatten_dict(head))
        else:
            acc.append(head)
    return acc        

def dictionary_to_frame(decisions:dict) -> pd.DataFrame:
    df = pd.DataFrame()
    for covariate, entry in decisions.items():
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
    decision = decision_frame.apply(combine_category_decision, axis = 1)
    decision_frame = pd.DataFrame({"covariate": decision_frame["covariate"], "decision": decision})

    return decision_frame

decision_dictionary = yaml_to_dictionary()
decision_frame = dictionary_to_frame(decision_dictionary)