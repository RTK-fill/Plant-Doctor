import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

# --- 1. SAFE IMPORTS & CONFIGURATION ---
st.set_page_config(
    page_title="Plant Doctor AI ",
    page_icon="🌱",
    layout="centered"
)

# Safely import your existing disease info file
try:
    import disease_info
except ImportError:
    st.error("❌ Could not find `disease_info.py` in the current directory. Please make sure it exists alongside app.py.")

# Initialize a clean session history if it doesn't exist yet
if 'history' not in st.session_state:
    st.session_state.history = []


# --- 2. OPTIMIZED MODEL & DATA LOADING ---
@st.cache_resource
def load_prediction_model():
    """Loads the compiled keras model safely and caches it to prevent reloading lag."""
    model_path = os.path.join('model', 'final_model.keras')
    if not os.path.exists(model_path):
        st.error(f"❌ Model file missing at `{model_path}`. Please verify your project folder structure.")
        return None
    return tf.keras.models.load_model(model_path)

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
        st.sidebar.markdown(f"**{idx+1}. {clean_lbl}**")
        st.sidebar.caption(f"Confidence: {log['confidence']} | Status: Checked")
        st.sidebar.write("---")


# --- 4. MAIN APP INTERFACE ---
st.title("🌱 Plant Doctor AI ")
st.markdown("##### *Advanced Agricultural Neural Network Diagnostics Framework*")
st.write("Upload a clear leaf photo or capture one directly using your camera to identify crop pathogens instantly.")

# Dual Input Selector (Highly mobile responsive)
input_mode = st.radio("Select Image Source Input Type:", ("📁 Upload Image File", "📷 Use Live Camera Capture"))

