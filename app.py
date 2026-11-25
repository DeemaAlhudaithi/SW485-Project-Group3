"""
app.py — Streamlit dashboard (Phase 2, Part C).
Run from the repository root:  streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from pipeline import predict_patient, _MODEL, FEATURE_NAMES
ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Diabetes Risk Screening", page_icon="🩺", layout="wide")

AGE_GROUPS = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
              "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
EDUCATION = {1: "Never attended / kindergarten", 2: "Elementary", 3: "Some high school",
             4: "High school graduate", 5: "Some college", 6: "College graduate"}
INCOME = {1: "< $10k", 2: "$10-15k", 3: "$15-20k", 4: "$20-25k",
          5: "$25-35k", 6: "$35-50k", 7: "$50-75k", 8: "$75k+"}
GENHLTH = {1: "Excellent", 2: "Very good", 3: "Good", 4: "Fair", 5: "Poor"}
SEGMENT_COLORS = {"Low risk": "#2E7D32", "Moderate risk": "#F9A825", "High risk": "#C62828"}


def yes_no(label, key, default=False):
    return int(st.checkbox(label, value=default, key=key))


st.title("🩺 Diabetes Risk Screening Dashboard")
st.caption("Screening aid based on CDC BRFSS 2015 data. Not a medical diagnosis.")

with st.sidebar:
    st.header("Patient information")
    bmi = st.slider("BMI", 13.0, 52.0, 29.0, 0.5)
    age_label = st.select_slider("Age group", options=AGE_GROUPS, value="55-59")
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    genhlth = st.select_slider("General health", options=list(GENHLTH), value=3,
                               format_func=lambda v: GENHLTH[v])
    st.subheader("Conditions & lifestyle")
    highbp = yes_no("High blood pressure", "bp", True)
    highchol = yes_no("High cholesterol", "chol", True)
    diffwalk = yes_no("Difficulty walking", "walk")
    heart = yes_no("Heart disease / heart attack", "heart")
    stroke = yes_no("Stroke", "stroke")
    smoker = yes_no("Smoker", "smoke")
    physact = yes_no("Physically active (last 30 days)", "act", True)
    with st.expander("Advanced options"):
        physhlth = st.slider("Days of poor physical health (last 30)", 0, 30, 0)
        menthlth = st.slider("Days of poor mental health (last 30)", 0, 30, 0)
        education = st.selectbox("Education", list(EDUCATION), index=4,
                                 format_func=lambda v: EDUCATION[v])
        income = st.selectbox("Income", list(INCOME), index=5, format_func=lambda v: INCOME[v])
        fruits = yes_no("Eats fruit daily", "fruit", True)
        veggies = yes_no("Eats vegetables daily", "veg", True)
        alcohol = yes_no("Heavy alcohol consumption", "alc")
        cholcheck = yes_no("Cholesterol checked in last 5 years", "cc", True)
        anyhc = yes_no("Has health coverage", "hc", True)
        nodoc = yes_no("Could not see doctor due to cost", "nodoc")

inputs = {
    "BMI": bmi, "Age": AGE_GROUPS.index(age_label) + 1, "Sex": int(sex == "Male"),
    "GenHlth": genhlth, "HighBP": highbp, "HighChol": highchol, "DiffWalk": diffwalk,
    "HeartDiseaseorAttack": heart, "Stroke": stroke, "Smoker": smoker, "PhysActivity": physact,
    "PhysHlth": physhlth, "MentHlth": menthlth, "Education": education, "Income": income,
    "Fruits": fruits, "Veggies": veggies, "HvyAlcoholConsump": alcohol,
    "CholCheck": cholcheck, "AnyHealthcare": anyhc, "NoDocbcCost": nodoc,
}
res = predict_patient(inputs)
pct = res["risk_probability"] * 100
thr = res["threshold"] * 100

# Three tabs: one patient, what-if scenarios, and an overview for decision-makers
tab_patient, tab_scenario, tab_exec = st.tabs(
    [" Patient Screening", "Scenario Analysis", "Executive Overview"]
)

# ---------------- Tab 1: Patient Screening ----------------
with tab_patient:
    c1, c2 = st.columns(2)
    with c1:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=pct, number={"suffix": "%"},
            title={"text": "Estimated diabetes risk"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#37474F"},
                   "steps": [{"range": [0, thr], "color": "#C8E6C9"},
                             {"range": [thr, 100], "color": "#FFCDD2"}],
                   "threshold": {"line": {"color": "black", "width": 3}, "value": thr}}))
        gauge.update_layout(height=300, margin=dict(t=60, b=10, l=20, r=20))
        st.plotly_chart(gauge, width="stretch")
        st.caption(f"Referral threshold: {thr:.0f}% or higher (chosen to catch more at-risk people).")
    with c2:
        # Screening result in a coloured box so the full text is always visible
        if res["high_risk"]:
            st.error("**Screening result:** Refer for check-up")
        else:
            st.success("**Screening result:** Lower concern")
        m1, m2 = st.columns(2)
        m1.metric("Risk probability", f"{pct:.1f}%")
        m2.metric("Diabetic rate in segment", f"{res['cluster_diabetic_pct']:.1f}%")
        st.caption(f"This segment holds {res['cluster_size_pct']:.1f}% of patients.")

    # Risk segment box with a fixed dark text colour so it is readable in light and dark mode
    color = SEGMENT_COLORS.get(res["cluster_name"], "#555")
    st.markdown(f"<div style='border-left:6px solid {color};padding:8px 14px;"
                f"background:#f6f6f6;color:#1a1a1a;border-radius:4px'>"
                f"<b>Risk segment: {res['cluster_name']}</b> — {res['cluster_description']}</div>",
                unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.subheader("What drives the model?")
        # Feature importance from the XGBoost model used for the predictions
        fi = pd.DataFrame({
            "Feature": FEATURE_NAMES,
            "Importance": _MODEL.feature_importances_
        })
        fi = fi.sort_values("Importance").tail(10)
        bar = go.Figure(go.Bar(x=fi["Importance"], y=fi["Feature"], orientation="h"))
        bar.update_layout(height=360, margin=dict(t=10, b=10), xaxis_title="Importance (XGBoost)")
        st.plotly_chart(bar, width="stretch")
        st.caption("Global feature importance: shows what the model relies on overall, "
                   "not the cause for this individual.")
    with right:
        st.subheader("AI-generated summary")
        st.info(res["genai_text"])

# ---------------- Tab 2: Scenario Analysis ----------------
def risk_of(patient):
    """Risk (%) from the XGBoost model only, without calling the AI summary."""
    x = pd.DataFrame([patient])[FEATURE_NAMES]
    return float(_MODEL.predict_proba(x)[0, 1]) * 100


with tab_scenario:
    st.subheader("What if the patient changes some risk factors?")
    st.caption("The sidebar values are the current patient. Change the values below "
               "to build a new scenario and compare the two risks.")

    s1, s2, s3 = st.columns(3)
    with s1:
        new_bmi = st.slider("BMI in scenario", 13.0, 52.0, float(bmi), 0.5, key="sc_bmi")
        new_gen = st.select_slider("General health in scenario", options=list(GENHLTH),
                                   value=genhlth, format_func=lambda v: GENHLTH[v], key="sc_gen")
    with s2:
        new_bp = st.checkbox("High blood pressure", value=bool(highbp), key="sc_bp")
        new_chol = st.checkbox("High cholesterol", value=bool(highchol), key="sc_chol")
    with s3:
        new_act = st.checkbox("Physically active", value=bool(physact), key="sc_act")
        new_smoke = st.checkbox("Smoker", value=bool(smoker), key="sc_smoke")

    # Same patient, with only the scenario values changed
    scenario = {**inputs, "BMI": new_bmi, "GenHlth": new_gen, "HighBP": int(new_bp),
                "HighChol": int(new_chol), "PhysActivity": int(new_act), "Smoker": int(new_smoke)}
    current_risk = risk_of(inputs)
    scenario_risk = risk_of(scenario)

    a, b = st.columns(2)
    a.metric("Current risk", f"{current_risk:.1f}%")
    b.metric("Scenario risk", f"{scenario_risk:.1f}%",
             delta=f"{scenario_risk - current_risk:+.1f} points", delta_color="inverse")
       

    st.subheader("Which single change lowers this patient's risk the most?")
    changes = {
        "Lower BMI by 5": {"BMI": max(13.0, bmi - 5)},
        "Control blood pressure": {"HighBP": 0},
        "Control cholesterol": {"HighChol": 0},
        "Become physically active": {"PhysActivity": 1},
        "Quit smoking": {"Smoker": 0},
        "Improve general health by one level": {"GenHlth": max(1, genhlth - 1)},
    }
    rows = []
    for name, change in changes.items():
        changed = {**inputs, **change}
        if changed == inputs:   # this change does not apply to this patient
            continue
        rows.append({"Change": name, "Risk reduction (points)": current_risk - risk_of(changed)})

    if rows:
        impact = pd.DataFrame(rows).sort_values("Risk reduction (points)")
        imp_bar = go.Figure(go.Bar(x=impact["Risk reduction (points)"], y=impact["Change"],
                                   orientation="h"))
        imp_bar.update_layout(height=320, margin=dict(t=10, b=10),
                              xaxis_title="Risk reduction (percentage points)")
        st.plotly_chart(imp_bar, width="stretch")
    else:
        st.info("None of these changes apply to this patient's current values.")
    st.caption("These are model-based estimates for decision support, not proven medical effects.")
# ---------------- Tab 3: Executive Overview ----------------
@st.cache_data
def load_test_results():
    """Predicted risk for every person in the shared test set (computed once, then cached)."""
    test = pd.read_csv(ROOT / "Dataset" / "test_data.csv")
    y_true = test["Diabetes_binary"].astype(int).values
    probs = _MODEL.predict_proba(test[FEATURE_NAMES])[:, 1]
    return y_true, probs


def screening_summary(y_true, probs, threshold):
    """Screening numbers on the test set for one referral threshold (0-1)."""
    referred = probs >= threshold
    tp = int((referred & (y_true == 1)).sum())
    fn = int((~referred & (y_true == 1)).sum())
    fp = int((referred & (y_true == 0)).sum())
    return {
        "recall": tp / (tp + fn) * 100,
        "precision": tp / (tp + fp) * 100 if (tp + fp) else 0.0,
        "referred_pct": referred.mean() * 100,
        "missed": fn,
    }


with tab_exec:
    y_true, probs = load_test_results()
    st.subheader("System performance for decision-makers")
    st.caption(f"Tuned XGBoost model evaluated on the shared test set ({len(y_true):,} people, "
               "not used in training).")

    # The decision-maker can try a different referral threshold
    exec_thr = st.slider("Referral threshold (%)", 10, 90, int(thr), 5, key="exec_thr")
    k = screening_summary(y_true, probs, exec_thr / 100)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("At-risk people detected", f"{k['recall']:.1f}%")
    k2.metric("People referred", f"{k['referred_pct']:.1f}%")
    k3.metric("At-risk people missed", f"{k['missed']:,}")
    k4.metric("Correct referrals", f"{k['precision']:.1f}%")

    # Trade-off curve: catching more at-risk people means referring more people
    grid = [t / 100 for t in range(10, 91, 5)]
    curve = pd.DataFrame([{"Threshold": t * 100, **screening_summary(y_true, probs, t)} for t in grid])
    trade = go.Figure()
    trade.add_trace(go.Scatter(x=curve["Threshold"], y=curve["recall"], mode="lines+markers",
                               name="At-risk people detected (%)"))
    trade.add_trace(go.Scatter(x=curve["Threshold"], y=curve["referred_pct"], mode="lines+markers",
                               name="People referred (%)"))
    trade.add_vline(x=exec_thr, line_dash="dash")
    trade.update_layout(height=360, margin=dict(t=10, b=10), xaxis_title="Referral threshold (%)",
                        yaxis_title="Percent", legend=dict(orientation="h", y=1.1))
    st.plotly_chart(trade, width="stretch")
    st.caption(f"The patient screening tab uses {thr:.0f}%. A lower threshold detects more at-risk "
               "people but sends more people for check-ups, so it should match the available clinical capacity.")
       