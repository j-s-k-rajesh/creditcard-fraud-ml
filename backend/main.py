from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load model and pipeline ONCE
model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Read CSV
    data = pd.read_csv(file)

    # Save original copy
    original_data = data.copy()

    # Transform
    data_prepared = pipeline.transform(data)

    # Predict
    predictions = model.predict(data_prepared)

    # Add predictions to original data
    original_data["Prediction"] = predictions

    # Convert to JSON
    result = original_data.to_dict(orient="records")

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
