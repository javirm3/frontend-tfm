---
title: Task Plots
description: Task-specific plots returned by `TaskAdapter.get_plots()`.
---

Task plot modules expose two kinds of functions:

- re-exported common model plots from `glmhmmt.model_plots`
- task-owned behavioural plots such as psychometrics, condition panels, and
  evidence curves

Common model plots use the DataFrame/payload contract described in
[Common Plots](/docs/api/common-plots/).

## Typical Model Plot Flow

```python
from glmhmmt.postprocess import build_emission_weights_df

adapter = get_adapter("two_afc")
plots = adapter.get_plots()

weights_df = build_emission_weights_df(views)
fig = plots.plot_emission_weights_summary(weights_df, K=K)
```

Task modules should not rebuild `views`, infer legacy arrays, or prepare model
diagnostic tables inside plotting functions.

## Task-Owned Plots

Task-owned plots remain in `NMDAR_paper/src/plots/<task>.py` and should receive
data prepared by the matching `NMDAR_paper/src/process/<task>.py` module.

```python
from src.process.two_afc import prepare_psych_panel_payload

payload = prepare_psych_panel_payload(...)
fig = plots.plot_psychometric_payload(payload)
```

Use task plots for:

- psychometric curves
- performance by task condition
- delay/stimulus panels
- fitted evidence curves
- task-specific integration maps

Use common model plots for:

- emission weights
- transition matrices
- posterior probabilities
- session trajectories
- state occupancy
- accuracy by state
- dwell times
- single-session diagnostics

## Boundary

`process` owns grouping, binning, state-aligned derived columns, and payload
construction. `plots` owns axes, marks, labels, legends, and figure layout.
