# ============================================================
# Plant Doctor AI 3.0
# Part 1
# TensorFlow 2.21 + Keras 3
# ============================================================

import os
import json
import time
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

DATASET_PATH = "dataset"

MODEL_FOLDER = "model"

MODEL_NAME = "best_model.weights.h5"

MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_NAME)

IMAGE_SIZE = (160, 160)

BATCH_SIZE = 8

INITIAL_EPOCHS = 10

FINE_TUNE_EPOCHS = 15

SEED = 123

# ------------------------------------------------------------
# CREATE MODEL DIRECTORY
# ------------------------------------------------------------

os.makedirs(MODEL_FOLDER, exist_ok=True)

# ------------------------------------------------------------
# START TIMER
# ------------------------------------------------------------

start_time = time.time()

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

print("\nLoading Dataset...\n")
print("Running NEW train_model.py")
print("IMAGE_SIZE =", IMAGE_SIZE)
print("BATCH_SIZE =", BATCH_SIZE)

train_dataset = tf.keras.utils.image_dataset_from_directory(

    DATASET_PATH,

    validation_split=0.20,

    subset="training",

    seed=SEED,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

)

validation_dataset = tf.keras.utils.image_dataset_from_directory(

    DATASET_PATH,

    validation_split=0.20,

    subset="validation",

    seed=SEED,

    image_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

)

class_names = train_dataset.class_names

NUM_CLASSES = len(class_names)

print("\nDetected Classes\n")

for i, c in enumerate(class_names):

    print(f"{i+1}. {c}")

# ------------------------------------------------------------
# SAVE CLASS NAMES
# ------------------------------------------------------------

with open("class_names.json", "w") as f:

    json.dump(class_names, f, indent=4)

print("\nClass names saved.\n")

# ------------------------------------------------------------
# PERFORMANCE
# ------------------------------------------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = (

    train_dataset

    .shuffle(1000)

    .prefetch(AUTOTUNE)

)

validation_dataset = (

    validation_dataset

    .prefetch(AUTOTUNE)

)

# ------------------------------------------------------------
# DATA AUGMENTATION
# ------------------------------------------------------------

data_augmentation = keras.Sequential([

    layers.RandomFlip("horizontal"),

    layers.RandomRotation(0.15),

    layers.RandomZoom(0.20),

    layers.RandomContrast(0.20),

], name="augmentation")

print("\nDataset Ready.\n")
print(f"Training Images : {len(train_dataset) * BATCH_SIZE}")
print(f"Validation Images : {len(validation_dataset) * BATCH_SIZE}")
print(f"Classes : {NUM_CLASSES}")

# ------------------------------------------------------------
# BUILD EFFICIENTNETB0 MODEL
# ------------------------------------------------------------

print("\nBuilding EfficientNetB0...\n")

base_model = tf.keras.applications.EfficientNetB0(

    include_top=False,

    weights="imagenet",

    input_shape=(*IMAGE_SIZE, 3)

)

# Freeze the base model for Stage 1
base_model.trainable = False

# ------------------------------------------------------------
# CREATE MODEL
# ------------------------------------------------------------

inputs = keras.Input(shape=(*IMAGE_SIZE, 3))

# Data Augmentation
x = data_augmentation(inputs)

# Feature extraction
x = base_model(x, training=False)

# Pooling
x = layers.GlobalAveragePooling2D()(x)

# Reduce overfitting
x = layers.Dropout(0.30)(x)

# Small dense layer
x = layers.Dense(
    512,
    activation="relu"
)(x)

x = layers.Dropout(0.20)(x)

# Final prediction layer
outputs = layers.Dense(

    NUM_CLASSES,

    activation="softmax",

    name="predictions"

)(x)

model = keras.Model(

    inputs,

    outputs,

    name="PlantDoctorAI"

)

# ------------------------------------------------------------
# COMPILE MODEL
# ------------------------------------------------------------

model.compile(

    optimizer=keras.optimizers.Adam(

        learning_rate=3e-4

    ),

    loss="sparse_categorical_crossentropy",

    metrics=[

        "accuracy"

    ]

)

print("\nModel Summary\n")

model.summary()
print("\nTrainable Variables:", len(model.trainable_variables))

