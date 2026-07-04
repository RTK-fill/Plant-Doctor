import os
import json
import numpy as np
import pandas as pd
from PIL import Image

import tensorflow as tf
from tensorflow import keras

# -----------------------------
# SETTINGS
# -----------------------------

IMAGE_SIZE = (160, 160)

MODEL_PATH = "model/best_model.weights.h5"
CLASS_NAMES_PATH = "class_names.json"
TEST_FOLDER = "test_images"

# -----------------------------
# LOAD CLASS NAMES
# -----------------------------

with open(CLASS_NAMES_PATH, "r") as f:
    class_names = json.load(f)

print("\nClasses Loaded:")
for i, name in enumerate(class_names):
    print(f"{i+1}. {name}")

# -----------------------------
print("Loading trained model...")

model = keras.models.load_model(
    "model/final_model.keras"
)

print("Model Loaded Successfully!")
# -----------------------------
# TEST ALL IMAGES
# -----------------------------

results = []

print("=" * 60)
print("STARTING TEST")
print("=" * 60)

for filename in os.listdir(TEST_FOLDER):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(TEST_FOLDER, filename)

    image = Image.open(image_path).convert("RGB")
    image = image.resize(IMAGE_SIZE)

    img_array = np.array(image, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)

    predicted_index = np.argmax(predictions)

    confidence = float(predictions[0][predicted_index]) * 100

    predicted_class = class_names[predicted_index]

    top3 = np.argsort(predictions[0])[-3:][::-1]

    print("\n" + "=" * 60)
    print("Image :", filename)
    print("Prediction :", predicted_class)
    print(f"Confidence : {confidence:.2f}%")

    print("\nTop 3 Predictions:")

    for idx in top3:
        print(
            f"   {class_names[idx]} : {predictions[0][idx]*100:.2f}%"
        )

    results.append({
        "Image": filename,
        "Prediction": predicted_class,
        "Confidence (%)": round(confidence, 2)
    })

# -----------------------------
# SAVE CSV
# -----------------------------

df = pd.DataFrame(results)

df.to_csv("test_results.csv", index=False)

print("\n")
print("=" * 60)
print("TESTING COMPLETE")
print("=" * 60)

print(f"Images Tested : {len(results)}")
print("Results saved as test_results.csv")