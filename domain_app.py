import streamlit as st
import whois
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io

# --- الإعدادات الأساسية ---
st.set_page_config(page_title="Domain Sniper V10.2", page_icon="🎯", layout="wide")

# --- دالة التقييم (Appraisal Logic) ---
def estimate_value(domain):
    try:
        name_part = domain.split('.')[0]
        tld = domain.split('.')[-1]
        length = len(name_part)
        base_val = 500
        if tld == 'com': base_val += 1500
        if length <= 6: base_val += 1000
        return f"${base_val:,}.0"
    except:
        return "$500.0"

# --- دالة فحص الدومين ---
def check_domain(domain_name):
    try:
        w = whois.whois(domain_name)
        if not w.domain_name:
            return "Available ✅"
        return "Taken 🔒"
    except:
        return "Available ✅"

# --- دالة توليد التقرير PDF ---
def create_pdf(domain, price):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Professional Domain Appraisal Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Domain Name: {domain}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Market Value: {price}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="This domain has high brandability and commercial potential due to its extension and length.")
    return pdf.output(dest='S').encode('latin-1')

# --- المنيو الجانبي ---
st.sidebar.title("🎯 Domain Sniper")
tab = st.sidebar.radio("Navigation:", ["Live Checker & Appraisal", "Expired Hunter"])

# --- 1. التاب القديمة (بكل ميزاتها) ---
if tab == "Live Checker & Appraisal":
    st.title("🔍 Live Checker & Appraisal")
    domain_input = st.text_input("Paste a domain to verify and appraise:", "Vestoza.com")
    
    if st.button("Check & Estimate Value"):
        with st.spinner('Checking...'):
            status = check_domain(domain_input)
            if "Available" in status:
                st.success(f"🔥 {domain_input} is AVAILABLE!")
                val = estimate_value(domain_input)
                
                # عرض الثمن كما في الصورة الأصلية
                st.markdown(f"""
                <div style="border: 2px solid #2e7d32; padding: 20px; border-radius: 10px; background-color: #0e1117;">
                    <p style="margin:0; color:#888;">Estimated Market Value</p>
                    <h1 style="margin:0; color:white;">{val}</h1>
                </div>
                """, unsafe_allow_html=True)
                
                # زر تحميل الـ PDF
                pdf_data = create_pdf(domain_input, val)
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=pdf_data,
                    file_name=f"Report_{domain_input}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"❌ {domain_input} is already taken.")

# --- 2. التاب الجديدة (بدون ما تخرب القديمة) ---
elif tab == "Expired Hunter":
    st.title("🏹 Expired Hunter")
    keyword = st.text_input("Enter keyword to hunt for expired gems:", "vesto")
    
    if st.button("Start Hunting"):
        results = []
        options = [f"{keyword}.com", f"the{keyword}.com", f"{keyword}hub.com", f"get{keyword}.net"]
        for d in options:
            stat = check_domain(d)
            if "Available" in stat:
                results.append({"Domain": d, "Value": estimate_value(d), "Status": stat})
        
        if results:
            st.table(pd.DataFrame(results))
            st.balloons()
        else:
            st.warning("No treasures found. Try another keyword!")
