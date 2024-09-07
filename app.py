# app.py
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
import requests

app = Flask(__name__)

# Load your trained model
MODEL_PATH = 'skin_disease_model.h5'  # Ensure this file is uploaded to the repo
model = tf.keras.models.load_model(MODEL_PATH)

# Example class names (update with actual)
class_names = [
    'BA: Cellulitis', 'BA: Impetigo', 'FU: Athlete Foot', 'FU: Nail Fungus',
    'FU: Ringworm', 'PA: Cutaneous Larva Migrans', 'VI: Chickenpox', 'VI: Shingles',
    'IN: Acne', 'IN: Atopic Dermatitis', 'IN: Eczema', 'IN: Psoriasis', 'UN: Unable to identify'
]

@app.route('/predict', methods=['POST'])
def predict():
    # Process the uploaded image
    file = request.files['image']
    img = Image.open(file.stream).convert("RGB")
    img = img.resize((150, 150))  # Adjust size according to model input

    # Prepare image for prediction
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions)
    confidence = np.max(predictions)

    # Integrate Gemini API (Example)
    gemini_data = {
        "query": class_names[class_idx],
        "confidence": float(confidence)
    }
    try:
        gemini_response = requests.post('https://api.gemini.com/v1/public', json=gemini_data)
        gemini_info = gemini_response.json()
    except Exception as e:
        gemini_info = {"error": str(e)}

    # Return combined prediction and Gemini API data
    result = {
        'predicted_class': class_names[class_idx],
        'confidence': float(confidence),
        'gemini_info': gemini_info
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
