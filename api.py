from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])  # Allow requests from frontend

# Load models (you can also lazy load them per request if needed)
models = {
    "brain-tumor": tf.keras.models.load_model("C:/Users/admin/Desktop/Radiographic Image Analyzer/brain_mri-scan.h5"),
    "bone-fracture": tf.keras.models.load_model("C:/Users/admin/Desktop/Radiographic Image Analyzer/bone_x-ray.h5"),
    "pneumonia": tf.keras.models.load_model("C:/Users/admin/Desktop/Radiographic Image Analyzer/chest_x-ray.h5"),
}

def preprocess_image(image_bytes, target_size=(224, 224)):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # normalize
    return np.expand_dims(image_array, axis=0)  # add batch dimension


@app.route("/predict/<condition>", methods=["POST"])
def predict(condition):
    if condition not in models:
        return jsonify({"error": "Invalid condition"}), 400

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_input = preprocess_image(image_file.read())


    model = models[condition]
    prediction = model.predict(image_input)[0]

    confidence = float(np.max(prediction)) * 100
    label_index = int(np.argmax(prediction))

    if(condition == "brain-tumor"):
        labels = ['Healthy Brain', 'Tumor Brain']  # Change as per your model
    elif(condition == "bone-fracture"):
        labels = ['Healthy Bone', 'Fractured Bone']
    else:
        labels = ['Healthy Chest', 'Pneumonia Infection']

    return jsonify({
        "result": labels[label_index],
        "confidence": f"{confidence:.2f}%"
    })

if __name__ == "__main__":
    app.run(debug=True)
