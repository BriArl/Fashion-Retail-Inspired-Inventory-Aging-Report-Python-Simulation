import pandas as pd
import streamlit as st

st.title("Retail Inventory Aging Report")

uploaded_file = st.file_uploader("Upload Inventory CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['last_movement_date'] = pd.to_datetime(df['last_movement_date'])
    today = pd.Timestamp.today()
    df['days_old'] = (today - df['last_movement_date']).dt.days

