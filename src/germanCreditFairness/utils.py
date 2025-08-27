import pandas as pd
from omegaconf import OmegaConf

def snake_to_camel(snake_string: str) -> str:
    """Turn snake case string into camel case string."""
    parts = snake_string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

def read_yaml(path_yaml: str = "conf/decisions.yaml") -> pd.DataFrame:

    decisions = OmegaConf.load(path_yaml)
    decisions = OmegaConf.to_container(decisions, resolve=True)
    
    strategies_list = []
    for covariate in decisions.keys():
        categories_list = decisions.get(covariate)
        for category_item in categories_list:
            if isinstance(category_item, dict):
                # category item: {'binning': [[a,b,c], 'quantile', [x,y,z]} for example
                for category, decision_list in category_item.items():
                    for decision in decision_list:
                        strategies_list.append({"covariate": snake_to_camel(covariate), "category": category, "decision": decision})
            else:
                # if a covariate only has the option drop the category_item will be a single string
                strategies_list.append({"covariate": snake_to_camel(covariate), "category": category, "decision": category})

    strategies = pd.DataFrame(strategies_list)

    return strategies

def check_implemented_strategies(strategies: pd.DataFrame) -> bool:
    pass