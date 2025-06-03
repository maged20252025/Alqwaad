import streamlit as st import fitz  # PyMuPDF import docx import os import zipfile from tempfile import TemporaryDirectory import re

def extract_legal_issues(text): issues = [] paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 30] for i, para in enumerate(paragraphs): if re.search(r'(طعن|طلب|اعترض|رفض)', para) and "الطاعن" in para: طلب = para رد = "" قاعدة = "" for j in range(i+1, min(i+6, len(paragraphs))): if re.search(r'(قررت|رأت|خلصت|ردت المحكمة|حيث إنه)', paragraphs[j]): رد = paragraphs[j] if re.search(r'(فإن القاعدة|مما سبق|لذلك|فقد استقر)', paragraphs[j]): قاعدة = paragraphs[j] issues.append({"طلب": طلب, "رد": رد, "قاعدة": قاعدة}) return issues if issues else [{"طلب": "لم يتم العثور على طلب واضح.", "رد": "-", "قاعدة": "-"}]

def create_word_file(issues, filename): doc = docx.Document() doc.add_heading('استخراج القواعد القضائية', level=1) for i, item in enumerate(issues, 1): doc.add_paragraph(f"{i}- {item['طلب']}", style='List Number') doc.add_paragraph(f"* رد المحكمة العليا: {item['رد']}") doc.add_paragraph(f"* القاعدة القضائية: {item['قاعدة']}") doc.add_paragraph("---") doc.save(filename)

st.set_page_config(page_title="استخراج القواعد القضائية من ملفات PDF", layout="centered") st.title("📄 استخراج القواعد القضائية من عدة أحكام PDF")

uploaded_files = st.file_uploader("📂 قم برفع ملفات الأحكام بصيغة PDF", type="pdf", accept_multiple_files=True)

if uploaded_files: if st.button("🔍 تحليل الأحكام وإنشاء ملف ZIP"): with TemporaryDirectory() as temp_dir: zip_path = os.path.join(temp_dir, "قواعد_قضائية_لكل_حكم.zip") with zipfile.ZipFile(zip_path, 'w') as zipf: for uploaded_file in uploaded_files: pdf_name = uploaded_file.name.replace('.pdf', '') docx_path = os.path.join(temp_dir, f"{pdf_name}.docx")

# قراءة النص من PDF
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = "\n".join([page.get_text() for page in doc])
                doc.close()

                # استخراج وتحليل الإشكاليات
                issues = extract_legal_issues(full_text)
                create_word_file(issues, docx_path)

                # إضافة إلى الملف المضغوط
                zipf.write(docx_path, arcname=os.path.basename(docx_path))

        with open(zip_path, "rb") as f:
            st.download_button(
                label="📥 تحميل الملف المضغوط للقواعد القضائية",
                data=f,
                file_name="قواعد_قضائية_لكل_حكم.zip",
                mime="application/zip"
            )

