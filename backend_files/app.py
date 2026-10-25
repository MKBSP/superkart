import joblib
import pandas as pd
from flask import Flask, request, jsonify

# the 10 input columns the model was trained on
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]

# Initialize Flask app
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained pipeline (preprocessing + tuned Random Forest), our own file
model = joblib.load("superkart_model.joblib")


# Health check / home page
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


# Predict sales for one product in one store
@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json()

    # reject requests with missing columns instead of crashing
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    input_data = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = model.predict(input_data).tolist()[0]

    return jsonify({"Predicted_Product_Store_Sales_Total": round(prediction, 2)})


# Predict sales for a CSV file of products
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    file = request.files["file"]
    input_data = pd.read_csv(file)

    missing = [f for f in FEATURES if f not in input_data.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    predictions = model.predict(input_data[FEATURES])

    # {row index: predicted sales}
    return jsonify({str(i): round(float(p), 2) for i, p in zip(input_data.index, predictions)})


# Run locally (in Docker, gunicorn starts the app instead)
if __name__ == "__main__":
    superkart_api.run(debug=True)
