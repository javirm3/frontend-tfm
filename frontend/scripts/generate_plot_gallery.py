from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "glmhmmt" / "src"))

from glmhmmt.model_plots import (  # noqa: E402
    plot_binary_emission_weights_summary_boxplot,
    plot_posterior_probs,
    plot_session_deepdive,
    plot_session_trajectories,
    plot_change_triggered_posteriors_summary,
    plot_state_accuracy,
    plot_state_dwell_times_summary,
    plot_state_occupancy,
    plot_state_posterior_count_kde,
    plot_transition_matrix,
)
from glmhmmt.postprocess import (  # noqa: E402
    build_change_triggered_posteriors_payload,
    build_session_deepdive_payload,
    build_session_trajectories_payload,
    build_state_accuracy_payload,
    build_state_dwell_times_payload,
    build_state_occupancy_payload,
    build_state_posterior_count_payload,
)


OUT_DIR = ROOT / "frontend" / "public" / "plot-gallery"


def _weights_df() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(12)
    for subject in ["S1", "S2", "S3", "S4"]:
        for rank, state in enumerate(["Engaged", "Disengaged"]):
            for feature, base in {"bias": 0.3, "stimulus": 1.2, "prev_choice": -0.5}.items():
                rows.append(
                    {
                        "subject": subject,
                        "state_idx": rank,
                        "state_rank": rank,
                        "state_label": state,
                        "class_idx": 0,
                        "feature": feature,
                        "weight": base + (0.35 if state == "Engaged" else -0.25) + rng.normal(0, 0.12),
                    }
                )
    return pd.DataFrame(rows)


def _trial_df() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(7)
    for subject in ["S1", "S2", "S3"]:
        for session in range(1, 5):
            state = 0
            for trial in range(45):
                if rng.random() < 0.08:
                    state = 1 - state
                p0 = 0.78 if state == 0 else 0.22
                p0 = float(np.clip(p0 + rng.normal(0, 0.08), 0.02, 0.98))
                p1 = 1.0 - p0
                correct = rng.random() < (0.82 if state == 0 else 0.58)
                rows.append(
                    {
                        "subject": subject,
                        "session": session,
                        "trial_idx": session * 100 + trial,
                        "trial": trial,
                        "state_idx": state,
                        "state_rank": state,
                        "state_label": "Engaged" if state == 0 else "Disengaged",
                        "p_state_0": p0,
                        "p_state_1": p1,
                        "correct_bool": correct,
                        "response": int(rng.random() > (0.70 if state == 0 else 0.45)),
                        "stimulus": np.sin(trial / 6),
                    }
                )
    return pd.DataFrame(rows)


def _posterior_df(trial_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    label_by_idx = {0: "Engaged", 1: "Disengaged"}
    for _, row in trial_df[trial_df["subject"] == "S1"].iterrows():
        for idx in [0, 1]:
            rows.append(
                {
                    "subject": row["subject"],
                    "trial_idx": row["trial_idx"],
                    "state_idx": idx,
                    "state_rank": idx,
                    "state_label": label_by_idx[idx],
                    "probability": row[f"p_state_{idx}"],
                }
            )
    return pd.DataFrame(rows)


def _save(fig, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / f"{name}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    weights = _weights_df()
    trials = _trial_df()

    _save(
        plot_binary_emission_weights_summary_boxplot(
            weights,
            K=2,
            feature_order=("bias", "stimulus", "prev_choice"),
            abs_features=("bias",),
        ),
        "emission-weights",
    )
    _save(
        plot_transition_matrix(
            np.asarray([[0.91, 0.09], [0.18, 0.82]]),
            ["Engaged", "Disengaged"],
            title="Mean transition matrix",
        ),
        "transition-matrix",
    )
    _save(plot_posterior_probs(_posterior_df(trials), subject="S1"), "posterior-probs")

    fig_acc, _ = plot_state_accuracy(build_state_accuracy_payload(trials, chance_level=0.5))
    _save(fig_acc, "state-accuracy")
    _save(plot_state_posterior_count_kde(build_state_posterior_count_payload(trials)), "posterior-counts")
    _save(plot_session_trajectories(build_session_trajectories_payload(trials)), "session-trajectories")
    _save(
        plot_change_triggered_posteriors_summary(
            build_change_triggered_posteriors_payload(trials, window=8)
        ),
        "change-triggered",
    )
    _save(plot_state_occupancy(build_state_occupancy_payload(trials)), "state-occupancy")
    _save(
        plot_state_dwell_times_summary(
            build_state_dwell_times_payload(
                trials,
                transition_matrices={
                    subject: np.asarray([[0.91, 0.09], [0.18, 0.82]])
                    for subject in trials["subject"].unique()
                },
            )
        ),
        "dwell-times",
    )
    _save(
        plot_session_deepdive(
            build_session_deepdive_payload(
                trials,
                subject="S1",
                session=1,
                trace_cols=["stimulus"],
            )
        ),
        "single-session",
    )


if __name__ == "__main__":
    main()
