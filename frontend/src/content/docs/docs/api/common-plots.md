---
title: Common Plots
description: Task-agnostic model plots using prepared DataFrames and payloads.
---

Common plots live in `glmhmmt.model_plots`. They do not build data internally:
prepare with `glmhmmt.postprocess`, then pass the resulting DataFrame or payload
to the plot function.

## Imports

```python
from glmhmmt.postprocess import (
    build_emission_weights_df,
    build_transition_matrix_payload,
    build_state_accuracy_payload,
    build_state_posterior_count_payload,
    build_session_trajectories_payload,
    build_change_triggered_posteriors_payload,
    build_state_occupancy_payload,
    build_state_dwell_times_payload,
    build_session_deepdive_payload,
)
from glmhmmt.model_plots import (
    plot_emission_weights_summary,
    plot_transition_matrix,
    plot_state_accuracy,
    plot_state_posterior_count_kde,
    plot_session_trajectories,
    plot_change_triggered_posteriors_summary,
    plot_state_occupancy,
    plot_state_occupancy_overall,
    plot_state_occupancy_overall_summary,
    plot_state_occupancy_overall_by_subject,
    plot_state_session_occupancy,
    plot_state_session_occupancy_summary,
    plot_state_session_occupancy_by_subject,
    plot_state_switches,
    plot_state_switches_summary,
    plot_state_switches_by_subject,
    plot_state_dwell_times_summary,
    plot_session_deepdive,
)
```

## Emission Weights

```python
weights_df = build_emission_weights_df(views)
fig = plot_emission_weights_summary(weights_df, K=K)
```

![Emission weights](/plot-gallery/emission-weights.png)

## Transition Matrix

```python
payload = build_transition_matrix_payload(arrays_store, state_labels, K, subjects)
fig = plot_transition_matrix(**payload)
```

![Transition matrix](/plot-gallery/transition-matrix.png)

## Posterior Probabilities

```python
posterior_df = build_posterior_df(views)
fig = plot_posterior_probs(posterior_df, subject=subjects[0])
```

![Posterior probabilities](/plot-gallery/posterior-probs.png)

## State Accuracy

```python
payload = build_state_accuracy_payload(trial_df, chance_level=1 / adapter.num_classes)
fig, table = plot_state_accuracy(payload)
```

![State accuracy](/plot-gallery/state-accuracy.png)

## Posterior Histogram

```python
payload = build_state_posterior_count_payload(trial_df)
fig = plot_state_posterior_count_kde(payload)
```

![Posterior histogram](/plot-gallery/posterior-counts.png)

## Session Trajectories

```python
payload = build_session_trajectories_payload(
    trial_df,
    session_col=adapter.session_col,
    sort_col=adapter.sort_col,
)
fig = plot_session_trajectories(payload)
```

![Session trajectories](/plot-gallery/session-trajectories.png)

## Change-Triggered Posteriors

```python
payload = build_change_triggered_posteriors_payload(
    trial_df,
    session_col=adapter.session_col,
    sort_col=adapter.sort_col,
    switch_posterior_threshold=0.5,
    window=15,
)
fig = plot_change_triggered_posteriors_summary(payload)
```

![Change-triggered posteriors](/plot-gallery/change-triggered.png)

## State Occupancy

```python
payload = build_state_occupancy_payload(
    trial_df,
    session_col=adapter.session_col,
    sort_col=adapter.sort_col,
)
fig = plot_state_occupancy(payload)
```

The combined occupancy figure is also available as six separate figures:
summary and by-subject variants for each occupancy diagnostic.

```python
fig_overall = plot_state_occupancy_overall(payload)
fig_sessions = plot_state_session_occupancy(payload)
fig_switches = plot_state_switches(payload)

fig_overall_summary = plot_state_occupancy_overall_summary(payload)
fig_overall_by_subject = plot_state_occupancy_overall_by_subject(payload)
fig_session_summary = plot_state_session_occupancy_summary(payload)
fig_session_by_subject = plot_state_session_occupancy_by_subject(payload)
fig_switches_summary = plot_state_switches_summary(payload)
fig_switches_by_subject = plot_state_switches_by_subject(payload)
```

![State occupancy](/plot-gallery/state-occupancy.png)

## Dwell Times

```python
payload = build_state_dwell_times_payload(
    trial_df,
    session_col=adapter.session_col,
    sort_col=adapter.sort_col,
    transition_matrices=transition_matrices_by_subject,
)
fig = plot_state_dwell_times_summary(payload)
```

![Dwell times](/plot-gallery/dwell-times.png)

## Single Session

```python
payload = build_session_deepdive_payload(
    trial_df,
    subject=subject,
    session=session,
    session_col=adapter.session_col,
    sort_col=adapter.sort_col,
)
fig = plot_session_deepdive(payload)
```

![Single session](/plot-gallery/single-session.png)

## Contract

- Plot functions receive `weights_df`, `posterior_df`, or a named payload.
- Missing required columns raise `ValueError`.
- `views` may still be used to build canonical DataFrames, but it is not the
  public plotting input for common diagnostics.
