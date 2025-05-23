import os
import fitz  # PyMuPDF
import re
import csv

input_folder = "judgments"
output_folder = "output"
output_file = os.path.join(output_folder, "rules_output.csv")

os.makedirs(output_folder, exist_ok=True)

def extract_appeal_number(text):
    match = re.search(r'رقم الطعن\s*[:\-]?\s*(\d+)', text)
    return match.group(1) if match else "غير محدد"

def extract_legal_rules(text):
    rules = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if (
            15 < len(line) < 300
            and not line.startswith("رقم الطعن")
            and not line.startswith("باسم الشعب")
            and not line.startswith("محكمة")
            and not line.startswith("صدر")
        ):
            if re.search(r'\b(قاعدة|يجوز|لا يجوز|يعد|تعد|يعتبر|تعتبر|إذا|متى|يحق)\b', line):
                rules.append(line)
    return rules

with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["رقم الطعن", "القاعدة القضائية"])

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(input_folder, filename)
            with fitz.open(filepath) as doc:
                full_text = ""
                for page in doc:
                    full_text += page.get_text()
                appeal_number = extract_appeal_number(full_text)
                rules = extract_legal_rules(full_text)
                for rule in rules:
                    writer.writerow([appeal_number, rule])

print(f"تم استخراج القواعد القضائية وحفظها في: {output_file}")
