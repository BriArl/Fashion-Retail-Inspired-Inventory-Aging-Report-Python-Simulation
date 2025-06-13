import pandas as pd
import streamlit as st
from utils import load_css
load_css("styles.css")


with open("sample_inventory.csv", "rb") as f:
        st.download_button(
            label ="Download Sample Inventory CSV",
            data=f,
            file_name = "sample_inventory.csv",
            mime="text/csv"
        )

uploaded_file = st.file_uploader("Upload Inventory CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['last_movement_date'] = pd.to_datetime(df['last_movement_date'])
    today = pd.Timestamp.today()
    df['days_old'] = (today - df['last_movement_date']).dt.days

    def get_buckets(days):
        if days <= 30:
            return "0-30 days"
        elif days <= 60:
            return "31-60 days"
        elif days <= 90:
            return "61-90 days"
        else:
            return ">90 days"

    df['aging_bucket'] = df['days_old'].apply(get_buckets)

    st.success("Report Generated")

    st.subheader("Inventory Aging Summary")
    st.dataframe(df[['material', 'description', 'category', 'store', 'quantity', 'days_old', 'aging_bucket']])

    csv = df.to_csv(index=False).encode()
    st.download_button("Download", data=csv, file_name="aging_report.csv", mime='text/csv')