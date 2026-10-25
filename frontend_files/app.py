import pandas as pd
import requests
import streamlit as st

# the backend container is reachable by its name on the shared Docker network
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecast")
st.write("Predict the total sales of a product in a store.")

# ---- single prediction ----
st.subheader("Single Prediction")
col1, col2 = st.columns(2)
with col1:
    product_id_char = st.selectbox("Product group", ["FD", "NC", "DR"], help="FD = food, NC = non-consumable, DR = drinks")
    product_type_category = st.selectbox("Product type", ["Perishables", "Non Perishables"])
    sugar = st.selectbox("Sugar content", ["Low Sugar", "Regular", "No Sugar"])
    weight = st.number_input("Product weight", min_value=1.0, max_value=30.0, value=12.66, step=0.1)
    mrp = st.number_input("Product MRP (max retail price)", min_value=1.0, max_value=500.0, value=147.0, step=1.0)
with col2:
    area = st.number_input("Allocated display area (share, 0–1)", min_value=0.0, max_value=1.0, value=0.068, step=0.001, format="%.3f")
    store_type = st.selectbox("Store type", ["Supermarket Type2", "Supermarket Type1", "Departmental Store", "Food Mart"])
    store_size = st.selectbox("Store size", ["Medium", "High", "Small"])
    city_type = st.selectbox("City tier", ["Tier 2", "Tier 1", "Tier 3"])
    store_age = st.number_input("Store age (years)", min_value=0, max_value=100, value=16, step=1)

payload = {
    "Product_Weight": weight,
    "Product_Sugar_Content": sugar,
    "Product_Allocated_Area": area,
    "Product_MRP": mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": city_type,
    "Store_Type": store_type,
    "Product_Id_char": product_id_char,
    "Store_Age_Years": store_age,
    "Product_Type_Category": product_type_category,
}

if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
    if response.status_code == 200:
        sales = response.json()["Predicted_Product_Store_Sales_Total"]
        st.success(f"Predicted sales: **{sales:,.2f}**")
    else:
        st.error(f"Error from API: {response.text}")

# ---- batch prediction ----
st.subheader("Batch Prediction")
file = st.file_uploader("Upload a CSV with the 10 input columns", type=["csv"])

if file is not None and st.button("Predict for Batch", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": file.getvalue()})
    if response.status_code == 200:
        batch = pd.read_csv(file)
        preds = response.json()
        batch["Predicted_Sales"] = [preds[str(i)] for i in batch.index]
        st.success("Predictions completed successfully!")
        st.dataframe(batch)
        st.download_button("Download results", batch.to_csv(index=False), "superkart_predictions.csv", "text/csv")
    else:
        st.error(f"Error from API: {response.text}")
