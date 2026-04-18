import streamlit as st
import pickle
import pandas as pd
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📉",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================
pipeline = pickle.load(open("notebooks/pipeline.pkl", "rb"))
columns = pickle.load(open("model/columns.pkl", "rb"))

threshold = 0.27

# =====================================================
# PREMIUM CSS
# =====================================================
st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */
.stApp {
    background: linear-gradient(135deg,#2563eb,#06b6d4,#14b8a6);
    color: white;
}

/* spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* =====================================================
TEXT
===================================================== */
h1,h2,h3,h4,label,p {
    color:white !important;
}

/* =====================================================
GLASS CARDS
===================================================== */
.card {
    background: rgba(255,255,255,0.10);
    padding: 22px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    margin-bottom: 18px;
}

/* =====================================================
SELECTBOX FIX
===================================================== */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: black !important;
}

/* dropdown menu */
ul {
    background-color: white !important;
    color: black !important;
}

/* =====================================================
INPUT BOX FIX
===================================================== */
input {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}

/* =====================================================
BUTTON
===================================================== */
div.stButton > button {
    width:100%;
    height:52px;
    border:none;
    border-radius:14px;
    font-size:18px;
    font-weight:700;
    color:white;
    background: linear-gradient(90deg,#1d4ed8,#06b6d4);
}

div.stButton > button:hover {
    transform: scale(1.02);
    transition:0.2s;
}

/* =====================================================
METRIC CARDS
===================================================== */
.metric-box {
    background: rgba(255,255,255,0.10);
    padding:18px;
    border-radius:16px;
    text-align:center;
}

/* =====================================================
FOOTER
===================================================== */
.footer {
    text-align:center;
    color:#e0e7ff;
    font-size:15px;
    margin-top:35px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown("<h1 style='text-align:center;'>📉 Customer Churn Prediction System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#dbeafe;'>AI-powered telecom churn risk detection dashboard</p>",
    unsafe_allow_html=True
)

# =====================================================
# INPUT SECTION
# =====================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("👤 Customer Profile & Billing")

c1, c2, c3 = st.columns(3)

with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])

with c2:
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    paperless = st.selectbox("Paperless Billing", ["No", "Yes"])

with c3:
    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )
    monthly = st.number_input("Monthly Charges", min_value=0.0, max_value=150.0, value=70.0)
    phone = st.selectbox("Phone Service", ["No", "Yes"])
    multiple = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# SERVICES
# =====================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌐 Internet Add-on Services")

s1, s2, s3 = st.columns(3)

with s1:
    security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])

with s2:
    protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
    support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])

with s3:
    tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
    movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# CREATE INPUT DATAFRAME
# =====================================================
input_df = pd.DataFrame(np.zeros((1, len(columns))), columns=columns)

input_df["SeniorCitizen"] = 1 if senior == "Yes" else 0
input_df["tenure"] = tenure
input_df["MonthlyCharges"] = monthly
input_df["TotalCharges"] = tenure * monthly
input_df["avg_charge"] = monthly

def activate(col):
    if col in input_df.columns:
        input_df[col] = 1

def pair(yes_col, no_col, value):
    if value == "Yes":
        activate(yes_col)
    else:
        activate(no_col)

pair("gender_Male", "gender_Female", gender)
pair("Partner_Yes", "Partner_No", partner)
pair("Dependents_Yes", "Dependents_No", dependents)
pair("PhoneService_Yes", "PhoneService_No", phone)
pair("PaperlessBilling_Yes", "PaperlessBilling_No", paperless)

activate(f"MultipleLines_{multiple}")
activate(f"InternetService_{internet}")
activate(f"Contract_{contract}")
activate(f"PaymentMethod_{payment}")
activate(f"OnlineSecurity_{security}")
activate(f"OnlineBackup_{backup}")
activate(f"DeviceProtection_{protection}")
activate(f"TechSupport_{support}")
activate(f"StreamingTV_{tv}")
activate(f"StreamingMovies_{movies}")

services = sum(x == "Yes" for x in [security, backup, protection, support, tv, movies])
input_df["total_services"] = services

if tenure <= 12:
    activate("tenure_group_0-1yr")
elif tenure <= 24:
    activate("tenure_group_1-2yr")
elif tenure <= 48:
    activate("tenure_group_2-4yr")
else:
    activate("tenure_group_4-6yr")

# =====================================================
# PREDICT
# =====================================================
if st.button("🔍 Predict Churn Risk"):

    prob = pipeline.predict_proba(input_df)[0][1]

    st.subheader("📊 Prediction Results")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f"<div class='metric-box'><h4>Probability</h4><h2>{prob:.2%}</h2></div>",
            unsafe_allow_html=True
        )

    with m2:
        risk = "High Risk" if prob >= threshold else "Low Risk"
        st.markdown(
            f"<div class='metric-box'><h4>Risk Level</h4><h2>{risk}</h2></div>",
            unsafe_allow_html=True
        )

    with m3:
        status = "Retention Needed" if prob >= threshold else "Stable Customer"
        st.markdown(
            f"<div class='metric-box'><h4>Status</h4><h2>{status}</h2></div>",
            unsafe_allow_html=True
        )

    st.progress(float(prob))

    if prob >= threshold:
        st.error("⚠️ Customer likely to churn. Retention action recommended.")
    else:
        st.success("✅ Customer likely to stay. Relationship appears stable.")

# =====================================================
# FOOTER
# =====================================================
st.markdown(
    "<div class='footer'>Made with Streamlit • Made by Neha Nayak 💜</div>",
    unsafe_allow_html=True
)