# ------------------------------------------------------------
# CALLBACKS
# ------------------------------------------------------------

early_stop = EarlyStopping(

    monitor="val_accuracy",

    patience=5,

    restore_best_weights=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.2,

    patience=2,

    min_lr=1e-6,

    verbose=1

)
checkpoint = ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    save_weights_only=True,
    verbose=1
)



callbacks = [

    early_stop,

    reduce_lr,

    checkpoint

]

print("\nModel Ready.\n")

# ------------------------------------------------------------
# STAGE 1 TRAINING
# Train only the classifier head
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 1 : TRAINING CLASSIFIER")
print("=" * 60 + "\n")

history_stage1 = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=INITIAL_EPOCHS,

    callbacks=callbacks,

    verbose=1

)

print("\n")
print("=" * 60)
print("STAGE 1 COMPLETE")
print("=" * 60)
print("\n")

# ------------------------------------------------------------
# SAVE STAGE 1 HISTORY
# ------------------------------------------------------------

history = {}

history["accuracy"] = history_stage1.history["accuracy"]

history["val_accuracy"] = history_stage1.history["val_accuracy"]

history["loss"] = history_stage1.history["loss"]

history["val_loss"] = history_stage1.history["val_loss"]

print("Classifier trained successfully!")

# ------------------------------------------------------------
# LOAD BEST MODEL
# ------------------------------------------------------------

print("\nLoading best model from Stage 1...\n")

model.load_weights(MODEL_PATH)

print("Best model loaded successfully.\n")

# ------------------------------------------------------------
# STAGE 2 - FINE TUNING
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STAGE 2 : FINE TUNING")
print("=" * 60 + "\n")

# Unfreeze the base model
base_model.trainable = True

# Freeze all except last ~30 layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Recompile with a very small learning rate
model.compile(

    optimizer=keras.optimizers.Adam(
        learning_rate=1e-5
    ),

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]

)

history_stage2 = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=FINE_TUNE_EPOCHS,

    callbacks=callbacks,

    verbose=1

)

print("\n")
print("=" * 60)
print("FINE TUNING COMPLETE")
print("=" * 60)

# ------------------------------------------------------------
# MERGE HISTORIES
# ------------------------------------------------------------

history["accuracy"].extend(
    history_stage2.history["accuracy"]
)

history["val_accuracy"].extend(
    history_stage2.history["val_accuracy"]
)

history["loss"].extend(
    history_stage2.history["loss"]
)

history["val_loss"].extend(
    history_stage2.history["val_loss"]
)

# ------------------------------------------------------------
# SAVE TRAINING HISTORY
# ------------------------------------------------------------

with open("training_history.json", "w") as f:
    json.dump(history, f, indent=4)

print("\nTraining history saved.")

# ------------------------------------------------------------
# SAVE FINAL MODEL
# ------------------------------------------------------------

model.save("model/final_model.keras")

print(f"\nModel saved to: {MODEL_PATH}")

# ------------------------------------------------------------
# PLOT ACCURACY
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history["val_accuracy"],
    label="Validation Accuracy"
)

plt.title("Model Accuracy")

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.legend()

plt.grid(True)

plt.savefig("accuracy_plot.png")

plt.close()

# ------------------------------------------------------------
# PLOT LOSS
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    history["loss"],
    label="Training Loss"
)

plt.plot(
    history["val_loss"],
    label="Validation Loss"
)

plt.title("Model Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.legend()

plt.grid(True)

plt.savefig("loss_plot.png")

plt.close()

# ------------------------------------------------------------
# FINAL RESULTS
# ------------------------------------------------------------

best_val_accuracy = max(
    history["val_accuracy"]
)

training_time = (
    time.time() - start_time
)

minutes = int(training_time // 60)

seconds = int(training_time % 60)

print("\n")
print("=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"\nBest Validation Accuracy: "
    f"{best_val_accuracy:.4f}"
)

print(
    f"Training Time: "
    f"{minutes}m {seconds}s"
)

print(
    f"\nClasses Trained: {NUM_CLASSES}"
)

print(
    f"Model Saved: {MODEL_PATH}"
)

print("\nPlant Doctor AI 3.0 Ready! 🌿")