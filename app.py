import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
from disease_info import disease_info

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Plant Doctor AI 3.0",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f4fff4;
}

h1 {
    color: #1b5e20;
}

.stButton>button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "model/plant_doctor_v3.keras",
        compile=False
    )

model = load_model()

# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open("class_names.json", "r") as f:
    class_names = json.load(f)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🌿 Plant Doctor AI")

    st.info("""
Version 3.0

Built using:

• TensorFlow

• MobileNetV2

• Streamlit

• Transfer Learning
""")

    st.success(
        f"Supported Classes: {len(class_names)}"
    )

# ==========================================
# MAIN HEADER
# ==========================================

st.title("🌿 Plant Doctor AI 3.0")

st.write(
    "Upload a plant leaf image and let the AI identify possible diseases."
)

st.divider()

# ==========================================
# IMAGE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)