import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("💡 Power Consumption Prediction")
st.markdown("Enter the environmental conditions and the desired date/time to predict power consumption.")

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Environmental Inputs")
    temperature = st.number_input("Temperature (°C)", value=25.0, format="%.2f")
    wind_speed = st.number_input("Wind Speed (m/s)", value=5.0, format="%.2f")
    gen_diffuse_flows = st.number_input("General Diffuse Flows", value=500.0, format="%.2f")
    diffuse_flows = st.number_input("Diffuse Flows", value=200.0, format="%.2f")

with col2:
    st.subheader("Date & Time Input")
    d = st.date_input("Select a Date")
    t = st.time_input("Select a Time")

# Combine date and time
user_datetime = pd.to_datetime(f"{d} {t}")

# Compute time_fraction: hour + minute/60 + second/3600
time_fraction = user_datetime.hour + user_datetime.minute / 60 + user_datetime.second / 3600

# --- Prediction Logic ---
if st.button("Predict Power Consumption", key='predict_button'):
    # Prepare input DataFrame in the order the model expects
    input_data = pd.DataFrame([[
        temperature,
        wind_speed,
        gen_diffuse_flows,
        diffuse_flows,
        time_fraction
    ]], columns=[
        'Temperature',
        'WindSpeed',
        'GeneralDiffuseFlows',
        'DiffuseFlows',
        'time_fraction'
    ])

    # Make prediction
    prediction = model.predict(input_data)

    st.success(f"Predicted Power Consumption: **{prediction[0]:,.2f}**")
