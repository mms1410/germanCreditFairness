from germanCreditFairness.data import assert_categories



def checkingStatus_positiveNegativeNone(data):
    """Merge '0<=X<200' and '>=200' for checking_status into the category 'positive'.
    '<0' will be set to 'negative' and 'no checking will be inherited."""

    expected_categories = ["<0", "0<=X<200", ">=200", "no checking"]
    assert_categories(data, "checking_status", expected_categories)

    to_replace = {"<0": "negative",
                  "0<=X<200": "positive",
                  ">200": "positive"
                  }
    data["checking_status"].replace(to_replace, inplace = True)

    return data

def duration_binning_strategy1():
    pass

def duration_binning_quantile():
    pass

def creditHistory_goodBad(data):
    """Seperate categories into 'Good' and 'Bad' ones."""
    
    expected_categories = [
        "all paid",
        "critical/other existing credit",
        "delayed previously",
        "existing paid",
        "no credits/all paid",
    ]
    assert_categories(data, "credit_history", expected_categories)

    to_replace= {"all paid": "Good",
                 "critical/other existing credit": "Bad",
                 "delayed previously": "Bad",
                 "existing paid": "Good",
                 "no credits/all paid": "Good"}
    data["credit_history"].replace(to_replace, inplace = True)

    return data

def purpose_educNoEduc(data):
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

    assert_categories(data, "credit_history", expected_categories)


def creditAmount_binning_strategy1():
    pass

def creditAmount_binning_quantile():
    pass

def savingsStatus_noneLower100Above100(data):
    """Seperate categories into 'above 100' (including 100), 'below 100' (excluding 100) and 'no known savings'."""
    
    expected_categories = [
        "100<=X<500",
        "500<=X<1000",
        "<100",
        ">=1000",
        "no known savings",
    ]
    assert_categories(data, "savings_status", expected_categories)

    to_replace = {"100<=X<500": "above 100",
                  "500<=X<1000": "above 100",
                  "<100": "below 100",
                  ">=1000": "above 100"}
    data["savings_status"].replace(to_replace, in_place = True)

    return data

def employment_employedUnemployed(data):
    """Seperate categories into 'employed' or 'unemployed' only."""
    
    expected_categories = ["1<=X<4", "4<=X<7", "<1", ">=7", "unemployed"]
    assert_categories(data, "employment", expected_categories)

    to_replace = {"1<=X<4": "employed",
                  "4<=X<7": "employed",
                  "<1": "employed",
                  ">=7": "employed"}
    data["employment"].replace(to_replace, in_place = True)

    return data

def installmentCommitment_notIncluded():
    pass

def personalStatus_maleFemale(data):
    """Seperate categories into 'male' and 'female' only."""
    
    expected_categories = [
        "female div/dep/mar",
        "male div/sep",
        "male mar/wid",
        "male single",
    ]
    assert_categories(data, "personal_status", expected_categories)

    to_replace = {"female div/dep/mar" : "female",
                  "male div/sep": "male",
                  "male mar/wid": "male",
                  "male single": "male"}
    
    data["personal_status"].repalace(to_replace, in_place = True)

    return data

def otherParties_notIncluded(data):
    
    assert "other_parties" in data.columns
    
    data.drop("other_parties", axis = 1, in_place = True)

    return data


def residenceSince_notIncluded(data):
    
    assert "residence_since" in data.columns

    data.drop("residence_since", axis = 1, in_place = True)

    return data

def propertyMagnitude_notIncluded(data):
    
    assert "property_magnitude" in data.columns

    data.drop("property_magnitude", axis = 1, in_place = True)

    return data

def age_binning_quantile(data):
    
    assert "age"

def otherPaymentPlans_notIncluded(data):
    
    assert "other_payment_plans" in data.columns

    data.drop("other_payment_plans", axis = 1, in_place = True)

    return data


def housing_notIncluded(data):
    
    assert "housing" in data.column

    data.drop("housing", axis = 1, in_place = True)

    return data

def existingCredit_notIncluded(data):
    
    assert "existing_credit" in data.columns

    data.drop("existing_credit", axis = 1, in_place = True)

    return data

def job_notIncluded(data):
    
    assert "job" in data.columns

    data.drop("job", axis = 1, in_place = True)

    return data
    

def numDepends_notIncluded(data):
    
    assert "num_depends" in data.columns

    data.drop("num_depends", axis = 1, in_place = True)

    return data

def ownTelephone_notIncluded(data):
    
    assert "own_telephone" in data.columns

    data.drop("own_telephone", axis = 1, in_place = True)

    return data

def foreignWorker_notIncluded(data):
    
    assert "foreign_worker" in data.columns

    data.frop("foreign_worker", axis = 1, in_place =True)

    return data