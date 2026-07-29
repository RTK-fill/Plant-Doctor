import streamlit as st
import tensorflow as tf
import keras  # Native Keras 3 engine
import numpy as np
from PIL import Image
import json
import os
import sys
import importlib

# --- 1. SAFE IMPORTS & CSS CONFIGURATION ---
st.set_page_config(
    page_title="Plant Doctor AI",
    page_icon="🌱",
    layout="wide", # Upgraded to wide mode for side-by-side columns
    initial_sidebar_state="expanded"
)

# Inject Custom CSS to hide Streamlit default branding and margins
# --- 1. SAFE IMPORTS & CLEAN MINIMALIST CSS ---
# --- 1. SAFE IMPORTS & CLEAN MINIMALIST CSS ---
custom_css = """
<style>
    /* Hide Streamlit Hamburger Menu and Footer, but keep the Header for the sidebar arrow! */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}

    /* Clean subtle card look for containers */
    div.st-key-metric-card {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
    }

    /* Soft, elegant accent colors for the metric */
    [data-testid="stMetricValue"] {
        color: #4ade80 !important; /* Soft modern mint green */
        font-weight: 700 !important;
    }

    /* Modern clean button styling */
    .stButton button, .stDownloadButton button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Safely import and force-reload disease info so descriptions always update
try:
    import disease_info

    importlib.reload(disease_info)
except ImportError:
    st.error("❌ Could not find `disease_info.py` in the current directory.")

# Initialize a clean session history if it doesn't exist yet
if 'history' not in st.session_state:
    st.session_state.history = []


# --- 2. OPTIMIZED MODEL & DATA LOADING ---
@st.cache_resource
def load_prediction_model():
    """Loads the compiled keras model safely using the modern Keras 3 engine."""
    model_path = os.path.join('model', 'final_model.keras')
    if not os.path.exists(model_path):
        st.error(f"❌ Model file missing at `{model_path}`.")
        return None
    try:
        return keras.models.load_model(model_path, compile=False)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None


@st.cache_data
def load_class_labels():
    """Loads the JSON mappings for the 15 trained classes."""
    label_path = 'class_names.json'
    if not os.path.exists(label_path):
        st.error(f"❌ Class mappings file missing at `{label_path}`.")
        return []
    with open(label_path, 'r') as f:
        return json.load(f)


# Load data assets
model = load_prediction_model()
class_names = load_class_labels()

# --- 3. UI SIDEBAR (SESSION HISTORY) ---
st.sidebar.header("📜 Session Diagnostics")
if not st.session_state.history:
    st.sidebar.info("No scans performed yet in this active session.")
else:
    for idx, log in enumerate(reversed(st.session_state.history)):
        clean_lbl = log['disease'].replace('___', ' ').replace('_', ' ')
        st.sidebar.markdown(f"**{idx + 1}. {clean_lbl}**")
        st.sidebar.caption(f"Confidence: {log['confidence']}")
        st.sidebar.write("---")

# Tucked Developer Mode
with st.sidebar.expander("🛠️ System Admin / Developer"):
    DEVELOPER_PASSWORD = "PD4_ADMIN_2026"
    developer_mode = False
    password = st.text_input("Admin Password", type="password", placeholder="🔒", label_visibility="collapsed")
    if password == DEVELOPER_PASSWORD:
        developer_mode = True
        st.success("Developer Mode Enabled")
        manual_prediction = st.selectbox("Manual Prediction", class_names)
        manual_confidence = st.slider("Confidence", 0, 100, 98)

# --- 4. MAIN APP INTERFACE ---

# Clean, full-width high-impact header (No extra buttons)
st.markdown("""
    <div style="margin-top: 0px; margin-bottom: 20px;">
        <h1 style="font-size: 3rem; font-weight: 800; letter-spacing: -0.05em; margin-bottom: 0px; line-height: 1.1;">
            🌱 Plant Doctor AI
        </h1>
        <p style="font-size: 1.15rem; opacity: 0.7; font-weight: 400; margin-top: 5px;">
            Advanced Agricultural Neural Network Diagnostics Framework
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# State management for sample gallery
if "selected_sample" not in st.session_state:
    st.session_state.selected_sample = None

