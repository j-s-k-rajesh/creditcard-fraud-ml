from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    data = pd.read_csv(file)

    original_data = data.copy()

    data_prepared = pipeline.transform(data)
    predictions = model.predict(data_prepared)

    original_data["Prediction"] = predictions

    predictions_list = original_data.to_dict(orient="records")

    return jsonify(predictions_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
