import streamlit as st
from groq import Groq
import requests
import whois # للمصداقية العالية في التشييك

# --- ⚙️ الإعدادات (حط الـ API Key ديالك) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Domain Sniper V9.0", page_icon="🏹")

# --- 🎨 تنسيق "الوحش" ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 10px; }
    .success-text { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Domain Sniper V9.0")
st.subheader("Your AI-Powered Domain Flipping Assistant")

# --- 🛠️ وظيفة التشييك الحقيقي (WHOIS) ---
def is_available(domain):
    try:
        w = whois.whois(domain)
        if w.domain_name is None:
            return True
        return False
    except:
        return True # غالباً متاح إذا وقع خطأ في البحث

# --- 🏗️ الواجهة ---
niche = st.text_input("💎 Enter Niche / Keyword:", placeholder="e.g., AI Healthcare, Crypto Hub...")

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Brand Style:", ["Modern & Short", "Tech (.ai focus)", "Dictionary Words", "Premium Brandable"])
with col2:
    extension = st.multiselect("Extensions:", [".com", ".ai", ".io", ".net"], default=[".com", ".ai"])

if st.button("🚀 Hunt Premium Domains"):
    if niche:
        with st.spinner("Analyzing high-value domain patterns..."):
            prompt = f"""
            Act as a professional domain investor (Domainer). 
            Suggest 10 premium, brandable domain names for the niche '{niche}' with a '{style}' style.
            Focus on these extensions: {extension}.
            For each domain:
            1. Suggest the name.
            2. Explain its 'Resale Value' (why a company would buy it for $1000+).
            Keep it professional and concise.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            
            st.session_state['results'] = chat_completion.choices[0].message.content
    else:
        st.warning("Please enter a niche first!")

# --- عرض النتائج والتشييك ---
if 'results' in st.session_state:
    st.markdown("### 💎 Suggested Gems:")
    st.write(st.session_state['results'])
    
    st.divider()
    st.markdown("### 🔍 Live Availability Check")
    check_name = st.text_input("Paste a domain from above to check:")
    if st.button("Check Availability"):
        if is_available(check_name):
            st.success(f"🔥 BOOM! {check_name} looks AVAILABLE! Grab it fast!")
        else:
            st.error(f"❌ Sadly, {check_name} is already taken.")

# --- سكايبار تعليمي ---
st.sidebar.header("🦁 Domaining Secrets")
st.sidebar.markdown("""
- **The 7-Letter Rule:** Try to keep names under 7 letters.
- **Pronunciation:** If you can't say it, don't buy it.
- **Trend:** .ai domains are selling like crazy in 2024-2025.
""")
