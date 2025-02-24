from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from flask_cors import CORS
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "model", "Crop_recommendation.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "DecisionTree_Crop_Predictor.pkl")

# Load dataset and train the model if not already saved
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Dataset not found at: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)
features = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
target = df['label'].astype('category')
target_encoded = target.cat.codes
category_mapping = dict(enumerate(target.cat.categories))

if not os.path.exists(MODEL_PATH):
    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(features, target_encoded, test_size=0.2, random_state=2)
    model = DecisionTreeClassifier(random_state=2)
    model.fit(X_train, y_train)
    with open(MODEL_PATH, 'wb') as file:
        pickle.dump(model, file)
    print("Model saved!")

# Load trained model
with open(MODEL_PATH, 'rb') as file:
    loaded_model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        required_keys = {'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'}
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required fields'}), 400

        values = np.array([[data['N'], data['P'], data['K'], data['temperature'],
                            data['humidity'], data['ph'], data['rainfall']]])

        prediction = loaded_model.predict(values)
        crop_name = category_mapping.get(prediction[0], "Unknown Crop")

        return jsonify({'crop': crop_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
