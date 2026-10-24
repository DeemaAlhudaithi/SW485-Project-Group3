# Meeting Notes — Phase 1

**SW485-Project-Group3**

---

## Meeting 1 — Task Distribution 

- **Format:** [online]
- **Attendees:** [all team members]

**Agenda**
1. Review the Phase 1 requirements
2. Distribute the roles among the six members
3. Agree on how the work will be shared (repository, shared split)

**Discussion and decisions**
- The work was divided into six roles, so that every member owns one part of the pipeline (see `task_distribution.md`).
- Preprocessing is done once by one member and shared as the same train/test files, so all models are compared on identical data.
- Each model (Logistic Regression, Random Forest, XGBoost) has its own member, and the comparative analysis and final model selection is a shared task.


**Action items**

| Task | Owner |
|------|-------|
| Repository structure, problem statement, dataset justification, final conclusion | Deema Alhudaithi |
| EDA and results visualization | Lina Almarouti |
| Preprocessing and data pipeline (`preprocessed_data.csv`, cross-validation setup) | Danah Aldhalaan |
| Logistic Regression | Nouf Alotaibi |
| Random Forest and feature importance | Dalia Almawash |
| XGBoost | Lamia Alromi |
| Comparative analysis and final model selection | Lina, Danah, Nouf, Dalia, Lamia |
---

## Meeting 2 

- **Format:** [online]
- **Attendees:** [all members]


**Agenda**
1. EDA findings (Lina)
2. Preprocessing pipeline and its decisions (Dana)
3. How each member loads and uses the shared files

**Discussion and decisions**
- Lina presented the EDA: the classes are balanced (50/50), and the main relationships with diabetes (age, BMI, general health, blood pressure).
- Dana explained the preprocessing pipeline and the reason behind each decision:
  - Duplicate rows were removed before the split, so identical rows cannot appear in both train and test.
  - BMI was capped at the 99th percentile (52.0) instead of removing rows, to limit extreme values while keeping informative records.
  - No encoding was needed, since all columns are numeric; near-constant features were kept.
  - The split is stratified 80/20 with `random_state=42`, and shared by all models.
  - Scaling is applied for Logistic Regression only (fitted on the training set); Random Forest and XGBoost use the unscaled files.
  - Cross-validation uses 5 stratified folds on the training set only.
- The team agreed that every model reads the shared train/test files instead of splitting or cleaning the data again.

**Action items**

| Task | Owner |
|------|-------|
| Load the shared files, tune and evaluate the model | Nouf, Dalia, Lamia |

---

## Meeting 3 — [Date]

- **Format:** [online]
- **Attendees:** [all members]


**Agenda**
1. Logistic Regression: model, tuning and results (Nouf)
2. Random Forest: model, tuning and results (Dalia)
3. XGBoost: model, tuning and results (Lamia)
4. Comparison of the three models

**Discussion and decisions**
- Each member presented her model, the tuned hyperparameters, and the evaluation results on the shared test set:
  - Logistic Regression (`C=0.1`): Recall 0.7738, F1 0.7557, ROC-AUC 0.8184.
  - Random Forest (`n_estimators=100`, `max_depth=10`): Recall 0.7973, F1 0.7610, ROC-AUC 0.8198.
  - XGBoost (`n_estimators=200`, `max_depth=5`, `learning_rate=0.05`): Recall 0.8041, F1 0.7660, ROC-AUC 0.8241.
- Each member explained her confusion matrix and error analysis (which at-risk cases the model misses).
- The three models perform within a close range, so the comparison focuses on Recall and F1, which matter most for a screening tool.


---
## Meeting 4 — Final Review

- **Format:** online
- **Attendees:** all members

**Agenda**
1. Review of the model comparison notebook (`Phase1_Supervised_Learning.ipynb`)
2. Check against the project description document
3. Final run and review plan

**Discussion and decisions**
- Deemah explained the model comparison notebook to the team, and the team reviewed it together.
- The team reviewed the project description document and checked that every Phase 1 requirement was covered.
- The notebooks were run again to confirm that they work from start to finish.
- Each member will keep reviewing her own part until the submission day.

**Action items**

| Task | Owner |
|------|-------|
| Review own notebook and files until the submission day | All members |