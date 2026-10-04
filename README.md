# Executive Clinical Screening & Triage Decision-Support Tool

**SWE485: Selected Topics in Software Engineering — King Saud University**
**Group 3 — 1st Semester 1448**

## Team Members

| Name | Student ID |
|------|-----------|
| Lina Almarouti | 445201347 |
| Nouf Alotaibi | 445202229 |
| Deema Alhudaithi | 445200365 |
| Danah Aldhalaan | 445201437 |
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
├── Phase1_Data_Exploration.ipynb
├── Phase1_Supervised_Learning.ipynb
├── Dataset/
│   ├── raw dataset (.csv)
│   ├── preprocessed_data.csv
│   └── dataset_info.txt
├── Supervised_Learning/
│   ├── models/
│   ├── evaluation_results/
│   └── plots/
└── docs/
```


## Project Phases

- **Phase 1:** Problem Understanding & Data Exploration, Supervised Learning
- **Phase 2:** Unsupervised Learning, Generative AI, Interactive Executive Dashboard
