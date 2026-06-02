---
title: Simulating GLM Choices
description: Generate fitted GLM choice sequences and use recursive task adapters for history regressors.
---

Fitted GLMs can be used as generative models by sampling choices from their
softmax probabilities. There are two useful simulation modes.

## Fixed Design Simulation

Use this when the design matrix does not need to change after each simulated
choice, for example when the model only uses stimulus or session regressors.

```python
from glmhmmt.glm import fit_glm

fit = fit_glm(X, y, num_classes=2)
choices = fit.simulate(seed=0, n_simulations=20)
```

The returned array has shape:

```text
(n_simulations, n_trials)
```

You can also simulate from saved arrays:

```python
from glmhmmt.glm import simulate_glm_choices

choices = simulate_glm_choices(
    X,
    emission_weights,
    baseline_class_idx=baseline_class_idx,
    num_classes=num_classes,
    lapse_mode=lapse_mode,
    lapse_rates=lapse_rates,
    seed=0,
    n_simulations=20,
)
```

## Recursive History Simulation

If the GLM contains recursive choice-history regressors, such as choice-lag
columns, action traces, previous reward, or win-stay/lose-shift terms, the
design matrix must be rebuilt after every simulated choice. Otherwise the
simulation samples choices using history regressors computed from the empirical
choices, not from the simulated choices.

Project analyses use the task adapter for this stricter mode:

```python
from src.process.common import (
    prepare_glm_simulated_corrected_behavior_autocorrelograms,
)

prepared_glm_autocorr = prepare_glm_simulated_corrected_behavior_autocorrelograms(
    df_all,
    arrays_store,
    adapter=adapter,
    subject_col="subject",
    session_col=adapter.session_col,
    trial_index_col=adapter.trial_col,
    tau=model_cfg.tau,
    emission_cols=list(model_cfg.emission_cols),
    recursive=True,
    n_simulations=20,
    max_lag=50,
    min_cross_pairs=20,
    max_cross_pairs=80,
    seed=1,
)
```

In recursive mode, each simulation proceeds trial by trial:

1. rebuild the task-owned feature dataframe with `adapter.load_subject(...)`;
2. evaluate the fitted GLM weights on the current trial design row;
3. sample the current choice;
4. write the simulated response and outcome back into the raw task dataframe;
5. continue to the next trial with history regressors rebuilt from the simulated history.

This is slower than fixed design simulation, but it is the appropriate mode for
model overlays on autocorrelograms of outcome and repetition sequences.

## Corrected Autocorrelogram Overlay

The simulated choices can be passed to the same drift-corrected
autocorrelogram pipeline used for data:

```python
from src.process.common import prepare_corrected_behavior_autocorrelograms
from src.plots.common import plot_corrected_behavior_autocorrelograms

prepared_data_autocorr = prepare_corrected_behavior_autocorrelograms(
    plot_df_all,
    subject_col="subject",
    session_col="session",
    choice_col="response",
    outcome_col="performance",
    trial_index_col="trial",
    max_lag=50,
)

fig, axes = plot_corrected_behavior_autocorrelograms(
    prepared_data_autocorr,
    model_autocorr=prepared_glm_autocorr["autocorr"],
)
```

The data are plotted as dots. The simulated GLM autocorrelogram is plotted as
the fitted model line.
