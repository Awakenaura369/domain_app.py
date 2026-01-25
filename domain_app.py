import streamlit as st
from groq import Groq
import whois
from fpdf import FPDF
import io
import time

# --- ⚙️ Config & API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add your GROQ_API_KEY to secrets!")

st.set_page_config(page_title="Domain Sniper V9.2", page_icon="🏹", layout="wide")

# --- 🎨 Beast UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 10px; border: 1px solid #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 8px; }
    .success-text { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ Functions ---
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
    return f"${value:,}"

def create_pdf(niche, results, style):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(0, 204, 153)
    pdf.cell(0, 20, "PREMIUM DOMAIN RESEARCH REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Target Niche: {niche.upper()}", ln=True)
    pdf.cell(0, 10, f"Strategy Style: {style}", ln=True)
    pdf.cell(0, 10, f"Date: {time.strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0, 0, 0)
    clean_results = results.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_results)
    return pdf.output(dest='S').encode('latin-1')

# --- 🏗️ Sidebar Navigation (الحل باش ماترونش الخدمة) ---
st.sidebar.title("🎮 Sniper Menu")
mode = st.sidebar.radio("Choose Mode:", ["💎 Domain Hunter (Original)", "🕵️ Expired Hunter"])

if mode == "💎 Domain Hunter (Original)":
    # هاد الجزء هو الكود ديالك الأصلي بالحرف، ما مقيوس فيه والو
    st.title("🏹 Domain Sniper V9.2")
    st.caption("AI-Powered Domain Hunting & Reporting Tool for Fiverr Sellers")

    col_side, col_main = st.columns([1, 2.5])

    with col_side:
        st.header("🎯 Target")
        niche_input = st.text_input("What is the Niche?", placeholder="e.g. Pet Tech")
        style_input = st.selectbox("Naming Strategy:", ["Modern & Short", "Tech (.ai focus)", "Brandable Abstract", "Two-Word Premium"])
        exts_input = st.multiselect("Extensions:", [".com", ".ai", ".io", ".net"], default=[".com", ".ai"])
        
        if st.button("🚀 Start Hunting"):
            if niche_input:
                with st.spinner("Analyzing market data..."):
                    prompt = f"Act as a professional domain flipper. Suggest 10 premium domain names for the niche '{niche_input}' with a '{style_input}' style. Focus on: {exts_input}. For each domain: 1. Name 2. Appraisal Value 3. Business Potential."
                    chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                    st.session_state['hunt_res'] = chat.choices[0].message.content
            else: st.warning("Please enter a niche!")

    with col_main:
        if 'hunt_res' in st.session_state:
            st.markdown("### 💎 Hunter's Findings")
            st.markdown(st.session_state['hunt_res'])
            pdf_bytes = create_pdf(niche_input, st.session_state['hunt_res'], style_input)
            st.download_button(label="📥 Download Professional PDF Report", data=pdf_bytes, file_name=f"Domain_Report_{niche_input}.pdf", mime="application/pdf")
            
        st.divider()
        st.markdown("### 🔍 Live Checker & Appraisal")
        check_dom = st.text_input("Paste a domain to verify and appraise:")
        if st.button("Check & Estimate Value"):
            if check_dom and "." in check_dom:
                if is_available(check_dom):
                    st.success(f"🔥 {check_dom} is AVAILABLE!")
                    st.metric("Estimated Market Value", estimate_value(check_dom))
                    st.balloons()
                else: st.error(f"❌ {check_dom} is already registered.")

elif mode == "🕵️ Expired Hunter":
    st.title("🕵️ Expired Domain Hunter")
    # ميزة البحث الجماعي اللي طلبنا (معزولة تماما باش ما تخربقش الفوقاني)
    exp_key = st.text_input("Enter Keyword to Hunt:")
    if st.button("Hunt Treasures"):
        options = [f"{exp_key}.com", f"the{exp_key}.com", f"{exp_key}tech.com"]
        for o in options:
            if is_available(o):
                st.success(f"💎 {o} is AVAILABLE! | Est. Value: {estimate_value(o)}")

# --- Sidebar Info ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🦁 How to Sell on Fiverr")
st.sidebar.write("1. Take an order. | 2. Run Sniper. | 3. Download PDF.")

