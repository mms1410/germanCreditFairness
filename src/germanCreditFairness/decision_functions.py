from germanCreditFairness.data import assert_categories
import pandas as pd
import numpy as np
import re
import ast


def replace_category(data: pd.Series, to_replace:dict) -> pd.Series:
    
    data = data.cat.add_categories(set(to_replace.values()))
    #data = data.replace(to_replace)
    data = data.map(lambda x: to_replace.get(x, x)).astype("category")
    data = data.cat.remove_unused_categories()

    return data

# classification depending on arguments
#
# individual function
#   required arguments: data
#   e.g. 'checkingStatus_bin_positiveNegativeNone'
#
# covariate specific function
#   required arguments: data, covariate_name
#   e.g. 'covariate_drop'
#
# covariate and decision specific function
#   required arguments: data, covariate_name, decision
#   e.g. 'covariate_bin'

# individual functions
#---------------------------------------------------------------------------------------------------------
def checkingStatus_bin_positiveNegativeNone(data:pd.DataFrame) -> pd.DataFrame :
    """Merge '0<=X<200' and '>=200' for checkingStatus into the category 'positive'.
    '<0' will be set to 'negative' and 'no checking will be inherited."""

    expected_categories = ["<0", "0<=X<200", ">=200", "no checking"]
    assert_categories(data, "checkingStatus", expected_categories)

    to_replace = {"<0": "negative",
                  "0<=X<200": "positive",
                  ">200": "positive"
                  }
    data["checkingStatus"] = replace_category(data["checkingStatus"], to_replace)
    return data

def creditHistory_bin_goodBad(data:pd.DataFrame) -> pd.DataFrame :
    """Seperate categories into 'Good' and 'Bad' ones."""
    
    expected_categories = [
        "all paid",
        "critical/other existing credit",
        "delayed previously",
        "existing paid",
        "no credits/all paid",
    ]
    assert_categories(data, "creditHistory", expected_categories)

    to_replace= {"all paid": "Good",
                 "critical/other existing credit": "Bad",
                 "delayed previously": "Bad",
                 "existing paid": "Good",
                 "no credits/all paid": "Good"}
    data["creditHistory"] = replace_category(data["creditHistory"], to_replace)

    return data

def purpose_bin_educNoEduc(data:pd.DataFrame) -> pd.DataFrame :
    
    expected_categories = ['radio/tv',
                           'education',
                           'furniture/equipment',
                           'new car',
                           'used car',
                           'business',
                           'domestic appliance',
                           'repairs',
                           'other',
                           'retraining']

    assert_categories(data, "purpose", expected_categories)

    to_replace = {'radio/tv': "NoEduc",
                           'education': "Educ",
                           'furniture/equipment': "NoEduc",
                           'new car': "NoEduc",
                           'used car': "NoEduc",
                           'business': "NoEduc",
                           'domestic appliance': "NoEduc",
                           'repairs': "noEduc",
                           'other': "noEduc",
                           'retraining': "noEduc"}
    
    data["purpose"] = replace_category(data["purpose"], to_replace)
    return data

def purpose_bin_checkExpensive(data:pd.DataFrame) -> pd.DataFrame :
    
    expected_categories = ['radio/tv',
                           'education',
                           'furniture/equipment',
                           'new car',
                           'used car',
                           'business',
                           'domestic appliance',
                           'repairs',
                           'other',
                           'retraining']

    assert_categories(data, "purpose", expected_categories)

    to_replace = {'radio/tv': "cheap",
                           'education': "cheap",
                           'furniture/equipment': "cheap",
                           'new car': "expensive",
                           'used car': "expensive",
                           'business': "cheap",
                           'domestic appliance': "cheap",
                           'repairs': "cheap",
                           'other': "expensive",
                           'retraining': "cheap"}
    
    data["purpose"] = replace_category(data["purpose"], to_replace)
    return data

