# Executive Clinical Screening & Triage Decision-Support Tool

**SWE485: Selected Topics in Software Engineering — King Saud University**
**Group 3 — 1st Semester 1448**

## Team Members

| Name | Student ID |
|------|-----------|
| Lina Almarouti | 445201347 |
| Nouf Alotaibi | 445202229 |
| Deema Alhudaithi | 445200365 |
| Dana Aldalaan | 445201437 |
| Lamia Alromi | 445203040 |
| Dalia Almawash | 445201330 |

## Project Motivation

Diabetes is one of the most widespread chronic diseases, and many people with
prediabetes or diabetes remain undiagnosed until complications appear. Early
screening allows healthcare organizations to intervene sooner and allocate
clinical resources more effectively.

This project builds an executive decision-support system that helps healthcare
professionals perform early screening and prioritize individuals who may need
further clinical assessment. The system uses health and lifestyle indicators
such as BMI, blood pressure, cholesterol, physical activity, smoking, age, and
general health to classify screening status.

> ⚠️ This system is a screening and decision-support tool, **not** a medical
> diagnosis tool.

## Why This Dataset?

We use the **Diabetes Health Indicators Dataset** from Kaggle, specifically the
file `diabetes_binary_5050split_health_indicators_BRFSS2015.csv`:

- **70,692 records** and **21 predictor features** covering health,
  demographic, and lifestyle indicators.
- **Balanced binary target** (`Diabetes_binary`): 0 = No Diabetes,
  1 = Prediabetes or Diabetes, split 50/50.
- Structured and tabular, which makes it suitable for supervised
  classification, EDA, and unsupervised clustering (after removing the target).

Source: https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset

## Repository Structure
```
SW485-Project-Group3/
├── README.md
├── Phase1_Data_Exploration.ipynb        # Part A: problem, EDA, preprocessing
├── Phase1_Supervised_Learning.ipynb     # Part B: model comparison & final selection
├── Dataset/
│   ├── diabetes_binary_5050split_health_indicators_BRFSS2015.csv   # raw dataset
│   ├── preprocessed_data.csv
│   ├── train_data.csv / test_data.csv                 # shared train/test split
│   ├── train_data_scaled.csv / test_data_scaled.csv   # scaled version (Logistic Regression)
│   └── dataset_info.txt
├── EDA_plots/                           # plots from the data exploration
├── Supervised_Learning/
│   ├── Phase1_Logistic_Regression.ipynb
│   ├── Phase1_Random_Forest.ipynb
│   ├── Phase1_XGBoost.ipynb
│   ├── models/
│   ├── evaluation_results/
│   └── plots/
└── docs/
```

## Use of AI Tools
Claude (Anthropic) was used to help structure the model comparison notebook and organize its Markdown explanations. All models, preprocessing, tuning and evaluation results were produced by the team, and all outputs were reviewed and verified by the team members.
**Preprocessing :** we used AI to review the cleaned data and the repository for consistency, and pointed out a possible minor leakage in the Logistic Regression cross-validation scores (the scaler was fitted on the full training set before the folds). Its effect is negligible, so we documented it as a limitation in the notebook instead of changing the pipeline.


## Project Phases

- **Phase 1:** Problem Understanding & Data Exploration, Supervised Learning
- **Phase 2:** Unsupervised Learning, Generative AI, Interactive Executive Dashboard

## References
1. M. A. Salari and B. Rahmani, "Machine Learning for Everyone: Simplifying Healthcare Analytics with BigQuery ML," arXiv:2502.07026, 2025.
