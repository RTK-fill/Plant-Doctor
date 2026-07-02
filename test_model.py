import tensorflow as tf

print("TensorFlow:", tf.__version__)

model = tf.keras.models.load_model(
    "model/plant_doctor_v3.keras",
    compile=False
)

print("SUCCESS!")