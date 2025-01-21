# Predictive Analysis API

This project provides a Flask-based RESTful API for predictive analysis using a machine learning model. The application accepts manufacturing data, trains a Logistic Regression model, and provides predictions on machine downtime.

---

## Features

1. **Upload and Train Model:**
   - Endpoint: `/upload`
   - Accepts a CSV file containing data with required columns.
   - Trains a Logistic Regression model on the uploaded dataset.
   - Returns model performance metrics such as accuracy and F1-score.

2. **Predict Downtime:**
   - Endpoint: `/predict`
   - Accepts JSON input with `Temperature` and `Run_Time`.
   - Predicts whether a machine will experience downtime (`Yes` or `No`).
   - Provides confidence score for the prediction.

3. **Persistent Model:**
   - Saves the trained model to disk (`model.pkl`) for future predictions.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python Predictive_Analysis.py
   ```

4. **Test the Endpoints:**
   Use Postman, cURL, or any API testing tool.

---

## API Endpoints

### 1. `/upload` (POST)
Uploads a CSV file to train the model.

- **Request:**
  - Content-Type: `multipart/form-data`
  - File: CSV with columns `Machine_ID`, `Temperature`, `Run_Time`, and `Downtime_Flag`.

- **Response:**
  ```json
  {
    "message": "Model trained successfully!",
    "accuracy": 0.95,
    "f1_score": 0.93
  }
  ```

### 2. `/predict` (POST)
Predicts machine downtime based on input data.

- **Request:**
  - Content-Type: `application/json`
  - JSON Body:
    ```json
    {
      "Temperature": 80,
      "Run_Time": 120
    }
    ```

- **Response:**
  ```json
  {
    "Downtime": "Yes",
    "Confidence": 0.85
  }
  ```

---

## Dataset Requirements
The uploaded CSV must contain the following columns:

- `Machine_ID`: Unique identifier for each machine.
- `Temperature`: Operational temperature of the machine.
- `Run_Time`: Cumulative runtime of the machine.
- `Downtime_Flag`: Binary indicator (1 for downtime, 0 otherwise).

---

## Project Structure

```
.
├── Predictive_Analysis.py   # Main application file
├── model.pkl                # Trained model file (generated after training)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Testing the API

### Using cURL

1. **Upload Data:**
   ```bash
   curl -X POST -F "file=@<path_to_csv>" http://127.0.0.1:5000/upload
   ```

2. **Predict Downtime:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"Temperature": 80, "Run_Time": 120}' \
   http://127.0.0.1:5000/predict
   ```

### Using Postman

1. **Upload Data:**
   - Method: POST
   - URL: `http://127.0.0.1:5000/upload`
   - Body: Form-data, key `file`, value as the CSV file.

2. **Predict Downtime:**
   - Method: POST
   - URL: `http://127.0.0.1:5000/predict`
   - Body: Raw JSON:
     ```json
     {
       "Temperature": 80,
       "Run_Time": 120
     }
     ```

---



## Author

Developed by Praveen Shukla.
