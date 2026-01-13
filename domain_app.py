import streamlit as st
from groq import Groq
import whois
import time

# --- ⚙️ الإعدادات ---
# تأكد من وضع الـ API Key الخاص بك في secrets أو استبدله مباشرة هنا
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add your GROQ_API_KEY to secrets!")

st.set_page_config(page_title="Domain Sniper V9.1", page_icon="🏹", layout="wide")

# --- 🎨 الستايل (Beast Mode) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2227; padding: 15px; border-radius: 10px; border: 1px solid #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #00cca3; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ الدوال البرمجية (The Logic) ---

def is_available(domain):
    """التحقق من إتاحة الدومين باستعمال WHOIS"""
    try:
        w = whois.whois(domain)
        # إذا لم يجد اسم الدومين في القاعدة، فهو متاح
        if w.domain_name is None:
            return True
        return False
    except Exception:
        # في حالة الخطأ غالباً يكون الدومين غير مسجل
        return True

def estimate_value(domain):
    """تخمين سعر الدومين بناءً على معايير السوق"""
    name = domain.split('.')[0]
    ext = domain.split('.')[-1]
    length = len(name)
    
    # القيمة الأساسية
    value = 500 
    
    # زيادة القيمة حسب الامتداد
    if ext == "com": value += 1200
    if ext == "ai": value += 1800
    if ext == "io": value += 900
    
    # القوة حسب قصر الاسم
    if length <= 4: value *= 5  # الدومينات الرباعية غالية جداً
    elif length <= 6: value *= 2.5
    elif length <= 8: value *= 1.5
    
    # لمسة الذكاء الاصطناعي في السعر
    if "ai" in name.lower() or "bot" in name.lower():
        value += 500
        
    return f"${value:,}"

# --- 🏗️ الواجهة (User Interface) ---

st.title("🏹 Domain Sniper V9.1")
st.markdown("#### AI Hunter & Price Predictor | 2026 Edition")

with st.sidebar:
    st.header("🦁 Sniper Settings")
    niche = st.text_input("Target Niche:", placeholder="e.g., Renewable Energy")
    style = st.selectbox("Brand Style:", ["Modern & Short", "Tech (.ai focus)", "Dictionary Words", "Two-Word Combo"])
    exts = st.multiselect("Extensions:", [".com", ".ai", ".io", ".net", ".org"], default=[".com", ".ai"])
    
    st.divider()
    st.info("💡 **Tip:** Short .ai domains are flipping for 3x their price in 2026.")

# --- الأزرار والأكشن ---
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 Start Hunting"):
        if niche:
            with st.spinner("The Beast is analyzing market trends..."):
                prompt = f"""
                Act as a professional domain flipper. 
                Suggest 12 premium domain names for the niche '{niche}' using '{style}' style.
                Focus on these extensions: {exts}.
                For each domain:
                - Suggest the name
                - Give a brief 'Why it sells' explanation.
                Format as a clean list.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                st.session_state['hunt_results'] = response.choices[0].message.content
        else:
            st.warning("Please enter a niche first!")

    if 'hunt_results' in st.session_state:
        st.markdown("### 💎 Hunter's Findings")
        st.markdown(st.session_state['hunt_results'])

with col2:
    st.markdown("### 🔍 Live Scanner")
    target_dom = st.text_input("Enter domain to check:", placeholder="beast.com")
    
    if st.button("Check & Appraise"):
        if target_dom and "." in target_dom:
            with st.spinner("Checking WHOIS database..."):
                available = is_available(target_dom)
                
                if available:
                    st.success(f"🔥 {target_dom} is AVAILABLE!")
                    price = estimate_value(target_dom)
                    st.metric(label="Estimated Resale Value 💰", value=price)
                    st.balloons()
                else:
                    st.error(f"❌ {target_dom} is ALREADY TAKEN.")
        else:
            st.error("Please enter a valid domain (e.g., name.com)")

# --- Footer ---
st.divider()
st.caption("Beast Domain Sniper V9.1 - Built for the Domaining Community")
