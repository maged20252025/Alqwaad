
import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="القواعد القضائية اليمنية", layout="centered")
st.markdown('<h1 style="text-align: right;">القواعد القضائية اليمنية</h1>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("القواعد_القضائية.csv")
    if "الرقم" not in df.columns:
        df.insert(0, "الرقم", range(1, len(df) + 1))
    if "نوع القضية" not in df.columns:
        df["نوع القضية"] = "غير محدد"
    return df

df = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []

search_query = st.text_input("ابحث في القواعد القضائية:")

if search_query.strip() == "":
    results = df
else:
    results = df[df["القاعدة القضائية"].str.contains(search_query, case=False, na=False)]

def toggle_cart(index):
    row = results.iloc[index]
    existing = next((item for item in st.session_state.cart if item["الرقم"] == row["الرقم"]), None)
    if existing:
        st.session_state.cart.remove(existing)
    else:
        st.session_state.cart.append({
            "الرقم": row["الرقم"],
            "القاعدة القضائية": row["القاعدة القضائية"],
            "رقم الطعن": row["رقم الطعن"],
            "نوع القضية": row["نوع القضية"]
        })

st.markdown(f"<div style='text-align:right;'>عدد النتائج: {len(results)}</div>", unsafe_allow_html=True)

for i, row in results.iterrows():
    with st.container():
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right;'><b>{int(row['الرقم'])}.</b> {row['القاعدة القضائية']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right;'>🔹 نوع القضية: <span style='color:green;'>{row['نوع القضية']}</span></div>", unsafe_allow_html=True)

        cols = st.columns([1, 1, 5])
        with cols[0]:
            label = "❌ إزالة من السلة" if any(item['الرقم'] == row["الرقم"] for item in st.session_state.cart) else "➕ إضافة للسلة"
            st.button(label, key=f"cart_{row['الرقم']}", on_click=toggle_cart, args=(i,))
        with cols[1]:
            st.text_input("انسخ يدويًا:", value=row["القاعدة القضائية"], key=f"copy_text_{row['الرقم']}", label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:right;'>السلة</h3>", unsafe_allow_html=True)

if st.session_state.cart:
    for item in st.session_state.cart:
        st.markdown(f"<div style='text-align:right;'><b>{item['الرقم']}.</b> {item['القاعدة القضائية']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right;'>🔹 نوع القضية: <span style='color:green;'>{item['نوع القضية']}</span></div>", unsafe_allow_html=True)
        st.button(f"❌ إزالة من السلة", key=f"remove_{item['الرقم']}", on_click=lambda i=item['الرقم']: st.session_state.cart.__delitem__(
            next(index for index, val in enumerate(st.session_state.cart) if val['الرقم'] == i)
        ))

    selected_ids = [str(item["الرقم"]) for item in st.session_state.cart]
    message = "أرغب في الحصول على الأحكام الخاصة بالقواعد التالية: " + "، ".join(selected_ids)
    encoded_message = message.replace(" ", "%20").replace("،", "%2C")
    whatsapp_url = f"https://wa.me/967777533034?text={encoded_message}"
    st.markdown(f"<div style='text-align:right;'><a href='{whatsapp_url}' target='_blank'>📩 مراسلتنا عبر واتساب</a></div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:right;color:gray;'>لم تقم بإضافة أي قاعدة إلى السلة بعد.</div>", unsafe_allow_html=True)
