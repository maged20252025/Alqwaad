import streamlit as st
import pandas as pd

st.set_page_config(page_title="القواعد القضائية اليمنية", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_csv("القواعد_القضائية.csv")
    if "الرقم" not in df.columns:
        df.insert(0, "الرقم", range(1, len(df) + 1))
    return df

df = load_data()

st.markdown("<h1 style='text-align: center;'>القواعد القضائية اليمنية</h1>", unsafe_allow_html=True)

# صندوق البحث بمحاذاة اليمين
col1, col2 = st.columns([5, 1])
with col1:
    search = st.text_input("ابحث في القواعد القضائية:", value="", label_visibility="visible")
with col2:
    if st.button("عودة"):
        search = ""

if search:
    filtered_df = df[df["القاعدة القضائية"].str.contains(search, case=False, na=False)]
else:
    filtered_df = df

st.write(f"عدد النتائج: {len(filtered_df)}")

# المفضلة والسلة
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# زر عرض السلة
if st.button("عرض السلة"):
    st.markdown("---")
    st.subheader("السلة")
    for item in st.session_state.favorites:
        st.markdown(f"<div style='direction: rtl; font-size: 18px;'>"
                    f"<b>{item['الرقم']}.</b> {item['القاعدة القضائية']} "
                    f"<br>نوع القضية: <span style='color: green;'>{item['نوع القضية']}</span>"
                    f"</div>", unsafe_allow_html=True)
        if st.button(f"❌ إزالة من السلة - {item['الرقم']}"):
            st.session_state.favorites = [f for f in st.session_state.favorites if f["الرقم"] != item["الرقم"]]
    st.markdown("---")

# عرض القواعد
for _, item in filtered_df.iterrows():
    st.markdown("---")
    st.markdown(f"<div style='direction: rtl; font-size: 18px;'>"
                f"<b>{item['الرقم']}.</b> {item['القاعدة القضائية']} "
                f"<br>نوع القضية: <span style='color: green;'>{item['نوع القضية']}</span>"
                f"</div>", unsafe_allow_html=True)

    if any(f["الرقم"] == item["الرقم"] for f in st.session_state.favorites):
        if st.button(f"❌ إزالة من السلة - {item['الرقم']}"):
            st.session_state.favorites = [f for f in st.session_state.favorites if f["الرقم"] != item["الرقم"]]
    else:
        if st.button(f"➕ إضافة للسلة - {item['الرقم']}"):
            st.session_state.favorites.append(item)

st.markdown("---")