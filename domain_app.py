import streamlit as st
from groq import Groq
import whois
from fpdf import FPDF
import io
import time

# --- Config & API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add your GROQ_API_KEY to secrets!")

st.set_page_config(page_title="Domain Sniper V10.0", page_icon="🏹", layout="wide")

# --- Beast UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 10px; border: 1px solid #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- Functions ---
def is_available(domain):
    try:
        w = whois.whois(domain)
        if w.domain_name is None: return True
        return False
    except: return True

def estimate_value(domain):
    name = domain.split('.')[0]
    ext = domain.split('.')[-1]
    length = len(name)
    value = 500 
    if ext == "com": value += 1200
    if ext == "ai": value += 1800
    if length <= 5: value *= 3
    elif length <= 8: value *= 1.5
    return f"${value:,}.0"

def create_pdf(niche, results, style):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(0, 204, 153)
    pdf.cell(0, 20, "PREMIUM DOMAIN RESEARCH REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Target: {niche.upper()}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    clean_results = results.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_results)
    return pdf.output(dest='S').encode('latin-1')

# --- Sidebar Navigation ---
st.sidebar.title("🎯 Sniper Menu")
mode = st.sidebar.radio("Mode:", ["💎 Main Hunter", "🕵️ Expired Hunter"])

if mode == "💎 Main Hunter":
    st.title("🏹 Domain Sniper V9.2")
    col_side, col_main = st.columns([1, 2.5])

    with col_side:
        st.header("🎯 Target")
        niche_input = st.text_input("What is the Niche?", placeholder="e.g. Pet Tech")
        style_input = st.selectbox("Naming Strategy:", ["Modern & Short", "Tech (.ai focus)", "Brandable Abstract"])
        exts_input = st.multiselect("Extensions:", [".com", ".ai", ".io"], default=[".com", ".ai"])
        
        if st.button("🚀 Start Hunting"):
            if niche_input:
                with st.spinner("Analyzing..."):
                    prompt = f"Suggest 10 premium domains for '{niche_input}' in '{style_input}' style. Focus on: {exts_input}."
                    chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                    st.session_state['hunt_res'] = chat.choices[0].message.content

    with col_main:
        if 'hunt_res' in st.session_state:
            st.markdown("### 💎 Findings")
            st.markdown(st.session_state['hunt_res'])
            pdf_bytes = create_pdf(niche_input, st.session_state['hunt_res'], style_input)
            st.download_button("📥 Download Report", pdf_bytes, "Report.pdf", "application/pdf")
            
        st.divider()
        st.markdown("### 🔍 Live Checker & Appraisal")
        check_dom = st.text_input("Paste a domain to verify:")
        if st.button("Check & Estimate Value"):
            if check_dom and "." in check_dom:
                if is_available(check_dom):
                    st.success(f"🔥 {check_dom} is AVAILABLE!")
                    st.metric("Estimated Market Value", estimate_value(check_dom))
                    st.balloons()
                else: st.error("❌ Taken.")

elif mode == "🕵️ Expired Hunter":
    st.title("🕵️ Expired Domain Hunter")
    kw = st.text_input("Search Keyword:")
    if st.button("Scan"):
        for ext in [".com", ".ai"]:
            d = f"{kw}{ext}"
            if is_available(d):
                st.success(f"💎 {d} | Value: {estimate_value(d)}")

st.sidebar.markdown("---")
st.sidebar.write("V10.0 - Clean Stable Version")