# Horizontal toggle updated with a 3rd option
input_mode = st.radio("📸 **Select Image Source:**",
                      ("📁 Upload Image File", "📷 Use Live Camera Capture", "🌿 Try a Sample Leaf"),
                      horizontal=True)

uploaded_file = None

if input_mode == "📁 Upload Image File":
    st.session_state.selected_sample = None  # Reset sample state
    uploaded_file = st.file_uploader("Select a plant leaf image...", type=["jpg", "jpeg", "png"],
                                     label_visibility="collapsed")

elif input_mode == "📷 Use Live Camera Capture":
    st.session_state.selected_sample = None  # Reset sample state
    uploaded_file = st.camera_input("Center the affected leaf pattern in the camera frame",
                                    label_visibility="collapsed")

elif input_mode == "🌿 Try a Sample Leaf":
    st.markdown("##### 🧪 Select a sample to test the AI:")

    # Check if the samples folder exists to prevent crashing
    if not os.path.exists("samples"):
        st.warning("⚠️ The `samples` folder is missing. Please create a folder named 'samples' and add images to it.")
    else:
        # Create a beautiful 3-column layout for the gallery
        samp_col1, samp_col2, samp_col3 = st.columns(3)

        with samp_col1:
            if os.path.exists("samples/sample1.jpg"):
                st.image("samples/sample1.jpg", use_container_width=True)
                if st.button("Test Sample 1", use_container_width=True):
                    st.session_state.selected_sample = "samples/sample1.jpg"

        with samp_col2:
            if os.path.exists("samples/sample2.jpg"):
                st.image("samples/sample2.jpg", use_container_width=True)
                if st.button("Test Sample 2", use_container_width=True):
                    st.session_state.selected_sample = "samples/sample2.jpg"

        with samp_col3:
            if os.path.exists("samples/sample3.jpg"):
                st.image("samples/sample3.jpg", use_container_width=True)
                if st.button("Test Sample 3", use_container_width=True):
                    st.session_state.selected_sample = "samples/sample3.jpg"

    # Feed the selected sample into the prediction pipeline
    if st.session_state.selected_sample:
        uploaded_file = st.session_state.selected_sample
