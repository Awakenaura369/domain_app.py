import streamlit as st
import whois
import pandas as pd
from datetime import datetime

# إعدادات واجهة المستخدم
st.set_page_config(page_title="Domain Hunter Pro", page_icon="🏹", layout="wide")

# دالة التقييم (اللي فالتصويرة ديالك)
def estimate_value(domain):
    try:
        name_part = domain.split('.')[0]
        tld = domain.split('.')[-1]
        length = len(name_part)
        
        # منطق تقدير الثمن
        base_val = 500
        if tld == 'com': base_val += 1500
        if tld in ['io', 'ai']: base_val += 800
        if length <= 6: base_val += 1000
        if '-' not in name_part: base_val += 200
        
        return f"${base_val:,}.0"
    except:
        return "$0.0"

# دالة الفحص باستعمال مكتبة python-whois
def check_domain(domain_name):
    try:
        w = whois.whois(domain_name)
        # إذا لم يجد معلومات، يعني الدومين متاح
        if not w.domain_name:
            return "Available ✅"
        return "Taken 🔒"
    except:
        # غالبا المكتبة كتعطي Error إلا كان متاح تماما
        return "Available ✅"

# القائمة الجانبية
st.sidebar.title("🎯 Domain Sniper")
menu = ["Live Checker", "Expired Hunter"]
choice = st.sidebar.selectbox("ختار التاب:", menu)

# --- TAB 1: Live Checker ---
if choice == "Live Checker":
    st.title("🔍 Live Checker & Appraisal")
    st.write("تشيك واش الدومين متاح وشحال كيسوا فالسوق")
    
    target = st.text_input("دخل الدومين هنا:", "Vestoza.com")
    
    if st.button("Check & Estimate"):
        with st.spinner('جاري الفحص...'):
            status = check_domain(target)
            if "Available" in status:
                st.success(f"🔥 {target} is AVAILABLE!")
                val = estimate_value(target)
                st.metric(label="Estimated Market Value", value=val)
            else:
                st.error(f"❌ {target} is already taken.")

# --- TAB 2: Expired Hunter ---
elif choice == "Expired Hunter":
    st.title("🏹 Expired Hunter (The Treasure Finder)")
    st.info("هنا كدخل الكلمة المفتاحية وحنا كنقلبو ليك على احتمالات اللي يقدروا يكونوا طاحوا (Expired)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        keyword = st.text_input("دخل الكلمة (مثلا: shop, tech, bio):", "crypto")
    with col2:
        exts = st.multiselect("الامتدادات:", [".com", ".net", ".io", ".org"], default=[".com", ".net"])
    
    if st.button("Start Hunting"):
        # توليد لستة ذكية ديال الدومينات بناء على الكلمة
        suggestions = [
            f"{keyword}", f"get{keyword}", f"{keyword}hub", 
            f"the{keyword}", f"{keyword}ly", f"my{keyword}"
        ]
        
        hunt_results = []
        
        progress_bar = st.progress(0)
        for idx, s in enumerate(suggestions):
            for ext in exts:
                full_d = s + ext
                status = check_domain(full_d)
                if "Available" in status:
                    val = estimate_value(full_d)
                    hunt_results.append({"Domain": full_d, "Status": status, "Estimated Value": val})
            progress_bar.progress((idx + 1) / len(suggestions))
            
        if hunt_results:
            df = pd.DataFrame(hunt_results)
            st.table(df)
            st.balloons()
        else:
            st.warning("ماعطى والو، جرب كلمة خرى!")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("V10.1 - No API Version")
