# Robustness Analysis of Fairness Metrics for the German Credit Dataset

<img label="teaser_gif1" src="assets\metrics_boxplot_age.png">
<br>
<img label="teaser_gif2" src="assets\metrics_boxplot_job.png">
<br>
<img label="teaser_gif2" src="assets\metrics_boxplot_personalStatus.png">

# Aim

A Simulation for Fairness Metrics implemented in [AIF360](https://github.com/Trusted-AI/AIF360) based on the [German Credit dataset](https://api.openml.org/d/31) from openML. The protected attributes are:
<br>
- 'age': categoroized in privileged group is "old", unprivileged group is "young".
- 'job': categorized in privileged group "resident", unprivileged group "nonResident".
- 'personalStatus': categorized into privileged group "female", unprivileged group "male".
<br>
For simulation different proprocessing combinations for each covariate where used and for each possible combination new metrics where calculated.
