"""
pipeline.py — integration layer (Phase 2, Part D).

One function, predict_patient(), connects:
  1. Supervised model (XGBoost)            -> risk probability
  2. Clustering (cluster_interface.py)     -> risk segment
  3. GenAI summary (Part B)                -> plain-language text

The dashboard (app.py) only calls predict_patient() and displays the returned dict.
Run the app from the repository root folder.
"""

import os
from pathlib import Path

import joblib
import pandas as pd

from Unsupervised_Learning.cluster_interface import assign_cluster, get_segment_info

_ROOT = Path(__file__).resolve().parent

# Screening threshold (instead of the default 0.5): a missed at-risk person costs more
# than an extra referral. Test set: Recall ~90.6%, Precision ~68.1%
# (see Phase1_Supervised_Learning.ipynb, Section 6.1).
THRESHOLD = 0.35

# The 21 features, in the same order used in training.
FEATURE_NAMES = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
    "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
    "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income",
]

# Values used for features the dashboard does not ask for (median of Dataset/train_data.csv).
DEFAULTS = {
    "HighBP": 1, "HighChol": 1, "CholCheck": 1, "BMI": 29, "Smoker": 0, "Stroke": 0,
    "HeartDiseaseorAttack": 0, "PhysActivity": 1, "Fruits": 1, "Veggies": 1,
    "HvyAlcoholConsump": 0, "AnyHealthcare": 1, "NoDocbcCost": 0, "GenHlth": 3,
    "MentHlth": 0, "PhysHlth": 0, "DiffWalk": 0, "Sex": 0, "Age": 9,
    "Education": 5, "Income": 6,
}

GENAI_FALLBACK = (
    "AI summary is not available right now. This tool is a screening aid, not a diagnosis. "
    "Please discuss your result with a healthcare professional."
)

_MODEL = joblib.load(_ROOT / "Supervised_Learning" / "models" / "xgboost_model.joblib")


# Same wording as PROMPT_TEMPLATE_1 in Generative_AI/Phase2_Generative_AI.ipynb (keep in sync).
PROMPT_TEMPLATE_1 = """
You are an assistant for a healthcare screening decision-support system.

Your role is to explain outputs produced by existing machine learning models.
Do not make an independent medical diagnosis.
Do not introduce facts that are not supported by the provided information.

Patient screening information:

Supervised model output:
- Screening result: {prediction}
- Prediction confidence: {probability}

Key contributing indicators:
{top_features}

Clustering output:
- Risk segment: {cluster_segment}
- Cluster profile: {cluster_profile}

Generate a concise individual patient briefing with these sections:

1. Screening Summary
2. Key Contributing Indicators
3. Risk Segment Context
4. Suggested Follow-up Considerations

Requirements:
- Use clear, non-technical language.
- Do not describe the result as a confirmed diagnosis.
- Do not invent medical information.
- Clearly distinguish the individual prediction confidence from the cluster-level profile.
- Keep the response concise and suitable for decision support.
"""

GENAI_MODEL = "openai/gpt-oss-20b"          # same model as the GenAI notebook (served by Groq)
GENAI_BASE_URL = "https://api.groq.com/openai/v1"


def _get_api_key():
    """GROQ_API_KEY from the environment/.env (local) or Streamlit secrets (deployed)."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None
    return key


def _top_features(n: int = 3) -> str:
    """Global top-n features of the model (same style as the GenAI test cases)."""
    fi = pd.read_csv(_ROOT / "Supervised_Learning" / "evaluation_results" / "feature_importance.csv")
    return ", ".join(fi.sort_values("Importance", ascending=False)["Feature"].head(n))


def get_genai_text(risk_probability: float, cluster_name: str, cluster_description: str,
                   patient: dict) -> str:
    """Fill Prompt Template 1 and call the LLM. Any failure returns GENAI_FALLBACK."""
    try:
        api_key = _get_api_key()
        if not api_key:
            return GENAI_FALLBACK
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=GENAI_BASE_URL, timeout=30)
        prompt = PROMPT_TEMPLATE_1.format(
            prediction=("Further clinical assessment recommended"
                        if risk_probability >= THRESHOLD else "Lower screening concern"),
            probability=f"{risk_probability:.0%}",
            top_features=_top_features(),
            cluster_segment=cluster_name,
            cluster_profile=cluster_description,
        )
        response = client.responses.create(model=GENAI_MODEL, input=prompt)
        return response.output_text or GENAI_FALLBACK
    except Exception:
        return GENAI_FALLBACK


def predict_patient(user_inputs: dict) -> dict:
    """user_inputs: any subset of the 21 features (original, unscaled values)."""
    patient = {**DEFAULTS, **user_inputs}
    x = pd.DataFrame([patient])[FEATURE_NAMES]

    risk = float(_MODEL.predict_proba(x)[0, 1])
    cluster_id, _ = assign_cluster(patient)
    info = get_segment_info(cluster_id)

    return {
        "risk_probability": risk,
        "threshold": THRESHOLD,
        "high_risk": risk >= THRESHOLD,
        "cluster_id": cluster_id,
        "cluster_name": info["segment"],
        "cluster_description": info["description"],
        "cluster_size_pct": info["size_pct"],
        "cluster_diabetic_pct": info["diabetic_pct"],
        "genai_text": get_genai_text(risk, info["segment"], info["description"], patient),
    }


if __name__ == "__main__":
    print(predict_patient({"BMI": 33, "HighBP": 1, "GenHlth": 4, "Age": 10}))
