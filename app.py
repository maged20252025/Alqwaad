
import streamlit as st
import pandas as pd

st.set_page_config(page_title="القواعد القضائية اليمنية", layout="centered")
st.title("القواعد القضائية اليمنية")

@st.cache_data
def load_data():
    df = pd.read_csv("القواعد_القضائية.csv")
    df.insert(0, "الرقم", range(1, len(df) + 1))
    return df

df = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []

search_query = st.text_input("ابحث في القواعد القضائية:")

if search_query:
    results = df[df["القاعدة القضائية"].str.contains(search_query, case=False, na=False)]
else:
    results = df

def add_to_cart(index):
    row = results.iloc[index]
    if row["الرقم"] not in [item["الرقم"] for item in st.session_state.cart]:
        st.session_state.cart.append({
            "الرقم": row["الرقم"],
            "القاعدة القضائية": row["القاعدة القضائية"],
            "رقم الطعن": row["رقم الطعن"]
        })

st.write(f"عدد النتائج: {len(results)}")

for i, row in results.iterrows():
    with st.container():
        cols = st.columns([1, 8, 1])
        cols[0].markdown(f"**{int(row['الرقم'])}.**")
        cols[1].markdown(row["القاعدة القضائية"])
        with cols[2]:
            st.button("➕", key=f"add_{row['الرقم']}", on_click=add_to_cart, args=(i,))
            st.button("📋", key=f"copy_{row['الرقم']}", on_click=st.session_state.setdefault, args=(f"copied_{row['الرقم']}", True), help="نسخ القاعدة")

st.markdown("---")
st.subheader("السلة")

if st.session_state.cart:
    for item in st.session_state.cart:
        st.markdown(f"**{item['الرقم']}.** {item['القاعدة القضائية']}")

    selected_ids = [str(item["الرقم"]) for item in st.session_state.cart]
    message = "أرغب في الحصول على الأحكام الخاصة بالقواعد التالية: " + "، ".join(selected_ids)
    encoded_message = message.replace(" ", "%20").replace("،", "%2C")
    whatsapp_url = f"https://wa.me/967777533034?text={encoded_message}"

    st.markdown(f"[مراسلتنا للحصول على الأحكام عبر واتساب]({whatsapp_url})", unsafe_allow_html=True)
else:
    st.info("لم تقم بإضافة أي قاعدة إلى السلة بعد.")
