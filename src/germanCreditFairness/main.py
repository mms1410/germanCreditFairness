import omegaconf
from pathlib import Path
from matplotlib import pyplot as plt
from germanCreditFairness.data import get_german_credit
from germanCreditFairness.plot_functions import plot_categories, plot_numerical

path_assets = Path(__file__).resolve().parent.parent.parent / Path("assets")

credit = get_german_credit()
# preprocessing_strategies = omegaconf.OmegaConf.load("preprocessing_strategies.yaml")
# print(omegaconf.OmegaConf.to_container(preprocessing_strategies, resolve = True))


# plot_categories(credit)
# plt.savefig(path_assets / Path("credit_categories.png"), dpi = 300, bbox_inches = "tight")
# plt.close()


plot_numerical(credit)
plt.savefig(path_assets / Path("credit_numericals.png"), dpi = 300, bbox_inches = "tight")
plt.close()