def savingsStatus_bin_noneLower100Above100(data:pd.DataFrame) -> pd.DataFrame :
    """Seperate categories into 'above 100' (including 100), 'below 100' (excluding 100) and 'no known savings'."""
    
    expected_categories = [
        "100<=X<500",
        "500<=X<1000",
        "<100",
        ">=1000",
        "no known savings",
    ]
    assert_categories(data, "savingsStatus", expected_categories)

    to_replace = {"100<=X<500": "above100",
                  "500<=X<1000": "above100",
                  "<100": "below100",
                  ">=1000": "above100",
                  "no known savings": "NA"}
    
    data["savingsStatus"] = replace_category(data["savingsStatus"], to_replace)
    return data

def employment_bin_employedUnemployed(data:pd.DataFrame) -> pd.DataFrame :
    """Seperate categories into 'employed' or 'unemployed' only."""
    
    expected_categories = ["1<=X<4", "4<=X<7", "<1", ">=7", "unemployed"]
    assert_categories(data, "employment", expected_categories)

    to_replace = {"1<=X<4": "employed",
                  "4<=X<7": "employed",
                  "<1": "employed",
                  ">=7": "employed"}
    data["employment"] = replace_category(data["employment"], to_replace)
    return data

def personalStatus_bin_maleFemale(data:pd.DataFrame) -> pd.DataFrame :
    """Seperate categories into 'male' and 'female' only."""
    
    expected_categories = [
        "female div/dep/mar",
        "male div/sep",
        "male mar/wid",
        "male single",
    ]
    assert_categories(data, "personalStatus", expected_categories)

    to_replace = {"female div/dep/mar" : "female",
                  "male div/sep": "male",
                  "male mar/wid": "male",
                  "male single": "male"}
    
    data["personalStatus"] = replace_category(data["personalStatus"], to_replace)
    return data

def job_bin_residentNoResidentOther(data: pd.DataFrame) -> pd.DataFrame:

    expected_categories = ['skilled', 'unskilled resident', 'high qualif/self emp/mgmt',
                           'unemp/unskilled non res']

    assert_categories(data, "job", expected_categories)

    to_replace = {'skilled': "other",
                  'unskilled resident': "resident",
                  'high qualif/self emp/mgmt': "other",
                  'unemp/unskilled non res':"noResident"}

    
    data["job"] = replace_category(data["job"], to_replace)
    return data

# covariate and decision specific functions
#----------------------------------------------------------------------------------------------------------# need data, covariate_name and specific final decision as arguments 
def covariate_bin(data:pd.DataFrame, covariate_name:str, bin: list[int | float] | str) -> pd.DataFrame : 

    assert covariate_name in data.columns

    
    pattern = r"^\[\s*\d+(\s*,\s*\d+)*\s*\]$"
    
    if bool(re.match(pattern, bin)):
        # check whether bin is keyword or a list with cuts
        bin = ast.literal_eval(bin)
    elif isinstance(bin, str):

        if bin == "quantile":
            data[covariate_name] = pd.qcut(data[covariate_name], q = 4,
                                           labels = False # integer outputs
                                           )
        else:
            raise ValueError(f"For binning keyword '{bin}' no implementation exists.")
    else:
        raise AttributeError(f"No implementation for '{covariate_name + bin}'")
    
    return data
    

def covariate_scale(data:pd.DataFrame, covariate_name:str, scale: str):
    
    values = data[covariate_name].values
    if scale == "log":
        values = np.log(values)
    elif scale == "standard":
        mean = np.mean(values)
        std = np.std(values)
        values -= mean
        values /= std
    else:
        raise ValueError(f"For scaling keyword '{scale}' no implementation exists.")
    
    data[covariate_name] = values
    
    return data



# covariate specific funcitons
#----------------------------------------------------------------------------------------------------------
def covariate_drop(data:pd.DataFrame, covariate_name:str) -> pd.DataFrame :

    if covariate_name not in data.columns:
        raise AttributeError(f"Covariate {covariate_name} not found in data to drop.")
    data.drop(covariate_name, axis = 1, inplace = True)

    return data