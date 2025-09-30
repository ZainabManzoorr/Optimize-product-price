import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split

# -------------------------
# Title & Description
# -------------------------
st.title("📊 Product Price Optimization Dashboard")
st.write("""
Upload your product + competitor dataset and let the ML model 
find the **optimal price** to maximize revenue.
""")

# -------------------------
# Upload Section
# -------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.write(df.head())

    # -------------------------
    # Train XGBoost Demand Model
    # -------------------------
    if "Price" in df.columns and "Demand_Index" in df.columns:
        X = df[["Price"]]
        y = df["Demand_Index"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)
        model.fit(X_train, y_train)

        # -------------------------
        # Price Optimization
        # -------------------------
        price_range = np.linspace(df["Price"].min(), df["Price"].max(), 200)
        demand_pred = model.predict(price_range.reshape(-1, 1))
        revenues = price_range * demand_pred

        optimal_idx = np.argmax(revenues)
        optimal_price = price_range[optimal_idx]
        max_revenue = revenues[optimal_idx]

        # -------------------------
        # Visualization
        # -------------------------
        st.subheader("Revenue Optimization")
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(price_range, revenues, label="Revenue Curve (XGBoost)")
        ax.axvline(optimal_price, color="red", linestyle="--", label=f"Optimal Price = {optimal_price:.2f}")
        ax.set_xlabel("Price")
        ax.set_ylabel("Revenue")
        ax.set_title("Revenue Optimization using XGBoost Demand Model")
        ax.legend()
        st.pyplot(fig)

        # -------------------------
        # Insights
        # -------------------------
        st.subheader("Insights 💡")
        st.success(f"✅ The **optimal price** is **{optimal_price:.2f}**, expected revenue ≈ **{max_revenue:,.2f}**.")
        st.write("""
        - Increasing price beyond this point decreases demand more than it increases revenue.  
        - Lowering price below this point sells more units but sacrifices revenue.  
        - This is your **profit sweet spot**.  
        """)
    else:
        st.error("CSV must have `Price` and `Demand_Index` columns.")
else:
    st.info("👆 Upload a dataset to get started.")
