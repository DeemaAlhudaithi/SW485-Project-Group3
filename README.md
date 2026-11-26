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
├── app.py                               # Streamlit dashboard (Phase 2, Part C)
├── pipeline.py                          # Integration: XGBoost + clustering + GenAI
├── requirements.txt
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
├── Unsupervised_Learning/               # Phase 2, Part A: clustering
│   ├── Phase2_Unsupervised_Learning.ipynb
│   ├── cluster_interface.py
│   ├── cluster_model.joblib
│   └── cluster_profiles.json
├── Generative_AI/                       # Phase 2, Part B: prompt templates
│   ├── Phase2_Generative_AI.ipynb
│   └── example_outputs/
└── docs/
```

## Literature Check

To check that our results are reasonable, we compared them with a published study that used the same dataset (Salari and Rahmani, 2025 [1]). Their boosted tree model also performed best, and HighBP and GenHlth were the strongest predictors, followed by Age, BMI and HighChol. Our results agree in direction: XGBoost is the best model, the three models perform within a close range, and the same features dominate. Absolute numbers are not directly comparable, since the paper does not report duplicate removal and the hyperparameters differ.

## Executive Decision-Making Interface & Dashboard (Phase 2)

**Live dashboard:** https://sw485-group3-diabetes.streamlit.app/

### Dashboard Setup
Run locally from the repository root:
```
pip install -r requirements.txt
streamlit run app.py
```
To enable the AI summary, create a local `.env` file containing `GROQ_API_KEY=<your key>`
(the file is excluded from the repository). On the deployed app the key is stored in Streamlit Secrets.
Note: the app uses the `requirements.txt` in the repository root.

### Visual Analytics Integration
- **Scenario sliders and inputs:** all 21 health indicators can be adjusted in the sidebar
  (core indicators first, the rest under "Advanced options"; initial values are the training-data medians).
- **Confidence metrics:** a risk gauge showing the estimated diabetes probability, the referral threshold, and the screening result.
- **Risk segment:** the patient's cluster, its description, its size and its diabetic rate.
- **Key driver chart:** XGBoost feature importance.
- **Scenario analysis:** a "what if" tab that compares the current risk with the risk after changing selected factors, and shows which single change lowers the risk most.
- **Executive Overview (KPIs):** system-performance indicators (share of at-risk people detected, share referred, missed cases, correct referrals) with an adjustable referral threshold.
- **AI-generated summary:** a plain-language explanation produced by the GenAI component.

### Integration Strategy
`pipeline.py` exposes one function, `predict_patient()`, used by the dashboard:
1. The patient's 21 indicators go to the **XGBoost** model, which returns a risk probability.
2. The same indicators go to the **K-Means** model (`cluster_interface.py`), which returns the risk segment.
3. The probability, segment and top model drivers fill **Prompt Template 1**, and the LLM (Groq, `openai/gpt-oss-20b`) writes the summary.
4. The dashboard displays one combined result.

Design decisions:
- **Decision threshold 0.35** instead of 0.5. The tool is for screening, so missing an at-risk person is costlier than an extra referral. On the test set this gives Recall ≈ 90.6% and Precision ≈ 68.1% (0.5 gives 80.4% and 73.1%).
- **Complementary roles:** XGBoost gives the individual risk; clustering gives the group context; GenAI explains the results and never diagnoses.
- **Safe failure:** if the GenAI call fails or no API key is set, a fixed fallback message is shown and the app keeps working.
- **Secrets:** the API key is never stored in the repository.

### Limitations
The models are trained on 2015 BRFSS survey data (balanced 50/50 sample), so predicted probabilities
are not population prevalence. The tool supports screening only and does not replace medical advice.

## Use of AI Tools
Claude (Anthropic) was used to help structure the model comparison notebook and organize its Markdown explanations. All models, preprocessing, tuning and evaluation results were produced by the team, and all outputs were reviewed and verified by the team members.

**Preprocessing :** we used AI to review the cleaned data and the repository for consistency, and pointed out a possible minor leakage in the Logistic Regression cross-validation scores (the scaler was fitted on the full training set before the folds). Its effect is negligible, so we documented it as a limitation in the notebook (Section 5.8 of `Phase1_Data_Exploration.ipynb`) instead of changing the pipeline.


## Project Phases

- **Phase 1:** Problem Understanding & Data Exploration, Supervised Learning
- **Phase 2:** Unsupervised Learning, Generative AI, Interactive Executive Dashboard

## References
1. M. A. Salari and B. Rahmani, "Machine Learning for Everyone: Simplifying Healthcare Analytics with BigQuery ML," arXiv:2502.07026, 2025.
