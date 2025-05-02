import streamlit as st
from utils.pattern_checker import get_pattern_type
from utils.model_utils import load_model, predict_strength
from utils.demographic_utils import predict_demographic_strength
from utils.mpin_generator import generate_secure_mpin
from utils.lottie_loader import load_lottie_url
import streamlit_lottie as st_lottie

# ------------------ PAGE CONFIG (FIRST LINE) ------------------
st.set_page_config(page_title="MPIN Pattern Checker", layout="wide", initial_sidebar_state="auto")

# ------------------ CSS STYLING ------------------
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #fffaf0;
        color: black;
        font-family: 'Segoe UI', sans-serif;
    }
    ::selection {
        background: #b3d4fc;
        color: black !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #fef3e2 !important;
        color: black !important;
    }
    .stTextInput input, .stDateInput input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 8px;
    }
    label, .stTextInput label, .stDateInput label, .stRadio label, .stMarkdown, .stMetricLabel, .stMetricValue, .stRadio div, .stMetric>div {
        color: black !important;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #0A66C2;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004080;
        color: white;
    }
    .stAlert, .st-success, .stWarning, .stError, .stInfo {
        color: black !important;
    }
    .stAlert {
        background-color: #d9f9c2 !important;
        border-radius: 6px;
    }
    .stMetric {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Load Model ------------------
classifier, regressor, encoder = load_model()

# ------------------ Sidebar ------------------
st.sidebar.title("🧡 OneBanc MPIN Tool")
page = st.sidebar.radio("Choose a Feature", ["Home", "Demographic Checkpoint", "MPIN Recommender"])

# ------------------ HOME PAGE ------------------
if page == "Home":
    st.markdown("## 🔐 MPIN Pattern Strength Checker")
    st.markdown("Check how predictable your MPIN is based on common patterns.")

    lottie_lock = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json")
    st_lottie.st_lottie(lottie_lock, height=200, key="lock")

    user_id = st.text_input("🆔 Unique User ID")
    mpin = st.text_input("🔢 Enter your 4 or 6 digit MPIN", max_chars=6, placeholder="e.g., 2705")

    if st.button("Check MPIN Strength"):
        if not mpin.isdigit() or len(mpin) not in [4, 6]:
            st.error("❌ MPIN must be a 4 or 6-digit number.")
        else:
            pattern_type = get_pattern_type(mpin)
            guessability, label = predict_strength(classifier, regressor, encoder, mpin, pattern_type)

            st.markdown(f"🧠 **Pattern Detected:** `{pattern_type}`")
            st.metric(label="🔍 Guessability %", value=f"{guessability} %")
            st.metric(label="🔐 Strength", value="STRONG" if label == 0 else "WEAK")

            if label == 0:
                st.success("✅ Your MPIN looks strong.")
            else:
                st.warning("⚠️ This MPIN is weak. Try changing it.")

# ------------------ DEMOGRAPHIC CHECKPOINT ------------------
elif page == "Demographic Checkpoint":
    st.markdown("## 📆 Demographic Checkpoint")
    st.markdown("Check if your MPIN is guessable from your personal dates.")

    lottie_calendar = load_lottie_url("https://assets5.lottiefiles.com/private_files/lf30_oqpbtola.json")
    st_lottie.st_lottie(lottie_calendar, height=200, key="calendar")

    mpin = st.text_input("🔑 Enter MPIN", max_chars=6)

    col1, col2 = st.columns(2)
    with col1:
        dob_self = st.date_input("👤 DOB (Self)")
        dob_spouse = st.date_input("💑 DOB (Spouse)")
    with col2:
        dob_pet = st.date_input("🐶 DOB (Pet)")
        anniversary = st.date_input("💍 Anniversary Date")

    if st.button("Check Demographic MPIN Risk"):
        if not mpin.isdigit():
            st.error("❌ MPIN must be numeric.")
        else:
            label = predict_demographic_strength(mpin, dob_self, dob_spouse, dob_pet, anniversary)
            st.metric(label="🔐 Strength", value=label)

            if label == "STRONG":
                st.success("✅ Good! Your MPIN is not linked to personal dates.")
            else:
                st.warning("⚠️ Predictable MPIN. It matches a date you entered.")

# ------------------ MPIN RECOMMENDER ------------------
elif page == "MPIN Recommender":
    st.markdown("## 🤖 MPIN Recommendation System")
    st.markdown("Generate a secure MPIN based on difficulty preference.")

    lottie_bot = load_lottie_url("https://assets7.lottiefiles.com/private_files/lf30_wqypnpu5.json")
    st_lottie.st_lottie(lottie_bot, height=220, key="bot")

    difficulty = st.radio("🧠 Choose Difficulty:", options=["Medium", "Hard"])

    if st.button("🎯 Generate MPIN"):
        avoid_set = set()
        mpin, pattern = generate_secure_mpin(difficulty, classifier, regressor, encoder, avoid_set)

        if mpin:
            st.success(f"✅ MPIN Generated: `{mpin}`")
            st.markdown(f"🧹 **Pattern Type:** `{pattern}`")
        else:
            st.error("⚠️ Failed to generate a strong MPIN. Try again.")