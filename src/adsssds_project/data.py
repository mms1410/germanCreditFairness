from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

def get_german_credit(xy = False):
    german_credit = fetch_openml(name='credit-g', version=1, as_frame=True)
    if not xy:
        return(german_credit)
    else:
        return (german_credit.data, german_credit.target)


