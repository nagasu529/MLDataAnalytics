# DataAnalysis.ipynb

This notebook contains the full analytical workflow for the Smart Farmer Program study.  
It integrates data cleaning, causal analysis, machine learning, explainability, and clustering  
into a single reproducible pipeline.

---

## 1. Data Loading & Cleaning
- Loads panel data from `SFProgramDataPanal.csv`
- Converts special symbols (e.g., '.') to numeric values
- Handles missing values using appropriate imputation rules
- Constructs feature groups based on economic theory:
  - Human capital
  - Production assets
  - Financial risk
  - Social capital
  - Baseline skills

---

## 2. Objective 1 — Skill Change Analysis
### 2.1 Difference-in-Differences (DiD)
- Computes before/after skill changes for SF vs Non-SF groups  
- Generates DiD tables and visualizations  
- Includes parallel trend plots

### 2.2 Correlation Analysis
- Pearson correlation between skill change and training characteristics  
- Heatmap visualization for SF participants

### 2.3 OLS Regression
- Model 1: Training characteristics → Skill change  
- Model 2: Training + Demographics → Skill change  
- Includes coefficient tables, significance levels, and coefficient plots  
- Per-skill regression summary

### 2.4 SHAP Analysis (Regression)
- Random Forest Regressor on SF participants  
- SHAP Beeswarm plot  
- SHAP Mean |SHAP| bar plot  
- Identifies global and local determinants of skill change

---

## 3. Objective 2 — Smart Farming Learning Framework
### 3.1 Clustering (K-Means)
- Uses demographic, skill, and risk variables  
- Elbow method + Silhouette score to determine optimal k  
- Cluster assignment and distribution

### 3.2 Cluster Profiles
- Mean profiles of each cluster  
- Radar chart visualization of skill profiles

### 3.3 PCA Visualization
- 2D PCA projection of clusters  
- Visualization of SF vs Non-SF distribution

### 3.4 Random Forest + SHAP (Full Dataset)
- RF Regressor on all participants  
- Feature importance bar plot  
- Prepares for SHAP dependence plots (optional)

---

## 4. Classification Models (Optional Section)
- XGBoost / RandomForest classification for predicting success (Ch_Skill > 0)
- Confusion matrix and classification report
- SHAP explainability for classification (optional)

---

## 5. Outputs
The notebook generates the following figures:

- `fig_DiD.png`  
- `fig_Correlation.png`  
- `fig_Regression.png`  
- `fig_SHAP_Beeswarm.png`  
- `fig_SHAP_Bar.png`  
- `fig_Elbow.png`  
- `fig_RadarCluster.png`  
- `fig_PCA.png`

These figures are used directly in the manuscript.

---

## 6. Revision Summary
This version includes:
- Cleaned and unified feature definitions  
- Consistent preprocessing across all models  
- Standardized evaluation for regression and classification  
- Complete SHAP explainability pipeline  
- Full clustering + PCA workflow  
- Publication-ready visualizations  
- Alignment with the finalized Methodology and Discussion sections

---

## Purpose
This notebook serves as the **master analysis file** for the Smart Farmer Program study,  
covering causal inference, machine learning, explainability, and segmentation  
in a single coherent workflow.
