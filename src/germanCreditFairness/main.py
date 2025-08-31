from pathlib import Path
from germanCreditFairness.data import get_german_credit
from germanCreditFairness.utils import yaml_to_dictionary, decision_dict_to_frame, get_decision_combos, handle_decision_selection
from germanCreditFairness.utils import PATH_CONF, PATH_ASSETS
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import csv
import xgboost as xgb

SEED = 123

credit = get_german_credit()
print(f"total number of variables: {len(credit.columns)}")
#------------------------------------ multiverse strategy setup -------------------------------------------------
decisions = yaml_to_dictionary(PATH_CONF / Path("decisions.yaml"))

decisions = decision_dict_to_frame(decisions)

decisions_combo = get_decision_combos(decisions)

print(f"possible decision combinations: {decisions_combo.shape[0]}, for {decisions_combo.shape[1]} varivables to change")
#------------------------------------ multiverse analysis ------------------------------------------------------
params = yaml_to_dictionary(PATH_CONF / Path("train.yaml"))
params_xgb = params.get("params_xgb")
model = xgb.XGBClassifier(params_xgb)

rowcounter = 0
str_log = PATH_ASSETS / Path("log.csv")
all_columns = credit.columns.tolist()
with open(str_log, "w", newline = "") as f:
    writer = csv.writer(f)
    writer.writerow(all_columns + ["accuracy"])

for rownumber in range(len(decisions_combo)):
    rowcounter += 1
    new_decision = decisions_combo.iloc[[rownumber]]
    credit_preprocessed = credit.copy()
    credit_preprocessed = handle_decision_selection(new_decision, credit_preprocessed)

    for col in credit_preprocessed.select_dtypes(include="category"):
        credit_preprocessed[col] = credit_preprocessed[col].cat.codes
    
    X = credit_preprocessed.drop(columns = ["class"])
    y = credit_preprocessed["class"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = SEED)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # logging
    active_covariates =[col if col in all_columns else "None" for col in credit_preprocessed.columns]
    with open(str_log, "a", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(active_covariates + acc)


print(f" Number of different preprocessing alternatives: {rowcounter}")
