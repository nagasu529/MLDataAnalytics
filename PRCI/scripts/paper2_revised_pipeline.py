#!/usr/bin/env python
"""Reproducible Paper 2 counterfactual pipeline.

This script keeps the SAR-derived cluster labels fixed, validates the Paper 2
cluster classifier, and generates action-constrained DiCE counterfactuals.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import dice_ml
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GroupKFold, StratifiedKFold, cross_val_predict


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR.parent / "datas" / "SFProgramDataPanal_with_clusters.csv"
OUT_DIR = PROJECT_DIR / "paper2_outputs"
TABLE_DIR = OUT_DIR / "tables"
FIG_DIR = OUT_DIR / "figures"

CLUSTER_FEATS = [
    "age",
    "edu",
    "agri_long",
    "irriga",
    "loan",
    "Avg_ProdManage",
    "Avg_InputManage",
    "Avg_Tech",
    "Avg_Ana&Plan",
    "Avg_Mkting",
    "Avg_Network",
    "Ave_ProdRisk",
    "Ave_InputRisk",
    "Ave_MktRisk",
    "Ave_FinRisk",
]

ACTION_FEATS = [
    "Avg_ProdManage",
    "Avg_InputManage",
    "Avg_Tech",
    "Avg_Ana&Plan",
    "Avg_Mkting",
    "Avg_Network",
]

COURSE_MAPPING = {
    "Avg_ProdManage": "Production Management",
    "Avg_InputManage": "Input and Resource Optimization",
    "Avg_Tech": "Technology Adoption",
    "Avg_Ana&Plan": "Agri-Business Analysis and Planning",
    "Avg_Mkting": "Marketing and Value Addition",
    "Avg_Network": "Network Building",
}

CLUSTER_NAMES = {
    0: "Low-skill",
    1: "Moderate-skill",
    2: "High-skill",
}

RF_PARAMS = {
    "n_estimators": 500,
    "min_samples_leaf": 10,
    "max_features": "sqrt",
    "random_state": 42,
    "n_jobs": -1,
}


def ensure_dirs() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_baseline() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    df = pd.read_csv(DATA_PATH).replace(".", np.nan)
    df_y0 = df[df["Year"] == 0].copy()
    df_cf = (
        df_y0[["id", "Cluster"] + CLUSTER_FEATS]
        .apply(pd.to_numeric, errors="coerce")
        .dropna()
        .copy()
    )
    x = df_cf[CLUSTER_FEATS].copy()
    y = df_cf["Cluster"].astype(int).copy()
    groups = df_cf["id"].astype(int).copy()
    return df_cf, x, y, groups


def export_data_summary(df_cf: pd.DataFrame, y: pd.Series) -> None:
    summary = pd.DataFrame(
        [
            {"metric": "baseline_records", "value": len(df_cf)},
            {"metric": "unique_farmers", "value": df_cf["id"].nunique()},
            {"metric": "n_features_classifier", "value": len(CLUSTER_FEATS)},
            {"metric": "n_actionable_features", "value": len(ACTION_FEATS)},
        ]
    )
    summary.to_csv(TABLE_DIR / "data_summary.csv", index=False)

    cluster_counts = (
        y.value_counts()
        .sort_index()
        .rename_axis("cluster")
        .reset_index(name="n")
    )
    cluster_counts["cluster_name"] = cluster_counts["cluster"].map(CLUSTER_NAMES)
    cluster_counts.to_csv(TABLE_DIR / "cluster_counts_year0.csv", index=False)

    feature_roles = []
    for feat in CLUSTER_FEATS:
        if feat in ["age", "edu", "agri_long"]:
            role = "immutable_demographic"
        elif feat in ACTION_FEATS:
            role = "mutable_actionable_skill"
        elif feat in ["irriga", "loan"]:
            role = "contextual_binary_not_varied"
        else:
            role = "contextual_risk_not_varied"
        feature_roles.append(
            {
                "feature": feat,
                "role": role,
                "course_mapping": COURSE_MAPPING.get(feat, ""),
            }
        )
    pd.DataFrame(feature_roles).to_csv(TABLE_DIR / "feature_roles.csv", index=False)


def validate_classifier(x: pd.DataFrame, y: pd.Series, groups: pd.Series) -> RandomForestClassifier:
    model = RandomForestClassifier(**RF_PARAMS)
    model.fit(x, y)

    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "protocol": "full_data_training",
            "accuracy_mean": accuracy_score(y, model.predict(x)),
            "accuracy_sd": np.nan,
            "macro_f1_mean": f1_score(y, model.predict(x), average="macro"),
            "macro_f1_sd": np.nan,
            "note": "Training fit only; not a generalization estimate.",
        }
    )

    cv_protocols = [
        ("stratified_5fold", StratifiedKFold(n_splits=5, shuffle=True, random_state=42), None),
        ("group_5fold_by_farmer_id", GroupKFold(n_splits=5), groups),
    ]

    for name, cv, cv_groups in cv_protocols:
        fold_acc: list[float] = []
        fold_f1: list[float] = []
        for train_idx, test_idx in cv.split(x, y, groups=cv_groups):
            fold_model = RandomForestClassifier(**RF_PARAMS)
            fold_model.fit(x.iloc[train_idx], y.iloc[train_idx])
            pred = fold_model.predict(x.iloc[test_idx])
            fold_acc.append(accuracy_score(y.iloc[test_idx], pred))
            fold_f1.append(f1_score(y.iloc[test_idx], pred, average="macro"))

        pred_all = cross_val_predict(
            RandomForestClassifier(**RF_PARAMS),
            x,
            y,
            cv=cv,
            groups=cv_groups,
        )
        report = classification_report(
            y,
            pred_all,
            output_dict=True,
            zero_division=0,
        )
        report_df = pd.DataFrame(report).T.reset_index().rename(columns={"index": "class"})
        report_df.to_csv(TABLE_DIR / f"classifier_report_{name}.csv", index=False)

        cm = confusion_matrix(y, pred_all, labels=[0, 1, 2])
        pd.DataFrame(cm, index=["true_0", "true_1", "true_2"], columns=["pred_0", "pred_1", "pred_2"]).to_csv(
            TABLE_DIR / f"confusion_matrix_{name}.csv"
        )

        rows.append(
            {
                "protocol": name,
                "accuracy_mean": float(np.mean(fold_acc)),
                "accuracy_sd": float(np.std(fold_acc)),
                "macro_f1_mean": float(np.mean(fold_f1)),
                "macro_f1_sd": float(np.std(fold_f1)),
                "note": "GroupKFold is close to row-level CV because Year 0 has one row per farmer.",
            }
        )

    pd.DataFrame(rows).to_csv(TABLE_DIR / "classifier_validation_summary.csv", index=False)
    return model


def features_to_vary(vary_mode: str) -> list[str]:
    if vary_mode == "action_only":
        return ACTION_FEATS
    if vary_mode == "all_mutable":
        return [feat for feat in CLUSTER_FEATS if feat not in ["age", "edu", "agri_long"]]
    raise ValueError(f"Unknown vary_mode: {vary_mode}")


def permitted_range(row: pd.Series, x: pd.DataFrame, vary_feats: list[str]) -> dict[str, list[float]]:
    ranges = {}
    for feat in vary_feats:
        val = float(row[feat])
        if feat in ACTION_FEATS:
            ranges[feat] = [val, val + 0.01] if val >= 5.0 else [val, 5.0]
        else:
            ranges[feat] = [float(x[feat].min()), float(x[feat].max())]
    return ranges


def select_best_cf(
    rf_model: RandomForestClassifier,
    orig_row: pd.Series,
    cfs_df: pd.DataFrame,
    target_cluster: int,
) -> tuple[pd.Series | None, dict[str, Any]]:
    best_row = None
    best_metric = {
        "valid": 0,
        "sparsity": np.nan,
        "l1_positive": np.nan,
        "l1_normalized": np.nan,
        "actionability_rate": 0.0,
        "n_actionable_changes": 0,
    }

    for _, cf_row in cfs_df.iterrows():
        pred = int(rf_model.predict(pd.DataFrame([cf_row])[CLUSTER_FEATS])[0])
        if pred != target_cluster:
            continue

        action_diffs = {feat: float(cf_row[feat]) - float(orig_row[feat]) for feat in ACTION_FEATS}
        all_diffs = {feat: float(cf_row[feat]) - float(orig_row[feat]) for feat in CLUSTER_FEATS}
        changed = {feat: diff for feat, diff in all_diffs.items() if abs(diff) > 0.01}
        action_changes = {feat: diff for feat, diff in action_diffs.items() if diff >= 0.1}
        sparsity = len(changed)
        l1_positive = float(sum(diff for diff in all_diffs.values() if diff > 0.01))
        l1_normalized = l1_positive / len(CLUSTER_FEATS)
        metric = {
            "valid": 1,
            "sparsity": sparsity,
            "l1_positive": l1_positive,
            "l1_normalized": l1_normalized,
            "actionability_rate": len(action_changes) / len(ACTION_FEATS),
            "n_actionable_changes": len(action_changes),
        }

        if best_row is None:
            best_row = cf_row
            best_metric = metric
            continue

        if (sparsity, l1_positive) < (best_metric["sparsity"], best_metric["l1_positive"]):
            best_row = cf_row
            best_metric = metric

    return best_row, best_metric


def process_farmer(
    idx: int,
    row: pd.Series,
    source_cluster: int,
    target_cluster: int,
    rf_model: RandomForestClassifier,
    exp_dice: dice_ml.Dice,
    x: pd.DataFrame,
    vary_mode: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
    base_metric = {
        "farmer_row_index": idx,
        "source_cluster": source_cluster,
        "target_cluster": target_cluster,
        "path": f"C{source_cluster}->C{target_cluster}",
        "vary_mode": vary_mode,
        "valid": 0,
        "sparsity": np.nan,
        "l1_positive": np.nan,
        "l1_normalized": np.nan,
        "actionability_rate": 0.0,
        "n_actionable_changes": 0,
        "error": "",
    }
    plans: list[dict[str, Any]] = []
    cf_record = None

    try:
        farmer_profile = pd.DataFrame([row])
        vary_feats = features_to_vary(vary_mode)
        cf_res = exp_dice.generate_counterfactuals(
            farmer_profile,
            total_CFs=5,
            desired_class=target_cluster,
            features_to_vary=vary_feats,
            permitted_range=permitted_range(row, x, vary_feats),
            posthoc_sparsity_param=0.1,
        )
        if not cf_res or not cf_res.cf_examples_list:
            return base_metric, plans, cf_record

        cfs_df = cf_res.cf_examples_list[0].final_cfs_df
        if cfs_df is None or cfs_df.empty:
            return base_metric, plans, cf_record

        best_cf, metric = select_best_cf(rf_model, row, cfs_df, target_cluster)
        base_metric.update(metric)
        if best_cf is None:
            return base_metric, plans, cf_record

        cf_record = {
            "farmer_row_index": idx,
            "source_cluster": source_cluster,
            "target_cluster": target_cluster,
            "path": f"C{source_cluster}->C{target_cluster}",
            "vary_mode": vary_mode,
        }
        for feat in CLUSTER_FEATS:
            cf_record[f"orig_{feat}"] = float(row[feat])
            cf_record[f"cf_{feat}"] = float(best_cf[feat])
            cf_record[f"diff_{feat}"] = float(best_cf[feat]) - float(row[feat])

        for feat in ACTION_FEATS:
            diff = float(best_cf[feat]) - float(row[feat])
            if diff >= 0.1:
                plans.append(
                    {
                        "farmer_row_index": idx,
                        "source_cluster": source_cluster,
                        "target_cluster": target_cluster,
                        "path": f"C{source_cluster}->C{target_cluster}",
                        "vary_mode": vary_mode,
                        "feature": feat,
                        "course": COURSE_MAPPING[feat],
                        "increment": diff,
                    }
                )
    except Exception as exc:  # DiCE can fail for individual edge cases.
        base_metric["error"] = str(exc)

    return base_metric, plans, cf_record


def run_counterfactuals(
    x: pd.DataFrame,
    y: pd.Series,
    rf_model: RandomForestClassifier,
    n_jobs: int,
    limit_per_path: int | None,
    transitions: list[tuple[int, int]],
    vary_mode: str,
    backend: str,
) -> None:
    d_data = dice_ml.Data(
        dataframe=pd.concat([x, y.rename("Cluster")], axis=1),
        continuous_features=CLUSTER_FEATS,
        outcome_name="Cluster",
    )
    d_model = dice_ml.Model(model=rf_model, backend="sklearn", model_type="classifier")
    exp_dice = dice_ml.Dice(d_data, d_model, method="genetic")

    all_metrics: list[dict[str, Any]] = []
    all_plans: list[dict[str, Any]] = []
    all_cfs: list[dict[str, Any]] = []

    for source_cluster, target_cluster in transitions:
        samples = x[y == source_cluster]
        if limit_per_path is not None:
            samples = samples.head(limit_per_path)

        print(
            f"Processing C{source_cluster}->C{target_cluster}: {len(samples)} farmers "
            f"(vary_mode={vary_mode})",
            flush=True,
        )
        start = time.time()
        parallel_kwargs: dict[str, Any] = {"n_jobs": n_jobs, "verbose": 10}
        if backend == "threads":
            parallel_kwargs["prefer"] = "threads"
        elif backend == "loky":
            parallel_kwargs["backend"] = "loky"
        elif backend != "sequential":
            raise ValueError(f"Unknown backend: {backend}")

        if backend == "sequential":
            parallel_kwargs["n_jobs"] = 1

        outputs = Parallel(**parallel_kwargs)(
            delayed(process_farmer)(
                int(idx),
                row,
                source_cluster,
                target_cluster,
                rf_model,
                exp_dice,
                x,
                vary_mode,
            )
            for idx, row in samples.iterrows()
        )

        for metric, plans, cf_record in outputs:
            all_metrics.append(metric)
            all_plans.extend(plans)
            if cf_record is not None:
                all_cfs.append(cf_record)

        elapsed = time.time() - start
        path_metrics = pd.DataFrame([m for m in all_metrics if m["path"] == f"C{source_cluster}->C{target_cluster}"])
        print(
            f"  success={path_metrics['valid'].mean() * 100:.1f}% "
            f"sparsity={path_metrics.loc[path_metrics['valid'] == 1, 'sparsity'].mean():.2f} "
            f"l1={path_metrics.loc[path_metrics['valid'] == 1, 'l1_positive'].mean():.2f} "
            f"time={elapsed:.1f}s",
            flush=True,
        )

    metrics_df = pd.DataFrame(all_metrics)
    plans_df = pd.DataFrame(all_plans)
    cfs_df = pd.DataFrame(all_cfs)

    metrics_df.to_csv(TABLE_DIR / "cf_per_farmer_metrics.csv", index=False)
    plans_df.to_csv(TABLE_DIR / "cf_action_plans.csv", index=False)
    cfs_df.to_csv(TABLE_DIR / "cf_best_counterfactuals.csv", index=False)

    valid = metrics_df[metrics_df["valid"] == 1]
    summary = (
        metrics_df.groupby(["source_cluster", "target_cluster", "path"])
        .agg(
            n_evaluated=("valid", "size"),
            n_valid=("valid", "sum"),
            success_rate=("valid", "mean"),
        )
        .reset_index()
    )
    detail = (
        valid.groupby(["source_cluster", "target_cluster", "path"])
        .agg(
            sparsity_mean=("sparsity", "mean"),
            sparsity_sd=("sparsity", "std"),
            l1_positive_mean=("l1_positive", "mean"),
            l1_positive_sd=("l1_positive", "std"),
            l1_normalized_mean=("l1_normalized", "mean"),
            actionability_rate_mean=("actionability_rate", "mean"),
            n_actionable_changes_mean=("n_actionable_changes", "mean"),
        )
        .reset_index()
    )
    summary = summary.merge(detail, on=["source_cluster", "target_cluster", "path"], how="left")
    summary["success_rate"] = summary["success_rate"] * 100
    summary.to_csv(TABLE_DIR / "cf_transition_summary.csv", index=False)

    if not plans_df.empty:
        freq = (
            plans_df.groupby(["path", "feature", "course"])
            .agg(
                recommendation_count=("course", "size"),
                mean_increment=("increment", "mean"),
            )
            .reset_index()
        )
        path_n = metrics_df.groupby("path")["valid"].size().rename("n_evaluated").reset_index()
        freq = freq.merge(path_n, on="path", how="left")
        freq["recommendation_rate_percent"] = freq["recommendation_count"] / freq["n_evaluated"] * 100
        freq.to_csv(TABLE_DIR / "training_recommendation_frequency.csv", index=False)

        plt.figure(figsize=(11, 6))
        sns.countplot(data=plans_df, y="course", hue="path", palette="Set2")
        plt.title("Recommended Training Programs by Cluster Transition Path", fontsize=14)
        plt.xlabel("Frequency")
        plt.ylabel("Training Course")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "fig_training_recommendations.png", dpi=300)
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-cf", action="store_true", help="Only run preprocessing and classifier validation.")
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument("--limit-per-path", type=int, default=None)
    parser.add_argument(
        "--transitions",
        default="0-1,1-2,0-2",
        help="Comma-separated source-target pairs, e.g. 0-1,1-2.",
    )
    parser.add_argument(
        "--vary-mode",
        choices=["action_only", "all_mutable"],
        default="all_mutable",
        help="DiCE feature variation mode. Recommendations are always mapped only from actionable skill features.",
    )
    parser.add_argument(
        "--backend",
        choices=["sequential", "threads", "loky"],
        default="sequential",
        help="Joblib backend. Use loky for process-parallel runs outside sandbox.",
    )
    args = parser.parse_args()

    ensure_dirs()
    df_cf, x, y, groups = load_baseline()
    export_data_summary(df_cf, y)
    rf_model = validate_classifier(x, y, groups)

    run_meta = {
        "project_dir": str(PROJECT_DIR),
        "data_path": str(DATA_PATH),
        "n_baseline_records": int(len(df_cf)),
        "n_unique_farmers": int(df_cf["id"].nunique()),
        "classifier_features": CLUSTER_FEATS,
        "actionable_features": ACTION_FEATS,
        "rf_params": RF_PARAMS,
    }
    (OUT_DIR / "run_metadata.json").write_text(json.dumps(run_meta, indent=2))

    if not args.skip_cf:
        transitions = []
        for item in args.transitions.split(","):
            source, target = item.split("-")
            transitions.append((int(source), int(target)))
        run_counterfactuals(
            x,
            y,
            rf_model,
            args.n_jobs,
            args.limit_per_path,
            transitions,
            args.vary_mode,
            args.backend,
        )

    print(f"Done. Outputs written to {OUT_DIR}")


if __name__ == "__main__":
    main()
