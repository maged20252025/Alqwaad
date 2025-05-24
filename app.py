
import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="القواعد القضائية اليمنية", layout="centered")
st.title("القواعد القضائية اليمنية")

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

if search_query:
    results = df[df["القاعدة القضائية"].str.contains(search_query, case=False, na=False)]
else:
    results = df

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

def js_copy(text):
    b64 = base64.b64encode(text.encode()).decode()
    return f'''
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert("تم نسخ القاعدة إلى الحافظة.");
        }}, function(err) {{
            alert("حدث خطأ أثناء النسخ.");
        }});
    }}
    copyToClipboard(atob("{b64}"));
    </script>
    '''

st.markdown(f"**عدد النتائج:** {len(results)}")

for i, row in results.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"**{int(row['الرقم'])}.** {row['القاعدة القضائية']}")
        st.markdown(f"🔹 نوع القضية: `{row['نوع القضية']}`")

        cols = st.columns([1, 1, 6])
        with cols[0]:
            label = "❌ إزالة من السلة" if any(item['الرقم'] == row["الرقم"] for item in st.session_state.cart) else "➕ إضافة للسلة"
            st.button(label, key=f"cart_{row['الرقم']}", on_click=toggle_cart, args=(i,))
        with cols[1]:
            if st.button("📋 نسخ", key=f"copy_{row['الرقم']}"):
                st.components.v1.html(js_copy(row["القاعدة القضائية"]), height=0)

st.markdown("---")
st.subheader("السلة")

if st.session_state.cart:
    for item in st.session_state.cart:
        st.markdown(f"**{item['الرقم']}.** {item['القاعدة القضائية']}\n🔹 نوع القضية: `{item['نوع القضية']}`")

    selected_ids = [str(item["الرقم"]) for item in st.session_state.cart]
    message = "أرغب في الحصول على الأحكام الخاصة بالقواعد التالية: " + "، ".join(selected_ids)
    encoded_message = message.replace(" ", "%20").replace("،", "%2C")
    whatsapp_url = f"https://wa.me/967777533034?text={encoded_message}"

    st.markdown(f"[مراسلتنا للحصول على الأحكام عبر واتساب]({whatsapp_url})", unsafe_allow_html=True)
else:
    st.info("لم تقم بإضافة أي قاعدة إلى السلة بعد.")
