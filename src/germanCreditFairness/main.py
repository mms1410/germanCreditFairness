from pathlib import Path
from germanCreditFairness.data import get_german_credit
from germanCreditFairness.utils import yaml_to_dictionary, decision_dict_to_frame, get_decision_combos, handle_decision_selection
from germanCreditFairness.utils import  evaluate_fairness, no_metrics
from germanCreditFairness.utils import PATH_CONF, PATH_ASSETS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import xgboost as xgb
import pandas as pd
import time


SEED = 123

credit = get_german_credit()
print(f"total number of variables: {len(credit.columns)}")
#------------------------------------ multiverse strategy setup -------------------------------------------------
decisions = yaml_to_dictionary(PATH_CONF / Path("decisions.yaml"))

decisions = decision_dict_to_frame(decisions)

decisions_combo = get_decision_combos(decisions)

all_columns = credit.columns.tolist()
variable_columns = decisions.covariate.unique().tolist()
print(f"possible decision combinations: {decisions_combo.shape[0]}, for {len(variable_columns)} varivables to change")
#------------------------------------ multiverse analysis ------------------------------------------------------

age_metrics = pd.DataFrame(columns = ["accuracy", "DI", "SPD","EOD","AOD","Theil"] + variable_columns)
personalStatus_metrics = age_metrics.copy()
job_metrics = age_metrics.copy()

params = yaml_to_dictionary(PATH_CONF / Path("train.yaml"))
params_xgb = params.get("paramsXgb")
params_xgb["random_state"] = SEED
params_xgb["enable_categorical"]  = True

model = xgb.XGBClassifier(**params_xgb)
start_time = time.time()
for rownumber in range(len(decisions_combo)):

    new_decision = decisions_combo.iloc[[rownumber]]
    credit_preprocessed = credit.copy()
    credit_preprocessed = handle_decision_selection(new_decision, credit_preprocessed)
    
    X = credit_preprocessed.drop(columns = ["class"])

    class_encoder = LabelEncoder()
    y = credit_preprocessed["class"]
    y = class_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = SEED)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if "age" in X.columns:
        current_age_decision = new_decision.iloc[0]["age"]
        if not pd.api.types.is_numeric_dtype(X["age"]): # fairnes metrics only for categorical protected attribute        
            if current_age_decision == "bin_younger30":
                fair_metrics = evaluate_fairness(X_test,y_test, y_pred, "age",
                                            privileged_value = "old",
                                            unprivileged_value = "young")
                fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)
            elif current_age_decision == "bin_younger25":
                fair_metrics = evaluate_fairness(X_test,y_test, y_pred, "age",
                                            privileged_value = "old",
                                            unprivileged_value = "young")
                fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)
            else:
                # nothing else implemented
                fair_metrics = no_metrics()
                fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)
        else:
            # not possible for continous variable
            fair_metrics = no_metrics()
            fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)

        age_metrics = pd.concat([age_metrics, fair_metrics])

    if "personalStatus" in X.columns:
        current_personalStatus_decision = new_decision.iloc[0]["personalStatus"]
        if current_personalStatus_decision == "bin_maleFemale":
            fair_metrics = evaluate_fairness(X_test, y_test, y_pred, "personalStatus",
                                             privileged_value="male",
                                             unprivileged_value="female")
            fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)
        else:
            # nothing else implemented
            fair_metrics = no_metrics()
            fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)

        personalStatus_metrics = pd.concat([personalStatus_metrics, fair_metrics])

    if "job" in X.columns:
        current_job_decision = new_decision.iloc[0]["job"]
        if current_job_decision == "bin_residentNoResidentOther":
            fair_metrics = evaluate_fairness(X_test, y_test, y_pred, "job",
                                            privileged_value="resident",
                                            unprivileged_value="noResident")
            fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)
            
        else:
            # nothing else implemented
            fair_metrics = no_metrics()
            fair_metrics = pd.concat([fair_metrics.reset_index(drop=True),new_decision.reset_index(drop = True)], axis = 1)

        job_metrics = pd.concat([job_metrics, fair_metrics])


age_metrics.to_csv(PATH_ASSETS / Path("age_metrics.csv"), index = False)
personalStatus_metrics.to_csv(PATH_ASSETS / Path("personalStatus_metrics.csv", index = False))
job_metrics.to_csv(PATH_ASSETS / Path("job_metrics.csv", index = False))

end_time = time.time()
print(end_time)
print("============================= END =============================")