"""
cluster_interface.py — shared interface between Part A (Clustering) and the rest of the team.

FINAL VERSION — uses the trained K-Means model (k = 3) chosen in
Phase2_Unsupervised_Learning.ipynb (Section 5).

Used by:
  - GenAI (Part B): the profile text fills the {cluster_profile} placeholder in the prompts
  - Dashboard (Part C): show the patient's risk segment next to the prediction
  - Integration pipeline: call assign_cluster() after the supervised prediction

Required files (same folder as this script):
  - cluster_model.joblib   -> {"scaler", "model", "feature_names"}
  - cluster_profiles.json  -> segment name, description, size % and diabetic % per cluster
"""

import json
from pathlib import Path

import joblib
import pandas as pd

_HERE = Path(__file__).resolve().parent
_BUNDLE = joblib.load(_HERE / "cluster_model.joblib")
with open(_HERE / "cluster_profiles.json", encoding="utf-8") as f:
    CLUSTER_PROFILES = {int(k): v for k, v in json.load(f).items()}

FEATURE_NAMES = _BUNDLE["feature_names"]   # the 21 features, in training order


def assign_cluster(patient_features: dict) -> tuple[int, str]:
    """
    Assign one patient to a risk segment.

    Input : dict with the 21 patient features, using the ORIGINAL (unscaled) values
            and the same column names as Dataset/train_data.csv, e.g.
            {"HighBP": 1, "HighChol": 1, "BMI": 31, "Age": 9, ...}
    Output: (cluster_id, cluster_profile_text)
            cluster_id: 1 = Low risk, 0 = Moderate risk, 2 = High risk
    """
    missing = [c for c in FEATURE_NAMES if c not in patient_features]
    if missing:
        raise ValueError(f"Missing features: {missing}")

    x = pd.DataFrame([patient_features])[FEATURE_NAMES]
    cluster_id = int(_BUNDLE["model"].predict(_BUNDLE["scaler"].transform(x))[0])
    return cluster_id, CLUSTER_PROFILES[cluster_id]["description"]


def get_segment_info(cluster_id: int) -> dict:
    """Full info for the dashboard: segment name, description, size % and diabetic %."""
    return CLUSTER_PROFILES[cluster_id]


if __name__ == "__main__":
    example = {
        "HighBP": 1, "HighChol": 1, "CholCheck": 1, "BMI": 33, "Smoker": 1, "Stroke": 0,
        "HeartDiseaseorAttack": 1, "PhysActivity": 0, "Fruits": 0, "Veggies": 1,
        "HvyAlcoholConsump": 0, "AnyHealthcare": 1, "NoDocbcCost": 0, "GenHlth": 4,
        "MentHlth": 10, "PhysHlth": 20, "DiffWalk": 1, "Sex": 0, "Age": 10,
        "Education": 4, "Income": 3,
    }
    cid, text = assign_cluster(example)
    print(cid, get_segment_info(cid)["segment"], "-", text)
