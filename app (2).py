
import streamlit as st
import pandas as pd

st.set_page_config(page_title="القواعد القضائية اليمنية", layout="centered")

st.title("القواعد القضائية اليمنية")

@st.cache_data
def load_data():
    return pd.read_csv("القواعد_القضائية.csv")

df = load_data()

search_query = st.text_input("ابحث في القواعد القضائية:")

if search_query:
    results = df[df["القاعدة القضائية"].str.contains(search_query, case=False, na=False)]
else:
    results = df

st.write(f"عدد النتائج: {len(results)}")
st.table(results)
