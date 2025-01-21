from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import pickle
import os

predictive_analysis = Flask(__name__)
model = None
MODEL_PATH = "model.pkl"

def train_model(data):
    global model
    #Splitting data into features and target
    X = data[["Temperature", "Run_Time"]]
    y = data["Downtime_Flag"]
    #Splitting dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Training Logistic Regression model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    #Save the trained model to disk
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return accuracy, f1


@predictive_analysis.route('/upload', methods=['POST'])
def upload_data():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided. Please upload a CSV file."}), 400

    try:
        df = pd.read_csv(file)

        required_columns = {"Machine_ID", "Temperature", "Run_Time", "Downtime_Flag"}
        if not required_columns.issubset(df.columns):
            return jsonify({
                "error": f"Dataset must contain these columns: {', '.join(required_columns)}"
            }), 400

        # Train the model and return metrics
        accuracy, f1 = train_model(df)
        return jsonify({
            "message": "Model trained successfully!",
            "accuracy": round(accuracy, 2),
            "f1_score": round(f1, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@predictive_analysis.route('/predict', methods=['POST'])
def predict():
    global model
    # Load model from disk
    if model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
        else:
            return jsonify({"error": "Model is not trained yet. Please upload data and train the model first."}), 400

    try:
        data = request.json
        temperature = data.get("Temperature")
        run_time = data.get("Run_Time")

        if temperature is None or run_time is None:
            return jsonify({"error": "Both 'Temperature' and 'Run_Time' are required fields."}), 400

        input_data = np.array([[temperature, run_time]])

        prediction = model.predict(input_data)
        confidence = model.predict_proba(input_data).max()

        result = {
            "Downtime": "Yes" if prediction[0] == 1 else "No",
            "Confidence": round(confidence, 2)
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Run application
if __name__ == "__main__":
    predictive_analysis.run(debug=True)