uploaded_file = None
if input_mode == "📁 Upload Image File":
    uploaded_file = st.file_uploader("Select a plant leaf image...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("Center the affected leaf pattern in the camera frame")


# --- 5. PROCESSING & INFERENCE PIPELINE ---
if uploaded_file is not None and model is not None and len(class_names) > 0:
    # Read image
    image = Image.open(uploaded_file)
    st.image(image, caption='Target Sample Image Assets', use_container_width=True)
    
    # Preprocessing to match your exact pipeline rules
    # 160x160 target dimension -> Array transform -> Batch expansion
    img_resized = image.resize((160, 160))
    img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0) 
    
    with st.spinner("Executing neural architecture prediction layers..."):
        # Run inference
        raw_predictions = model.predict(img_array)[0]
        
    # Extract top index elements (Top 3 indices sorted high to low)
    top_3_indices = np.argsort(raw_predictions)[-3:][::-1]
    
    primary_class = class_names[top_3_indices[0]]
    primary_confidence = float(raw_predictions[top_3_indices[0]])
    
    # --- 6. SAFETY GUARDRAIL (Out-of-Distribution Layer) ---
    # Stops non-plant images from forcing a bad 90%+ prediction match
    CONFIDENCE_THRESHOLD = 0.45
    
    if primary_confidence < CONFIDENCE_THRESHOLD:
        st.error("⚠️ **Inconclusive Image Sample Detected**")
        st.warning(
            f"The top match pattern profile only returned a **{primary_confidence*100:.1f}%** confidence value. "
            "The system cannot verify if this image contains a valid target agricultural leaf specimen. "
            "Please upload a clearer, well-lit photograph focusing purely on the leaf structure."
        )
    else:
        # Format names cleanly for the presentation screen
        readable_title = primary_class.replace('___', ' – ').replace('_', ' ')
        st.success(f"### Diagnosis Target: {readable_title}")
        
        # Main Prediction Metric display
        st.write(f"**Primary Target Match Probability:** `{primary_confidence * 100:.2f}%`")
        st.progress(primary_confidence)
        
        # Session State Log Event Append
        current_log = {"disease": primary_class, "confidence": f"{primary_confidence*100:.1f}%"}
        if current_log not in st.session_state.history:
            st.session_state.history.append(current_log)
            
        # Top 3 Alternative Candidates Metrics Block
        with st.expander("📊 View Top 3 Probabilistic Class Distribution Weights"):
            for rank, idx in enumerate(top_3_indices):
                alt_name = class_names[idx].replace('___', ' – ').replace('_', ' ')
                alt_conf = float(raw_predictions[idx])
                st.write(f"**Rank {rank+1}:** {alt_name} (`{alt_conf*100:.2f}%`)")
                st.progress(alt_conf)

        st.write("---")
        
        # --- 7. DYNAMIC TREATMENT MATRIX & DISCOVERY ---
        # Safeguards matching keys against the external disease_info dictionary structure
        # --- 7. DYNAMIC TREATMENT MATRIX & DISCOVERY ---
        # Safeguards matching keys against the external disease_info dictionary structure
        # --- 7. DYNAMIC TREATMENT MATRIX & DISCOVERY ---
        # --- 7. DYNAMIC TREATMENT MATRIX & DISCOVERY ---
        try:
            # Synced with your actual dictionary variable name
            DICTIONARY_NAME = "disease_database"

            if hasattr(disease_info, DICTIONARY_NAME):
                target_dict = getattr(disease_info, DICTIONARY_NAME)

                # SMART LOOKUP: Try the raw name first, then try a cleaned-up version
                raw_key = primary_class
                clean_key = primary_class.replace('___', '_').replace('__', '_')

                data_profile = None
                if raw_key in target_dict:
                    data_profile = target_dict[raw_key]
                elif clean_key in target_dict:
                    data_profile = target_dict[clean_key]

                # If we found a match, display cleanly formatted tabs
                if data_profile is not None:
                    tab1, tab2, tab3 = st.tabs(
                        ["📋 Description & Pathology", "🧪 Biochemical Treatment", "🛡️ Agrosanitary Prevention"])

                    with tab1:
                        st.markdown("### Profile Description")
                        description_text = (
                                data_profile.get('about') or
                                data_profile.get('About') or
                                data_profile.get('description') or
                                data_profile.get('Description') or
                                'Data unavailable.'
                        )
                        st.write(description_text)

                        st.markdown("### Clinical Symptoms")
                        symptoms = data_profile.get('symptoms', 'Data unavailable.')
                        if isinstance(symptoms, list):
                            for symptom in symptoms:
                                st.write(f"• {symptom}")
                        else:
                            st.write(symptoms)

                    with tab2:
                        st.markdown("### Recommended Agricultural Controls")
                        treatment = data_profile.get('treatment', 'Data unavailable.')
                        # Check if treatment data is stored as a list, then loop over it to print bullets
                        if isinstance(treatment, list):
                            for step in treatment:
                                st.write(f"• {step}")
                        else:
                            st.write(treatment)

                    with tab3:
                        st.markdown("### Long-term Crop Field Management")
                        prevention = data_profile.get('prevention', 'Data unavailable.')
                        # Check if prevention data is stored as a list, then loop over it to print bullets
                        if isinstance(prevention, list):
                            for step in prevention:
                                st.write(f"• {step}")
                        else:
                            st.write(prevention)
                else:
                    st.info(
                        f"💡 Model identified pattern metrics, but couldn't find a matching key inside `{DICTIONARY_NAME}`.")
            else:
                st.error(f"❌ Variable `{DICTIONARY_NAME}` not found inside `disease_info.py`.")
        except Exception as e:
            st.error(f"Error reading dataset profiles from external file array: {e}")
            
        # --- 8. PDF/TEXT REPORT DUMP ENGINE ---
        # Instantly creates an offline medical ticket summary asset users can save
        try:
            about_data = disease_info.info_dict.get(primary_class, {}).get('about', 'N/A') if 'disease_info' in locals() else 'N/A'
            tx_data = disease_info.info_dict.get(primary_class, {}).get('treatment', 'N/A') if 'disease_info' in locals() else 'N/A'
            
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
                mime="text/plain"
            )
        except Exception:
            pass