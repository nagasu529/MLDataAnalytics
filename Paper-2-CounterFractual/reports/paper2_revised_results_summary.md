# Paper 2 Revised Pipeline Results

Date: 2026-08-20

Script:
- `scripts/paper2_revised_pipeline.py`

Final output directory:
- `paper2_outputs/`

Execution used for final CF tables:

```bash
/Users/nagasu/miniforge3/envs/data-ai/bin/python -u scripts/paper2_revised_pipeline.py \
  --n-jobs -1 \
  --backend loky \
  --transitions 0-1,1-2,0-2 \
  --vary-mode all_mutable
```

Important reproducibility note:
- `backend=threads` caused DiCE internal errors and invalid CF rows.
- `backend=loky` process-parallel completed without errors.
- Do not use thread-mode outputs for publication.

## Dataset

The revised Paper 2 pipeline uses baseline Year 0 records only.

| Item | Value |
|---|---:|
| Baseline records | 417 |
| Unique farmers | 417 |
| Classifier features | 15 |
| Actionable skill features | 6 |

Year 0 cluster distribution:

| Cluster | Name | N |
|---:|---|---:|
| 0 | Low-skill | 153 |
| 1 | Moderate-skill | 119 |
| 2 | High-skill | 145 |

## Classifier Validation

Model:
- `RandomForestClassifier`
- `n_estimators=500`
- `min_samples_leaf=10`
- `max_features='sqrt'`
- `random_state=42`

| Protocol | Accuracy mean | Accuracy SD | Macro-F1 mean | Macro-F1 SD |
|---|---:|---:|---:|---:|
| Full-data training | 0.9640 | NA | 0.9642 | NA |
| Stratified 5-fold CV | 0.9425 | 0.0176 | 0.9437 | 0.0171 |
| GroupKFold by farmer ID | 0.9401 | 0.0329 | 0.9410 | 0.0316 |

Recommended paper value:
- Use Stratified 5-fold or GroupKFold result, not full-data training accuracy.
- If GroupKFold is reported, explicitly note that Year 0 contains one row per farmer, so grouping by farmer ID is practically close to row-level splitting.

## Counterfactual Setup

Model explained:
- Final Random Forest classifier trained on all 417 baseline records.

DiCE:
- `method='genetic'`
- `total_CFs=5`
- `posthoc_sparsity_param=0.1`

Feature variation mode used for final run:
- `all_mutable`

Immutable:
- `age`
- `edu`
- `agri_long`

Allowed to vary:
- `irriga`
- `loan`
- six skill features
- four risk features

Monotonic non-decreasing ranges are imposed only on the six skill/actionable features:
- `Avg_ProdManage`
- `Avg_InputManage`
- `Avg_Tech`
- `Avg_Ana&Plan`
- `Avg_Mkting`
- `Avg_Network`

Recommendation mapping is restricted to the six actionable skill features only.

Publication caveat:
- The paper should not claim that all features obey strict monotonic constraints.
- Correct claim: monotonic constraints are imposed on training-actionable skill features, while other mutable/contextual variables may be varied by the CF generator to locate feasible model transitions.

## CF Quality Results

| Transition | N evaluated | Valid CFs | Success rate | Mean sparsity | SD sparsity | Mean L1 | SD L1 | Mean actionable changes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C0 -> C1 | 153 | 153 | 100.0% | 5.51 | 1.69 | 3.89 | 1.86 | 0.67 |
| C1 -> C2 | 119 | 119 | 100.0% | 6.29 | 1.59 | 1.97 | 1.57 | 1.51 |
| C0 -> C2 | 153 | 153 | 100.0% | 6.17 | 1.90 | 3.26 | 2.02 | 2.16 |

Note:
- Sparsity and L1 are computed across the classifier feature space.
- Training recommendations are counted only when one of the six actionable skill features increases by at least 0.1.

## Training Recommendation Frequency

### C0 -> C1

| Course | Count | Rate |
|---|---:|---:|
| Marketing and Value Addition | 30 | 19.6% |
| Input and Resource Optimization | 22 | 14.4% |
| Agri-Business Analysis and Planning | 20 | 13.1% |
| Production Management | 19 | 12.4% |
| Network Building | 11 | 7.2% |
| Technology Adoption | 1 | 0.7% |

### C1 -> C2

| Course | Count | Rate |
|---|---:|---:|
| Agri-Business Analysis and Planning | 77 | 64.7% |
| Marketing and Value Addition | 41 | 34.5% |
| Network Building | 34 | 28.6% |
| Technology Adoption | 16 | 13.4% |
| Input and Resource Optimization | 8 | 6.7% |
| Production Management | 4 | 3.4% |

### C0 -> C2

| Course | Count | Rate |
|---|---:|---:|
| Agri-Business Analysis and Planning | 108 | 70.6% |
| Marketing and Value Addition | 78 | 51.0% |
| Network Building | 60 | 39.2% |
| Input and Resource Optimization | 36 | 23.5% |
| Technology Adoption | 32 | 20.9% |
| Production Management | 17 | 11.1% |

## Manuscript Revision Implications

Replace the previous classifier claim:

> Evaluated via 5-fold GroupKFold cross-validation, the model achieved 93.05% accuracy.

With:

> The Random Forest surrogate classifier achieved 94.25% accuracy (macro-F1 = 94.37%) under stratified 5-fold cross-validation. A farmer-grouped 5-fold split yielded a similar accuracy of 94.01% (macro-F1 = 94.10%).

Replace the previous CF quality values:

> average sparsity 2.76 and L1 2.32

With transition-specific values from the revised run:

> The GA-based DiCE procedure generated valid CFs for 100% of evaluated cases. Mean sparsity ranged from 5.51 to 6.29 changed features, while mean positive L1 distance ranged from 1.97 to 3.89 across transition paths.

Do not write:

> strict monotonic constraints (Delta X >= 0)

Write:

> monotonic non-decreasing constraints on six training-actionable skill features

## Next Writing Tasks

1. Rewrite Methodology to separate SAR-derived clustering from Paper 2 CF generation.
2. Rewrite Experiments section using `paper2_outputs/tables/`.
3. Update Results figures using `paper2_outputs/figures/fig_training_recommendations.png`.
4. Add a limitation that CFs are model-implied transitions, not causal evidence.
5. Add a limitation that non-skill contextual variables may vary in the CF search, while final recommendations are mapped only from skill increases.

