import pandas as pd

#----------------------------------------------------------------------------------------------------------------
def set_equal(list1:list, list2:list) -> bool:

    return set(list1) == set(list2)


def check_checkingStatus(data:pd.DataFrame):
    
    expected = ['<0', '0<=X<200', 'no checking', '>=200']
    found = data["checking_status"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")

def check_duration():
    pass

def check_creditHistory(data:pd.DataFrame):
    
    expected = ['critical/other existing credit', 'existing paid', 'delayed previously', 'no credits/all paid', 'all paid']
    found = data["credit_history"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")


def check_purpose(data:pd.DataFrame):
    
    expected = ['radio/tv', 'education', 'furniture/equipment', 'new car', 'used car', 'business', 'domestic appliance', 'repairs', 'other', 'retraining']
    found = data["purpose"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")

def check_creditAmount():
    pass

def check_savingsStatus(data:pd.DataFrame):
    
    expected = ['no known savings', '<100', '500<=X<1000', '>=1000', '100<=X<500']
    found = data["saving_status"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")


def check_employment(data:pd.DataFrame):
    
    expected = ['>=7', '1<=X<4', '4<=X<7', 'unemployed', '<1']
    found = data["employment"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_installmentCommitment(data:pd.DataFrame):
    
    expected = [4, 2, 3, 1]
    found = data["installment_commitment"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_personalStatus(data:pd.DataFrame):
    
    expected = ['male single', 'female div/dep/mar', 'male div/sep', 'male mar/wid']
    found = data["personal_status"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_otherParties(data:pd.DataFrame):
    
    expected = ['none', 'guarantor', 'co applicant']
    found = data["other_parties"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_residenceSince(data:pd.DataFrame):
    
    expected = [1, 2, 3, 4]
    found = data["residence_since"]

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_propertyMagnitude(data:pd.DataFrame):
    
    expected = ['real estate', 'life insurance', 'no known property', 'car']
    found = data["property_magnitude"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")

def check_age():
    pass

def check_otherPaymentPlans(data:pd.DataFrame):
     
     expected = ['none', 'bank', 'stores']
     found = data["other_payment_plans"].unique()

     if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
     
def check_housing(data:pd.DataFrame):

    expected = ['own', 'for free', 'rent']
    found = data["housing"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_existingCredits(data:pd.DataFrame):
    
    expected = [1, 2, 3, 4]
    found = data["existing_credits"]

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_job(data:pd.DataFrame):
    
    expected = ['skilled', 'unskilled resident', 'high qualif/self emp/mgmt', 'unemp/unskilled non res']
    found  = data["job"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_numDepends(data:pd.DataFrame):
    
    expected = [1, 2, 3, 4]
    found = data["num_depends"]

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")
    
def check_ownTelephone(data:pd.DataFrame):
    
    expected = ['yes', 'none']
    found = data["own_telephone"].unique()

    if not set_equal(expected, found):
        raise ValueError(f"Expected values {expected}, got {found}")