# --- 5. PROCESSING & INFERENCE PIPELINE ---
if uploaded_file is not None and model is not None and len(class_names) > 0:
    image = Image.open(uploaded_file)

    # Preprocessing
    img_resized = image.resize((160, 160))
    img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)

    with st.spinner("Executing neural architecture prediction layers..."):
        raw_predictions = model.predict(img_array)[0]

    top_3_indices = np.argsort(raw_predictions)[-3:][::-1]
    primary_class = class_names[top_3_indices[0]]
    primary_confidence = float(raw_predictions[top_3_indices[0]])

    # Developer Override
    if developer_mode:
        primary_class = manual_prediction
        primary_confidence = manual_confidence / 100.0
        top_3_indices = [class_names.index(primary_class)]
        raw_predictions = np.zeros(len(class_names))
        raw_predictions[class_names.index(primary_class)] = primary_confidence

    # --- 6. SAFETY GUARDRAIL ---
    CONFIDENCE_THRESHOLD = 0.45

    if primary_confidence < CONFIDENCE_THRESHOLD:
        st.error("⚠️ **Inconclusive Image Sample Detected**")
        st.warning(
            f"The top match pattern profile only returned a **{primary_confidence * 100:.1f}%** confidence value. Please upload a clearer, well-lit photograph focusing purely on the leaf structure.")
        st.image(image, use_container_width=True)
    else:
        # --- 7. SIDE-BY-SIDE LAYOUT DASHBOARD ---
        col1, col2 = st.columns([1, 1.5], gap="large")

        with col1:
            st.image(image, caption='Target Sample', use_container_width=True)

            # Sleek KPI Metric display
            st.metric(label="🔬 Primary Model Confidence", value=f"{primary_confidence * 100:.2f}%")

            # --- INTERACTIVE PROBABILITY CHART ---
            with st.expander("📊 View Probability Distribution", expanded=True):
                st.caption("Top matching disease candidate likelihoods:")

                # Build a dictionary or data structure for Streamlit's bar chart
                # We'll take the top 5 predictions to make the chart look robust
                top_5_indices = np.argsort(raw_predictions)[-5:][::-1]

                chart_data = {}
                for idx in top_5_indices:
                    # Clean up class name for readable chart labels
                    label = class_names[idx].replace('___', ' ').replace('_', ' ')
                    # Shorten extra long names if needed
                    if len(label) > 25:
                        label = label[:22] + "..."
                    score = float(raw_predictions[idx])
                    chart_data[label] = score

                # Render native interactive Streamlit bar chart
                st.bar_chart(chart_data, color="#4ade80")

            # Session Logging
            current_log = {"disease": primary_class, "confidence": f"{primary_confidence * 100:.1f}%"}
            if current_log not in st.session_state.history:
                st.session_state.history.append(current_log)
        with col2:
            readable_title = primary_class.replace('___', ' – ').replace('_', ' ')
            st.success(f"### Diagnosis Target: {readable_title}")

            try:
                if hasattr(disease_info, "disease_database"):
                    db = disease_info.disease_database
                    target_data = db.get(primary_class,
                                         db.get(primary_class.replace('___', '_').replace('__', '_'), {}))

                    if target_data:
                        tab1, tab2, tab3 = st.tabs(["📋 Pathology", "🧪 Treatment", "🛡️ Prevention"])

                        with tab1:
                            st.write(target_data.get('about', 'Data unavailable.'))
                            st.markdown("#### Clinical Symptoms")
                            symp = target_data.get('symptoms', 'Data unavailable.')
                            if isinstance(symp, list):
                                for s in symp: st.markdown(f"- {s}")
                            else:
                                st.write(symp)

                        with tab2:
                            tx = target_data.get('treatment', 'Data unavailable.')
                            if isinstance(tx, list):
                                for t in tx: st.markdown(f"- {t}")
                            else:
                                st.write(tx)

                        with tab3:
                            prev = target_data.get('prevention', 'Data unavailable.')
                            if isinstance(prev, list):
                                for p in prev: st.markdown(f"- {p}")
                            else:
                                st.write(prev)
                    else:
                        st.info(
                            "💡 Model identified pattern metrics, but couldn't find a matching key inside the database.")
            except Exception as e:
                st.error(f"Error reading dataset profiles: {e}")

            st.write("---")

            # --- 8. REPORT DUMP ENGINE ---
            try:
                if hasattr(disease_info, 'disease_database'):
                    db = disease_info.disease_database
                    target_data = db.get(primary_class,
                                         db.get(primary_class.replace('___', '_').replace('__', '_'), {}))
                    about_data = target_data.get('about', 'Data unavailable.')
                    tx_raw = target_data.get('treatment', 'Data unavailable.')
                    tx_data = "\n".join([f"• {item}" for item in tx_raw]) if isinstance(tx_raw, list) else tx_raw
                else:
                    about_data, tx_data = 'N/A', 'N/A'

                report_body = (
                    f"PLANT DOCTOR AI DIAGNOSTIC EXAM SUMMARY\n"
                    f"============================================\n"
                    f"Target Identification Class : {primary_class}\n"
                    f"Model Verification Weight   : {primary_confidence * 100:.2f}%\n\n"
                    f"PATHOLOGY OVERVIEW:\n{about_data}\n\n"
                    f"TREATMENT INSTRUCTIONS:\n{tx_data}\n"
                )

                st.download_button(
                    label="📥 Export Digital Treatment Record (TXT)",
                    data=report_body,
                    file_name=f"PlantDoctor_Diagnosis_{primary_class}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating download report: {e}")