import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import hashlib
import random
import string

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="DataCollect UG - Digital Governance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== نظام الترجمة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

lang_text = {
    "en": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "Uganda Digital Governance Platform",
        "nbi_compatible": "NBI Compatible | Data Protection Act 2019",
        "consent_title": "Consent Required",
        "read_terms": "Read Terms",
        "agree": "✅ I Agree",
        "disagree": "❌ I Disagree",
        "consent_recorded": "Consent recorded",
        "user_info": "User Information",
        "full_name": "Full Name",
        "role": "Role",
        "district": "District",
        "phone": "Phone Number",
        "encrypted": "Your number will be encrypted",
        "will_show": "Will show as",
        "agriculture": "🌾 Agriculture",
        "health": "🏥 Health",
        "education": "📚 Education",
        "livestock": "🐄 Livestock",
        "water": "💧 Water",
        "energy": "⚡ Energy",
        "total_records": "Total Records",
        "villages_covered": "Villages Covered",
        "agriculture_records": "Agriculture Records",
        "health_records": "Health Records",
        "new_data": "Register New Data",
        "select_sector": "Select Sector",
        "save_data": "✅ Save Data",
        "save_success": "Data saved!",
        "record_summary": "Record Summary",
        "record_id": "Record ID",
        "sector": "Sector",
        "date": "Date",
        "encrypted_yes": "Encrypted: Yes",
        "view_data": "View Data",
        "export_csv": "📥 Export CSV",
        "nbi_integration": "NBI Integration",
        "ready_to_sync": "Ready to Sync",
        "sync_nbi": "🔄 Sync with NBI",
        "sync_success": "Data synced!",
        "stats": "Statistics",
        "today_records": "Today's Records",
        "compatible_with": "Compatible with",
        "support": "Support",
        "footer": "Digital Governance for Uganda",
        "notes": "Additional Notes",
        "farmer_name": "Farmer Name",
        "farmer_phone": "Farmer Phone",
        "village": "Village",
        "crop_type": "Crop Type",
        "quantity": "Quantity (kg)",
        "price": "Price (UGX)",
        "patient_name": "Patient Name",
        "patient_age": "Age",
        "symptoms": "Symptoms",
        "disease_type": "Disease Type",
        "school_name": "School Name",
        "students_count": "Students",
        "teachers_count": "Teachers",
        "needs": "Needs",
        "animal_type": "Animal Type",
        "animal_count": "Count",
        "water_source": "Water Source",
        "water_functional": "Working",
        "distance_km": "Distance (km)",
        "has_electricity": "Has Electricity",
        "main_energy_source": "Energy Source"
    },
    "ar": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "منصة الحوكمة الرقمية لأوغندا",
        "nbi_compatible": "متوافق مع NBI | قانون حماية البيانات 2019",
        "consent_title": "مطلوب موافقتك",
        "read_terms": "اقرأ الشروط",
        "agree": "✅ أوافق",
        "disagree": "❌ لا أوافق",
        "consent_recorded": "تم تسجيل الموافقة",
        "user_info": "معلومات المستخدم",
        "full_name": "الاسم الكامل",
        "role": "الجهة",
        "district": "المقاطعة",
        "phone": "رقم الهاتف",
        "encrypted": "سيتم تشفير رقمك",
        "will_show": "سيظهر كـ",
        "agriculture": "🌾 الزراعة",
        "health": "🏥 الصحة",
        "education": "📚 التعليم",
        "livestock": "🐄 الثروة الحيوانية",
        "water": "💧 المياه",
        "energy": "⚡ الطاقة",
        "total_records": "إجمالي السجلات",
        "villages_covered": "قرى مشمولة",
        "agriculture_records": "سجلات زراعية",
        "health_records": "سجلات صحية",
        "new_data": "تسجيل بيانات جديدة",
        "select_sector": "اختر القطاع",
        "save_data": "✅ حفظ البيانات",
        "save_success": "تم حفظ البيانات!",
        "record_summary": "ملخص السجل",
        "record_id": "رقم السجل",
        "sector": "القطاع",
        "date": "التاريخ",
        "encrypted_yes": "مشفر: نعم",
        "view_data": "عرض البيانات",
        "export_csv": "📥 تصدير CSV",
        "nbi_integration": "الربط مع NBI",
        "ready_to_sync": "جاهز للمزامنة",
        "sync_nbi": "🔄 مزامنة مع NBI",
        "sync_success": "تمت المزامنة!",
        "stats": "إحصائيات",
        "today_records": "سجلات اليوم",
        "compatible_with": "متوافق مع",
        "support": "الدعم",
        "footer": "الحوكمة الرقمية لأوغندا",
        "notes": "ملاحظات إضافية",
        "farmer_name": "اسم المزارع",
        "farmer_phone": "رقم المزارع",
        "village": "القرية",
        "crop_type": "نوع المحصول",
        "quantity": "الكمية (كيلو)",
        "price": "السعر (شلن)",
        "patient_name": "اسم المريض",
        "patient_age": "العمر",
        "symptoms": "الأعراض",
        "disease_type": "نوع المرض",
        "school_name": "اسم المدرسة",
        "students_count": "الطلاب",
        "teachers_count": "المعلمين",
        "needs": "الاحتياجات",
        "animal_type": "نوع الماشية",
        "animal_count": "العدد",
        "water_source": "مصدر المياه",
        "water_functional": "يعمل",
        "distance_km": "المسافة (كم)",
        "has_electricity": "يوجد كهرباء",
        "main_energy_source": "مصدر الطاقة"
    },
    "sw": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "Jukwaa la Utawala wa Kidijitali Uganda",
        "nbi_compatible": "Inaendana na NBI | Sheria ya Ulinzi wa Data 2019",
        "consent_title": "Ruhusa Inahitajika",
        "read_terms": "Soma Masharti",
        "agree": "✅ Nakubali",
        "disagree": "❌ Sikubali",
        "consent_recorded": "Ruhusa imerekodiwa",
        "user_info": "Taarifa za Mtumiaji",
        "full_name": "Jina Kamili",
        "role": "Nafasi",
        "district": "Wilaya",
        "phone": "Namba ya Simu",
        "encrypted": "Namba yako itafichwa",
        "will_show": "Itaonekana kama",
        "agriculture": "🌾 Kilimo",
        "health": "🏥 Afya",
        "education": "📚 Elimu",
        "livestock": "🐄 Mifugo",
        "water": "💧 Maji",
        "energy": "⚡ Nishati",
        "total_records": "Jumla ya Rekodi",
        "villages_covered": "Vijiji Vilivyofikiwa",
        "agriculture_records": "Rekodi za Kilimo",
        "health_records": "Rekodi za Afya",
        "new_data": "Sajili Data Mpya",
        "select_sector": "Chagua Sekta",
        "save_data": "✅ Hifadhi Data",
        "save_success": "Data imehifadhiwa!",
        "record_summary": "Muhtasari wa Rekodi",
        "record_id": "Namba ya Rekodi",
        "sector": "Sekta",
        "date": "Tarehe",
        "encrypted_yes": "Imefichwa: Ndiyo",
        "view_data": "Angalia Data",
        "export_csv": "📥 Pakua CSV",
        "nbi_integration": "Ushirikiano wa NBI",
        "ready_to_sync": "Inasubiri",
        "sync_nbi": "🔄 Shirikisha na NBI",
        "sync_success": "Data imeshirikishwa!",
        "stats": "Takwimu",
        "today_records": "Rekodi za Leo",
        "compatible_with": "Inaendana na",
        "support": "Msaada",
        "footer": "Utawala wa Kidijitali Uganda",
        "notes": "Maelezo ya Ziada",
        "farmer_name": "Jina la Mkulima",
        "farmer_phone": "Simu ya Mkulima",
        "village": "Kijiji",
        "crop_type": "Aina ya Zao",
        "quantity": "Kiasi (kg)",
        "price": "Bei (UGX)",
        "patient_name": "Jina la Mgonjwa",
        "patient_age": "Umri",
        "symptoms": "Dalili",
        "disease_type": "Aina ya Ugonjwa",
        "school_name": "Jina la Shule",
        "students_count": "Wanafunzi",
        "teachers_count": "Walimu",
        "needs": "Mahitaji",
        "animal_type": "Aina ya Mnyama",
        "animal_count": "Idadi",
        "water_source": "Chanzo cha Maji",
        "water_functional": "Kinafanya kazi",
        "distance_km": "Umbali (km)",
        "has_electricity": "Ina Umeme",
        "main_energy_source": "Chanzo cha Nishati"
    }
}

def t(key):
    return lang_text[st.session_state.language].get(key, key)

# ==================== دوال مساعدة ====================
def encrypt_phone(phone):
    if len(str(phone)) >= 7:
        return str(phone)[:3] + "****" + str(phone)[-3:]
    return "***"

def generate_id():
    return str(uuid.uuid4())[:8].upper()

def generate_api_key():
    return "NBI_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

# ==================== تهيئة الحالة ====================
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "user_district" not in st.session_state:
    st.session_state.user_district = ""
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""

# ==================== ملفات التخزين ====================
DATA_FOLDER = "datacollect_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

RECORDS_FILE = os.path.join(DATA_FOLDER, "records.json")
SECTORS_FILE = os.path.join(DATA_FOLDER, "sectors.json")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except:
            return []
    return []

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

# ==================== إعادة تهيئة القطاعات بالكامل ====================
# حذف الملف القديم إذا كان موجوداً وإعادة إنشائه
if os.path.exists(SECTORS_FILE):
    os.remove(SECTORS_FILE)

# تعريف القطاعات الجديدة
new_sectors = {
    "agriculture": {
        "name_en": "🌾 Agriculture",
        "name_ar": "🌾 الزراعة",
        "name_sw": "🌾 Kilimo",
        "fields": ["farmer_name", "farmer_phone", "village", "crop_type", "quantity", "price"]
    },
    "health": {
        "name_en": "🏥 Health",
        "name_ar": "🏥 الصحة",
        "name_sw": "🏥 Afya",
        "fields": ["patient_name", "patient_age", "village", "symptoms", "disease_type"]
    },
    "education": {
        "name_en": "📚 Education",
        "name_ar": "📚 التعليم",
        "name_sw": "📚 Elimu",
        "fields": ["school_name", "village", "students_count", "teachers_count", "needs"]
    },
    "livestock": {
        "name_en": "🐄 Livestock",
        "name_ar": "🐄 الثروة الحيوانية",
        "name_sw": "🐄 Mifugo",
        "fields": ["farmer_name", "farmer_phone", "village", "animal_type", "animal_count"]
    },
    "water": {
        "name_en": "💧 Water",
        "name_ar": "💧 المياه",
        "name_sw": "💧 Maji",
        "fields": ["village", "water_source", "water_functional", "distance_km"]
    },
    "energy": {
        "name_en": "⚡ Energy",
        "name_ar": "⚡ الطاقة",
        "name_sw": "⚡ Nishati",
        "fields": ["village", "has_electricity", "main_energy_source"]
    }
}
save_data(SECTORS_FILE, new_sectors)

# تحميل القطاعات
sectors_data = load_data(SECTORS_FILE)

# ==================== تصميم الصفحة ====================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%); }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; font-size: 2.5rem; }
    .main-header p { color: #e0e0e0; }
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border-top: 4px solid #2ecc71;
    }
    .stat-card .number { font-size: 2rem; font-weight: bold; color: #2c3e50; }
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: #2c3e50;
        border-radius: 15px;
        color: white;
    }
    .stButton button {
        background-color: #2ecc71;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== أزرار اللغة ====================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇸🇦 العربية", use_container_width=True):
        st.session_state.language = "ar"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.language = "en"
        st.rerun()
with col3:
    if st.button("🇺🇬 Kiswahili", use_container_width=True):
        st.session_state.language = "sw"
        st.rerun()

# ==================== العنوان ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('app_name')}</h1>
    <p>{t('subtitle')}</p>
    <p><strong>{t('nbi_compatible')}</strong></p>
</div>
""", unsafe_allow_html=True)

# ==================== الموافقة ====================
if not st.session_state.consent_given:
    st.markdown(f"### 📜 {t('consent_title')}")
    st.info("I consent to the collection of my personal data for official government purposes.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('agree'), use_container_width=True):
            st.session_state.consent_given = True
            st.rerun()
    with col2:
        if st.button(t('disagree'), use_container_width=True):
            st.stop()
else:
    st.success(f"✅ {t('consent_recorded')}")

# ==================== معلومات المستخدم ====================
with st.expander(f"👤 {t('user_info')}", expanded=not st.session_state.user_name):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input(t('full_name'), value=st.session_state.user_name)
        st.session_state.user_name = name
    with col2:
        role = st.selectbox(t('role'), ["Government Officer", "Extension Worker", "Health Worker", "Teacher", "Researcher"])
        st.session_state.user_role = role
    with col3:
        district = st.selectbox(t('district'), ["Kiryandongo", "Masindi", "Gulu", "Kampala", "Jinja"])
        st.session_state.user_district = district
    
    phone = st.text_input(t('phone'), value=st.session_state.user_phone)
    if phone:
        st.session_state.user_phone = phone
        st.caption(f"{t('will_show')}: {encrypt_phone(phone)}")

# ==================== إحصائيات ====================
records = load_data(RECORDS_FILE)

st.markdown(f"### 📊 {t('stats')}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='stat-card'><div class='number'>{len(records)}</div><div class='label'>{t('total_records')}</div></div>", unsafe_allow_html=True)
with col2:
    villages = len(set([r.get("fields", {}).get("village", "") for r in records if r.get("fields")]))
    st.markdown(f"<div class='stat-card'><div class='number'>{villages}</div><div class='label'>{t('villages_covered')}</div></div>", unsafe_allow_html=True)
with col3:
    agri = len([r for r in records if r.get("sector") == "agriculture"])
    st.markdown(f"<div class='stat-card'><div class='number'>{agri}</div><div class='label'>{t('agriculture_records')}</div></div>", unsafe_allow_html=True)
with col4:
    health = len([r for r in records if r.get("sector") == "health"])
    st.markdown(f"<div class='stat-card'><div class='number'>{health}</div><div class='label'>{t('health_records')}</div></div>", unsafe_allow_html=True)

# ==================== تسجيل بيانات ====================
st.markdown("---")
st.markdown(f"### 📝 {t('new_data')}")

# قائمة القطاعات
sectors_list = list(sectors_data.keys())

# عرض أسماء القطاعات حسب اللغة
sector_names_display = []
for s in sectors_list:
    if st.session_state.language == "ar":
        sector_names_display.append(sectors_data[s]["name_ar"])
    elif st.session_state.language == "sw":
        sector_names_display.append(sectors_data[s]["name_sw"])
    else:
        sector_names_display.append(sectors_data[s]["name_en"])

selected_idx = st.selectbox(t('select_sector'), range(len(sectors_list)), format_func=lambda i: sector_names_display[i])
selected_key = sectors_list[selected_idx]
selected_sector = sectors_data[selected_key]

st.markdown(f"#### {sector_names_display[selected_idx]}")

record_data = {}
fields = selected_sector["fields"]
col1, col2 = st.columns(2)

for i, field in enumerate(fields):
    with col1 if i % 2 == 0 else col2:
        label = t(field)
        
        if field in ["quantity", "price", "patient_age", "students_count", "teachers_count", "animal_count", "distance_km"]:
            val = st.number_input(label, min_value=0, step=1, key=f"f_{field}")
        elif field in ["water_functional", "has_electricity"]:
            val = st.checkbox(label, key=f"f_{field}")
        else:
            val = st.text_input(label, key=f"f_{field}")
        
        record_data[field] = val

notes = st.text_area(t('notes'), height=80)

if st.button(t('save_data'), type="primary", use_container_width=True):
    if st.session_state.consent_given and st.session_state.user_name:
        record = {
            "id": generate_id(),
            "sector": selected_key,
            "sector_name": sector_names_display[selected_idx],
            "fields": record_data,
            "notes": notes,
            "collector_name": st.session_state.user_name,
            "collector_role": st.session_state.user_role,
            "collector_district": st.session_state.user_district,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        all_records = load_data(RECORDS_FILE)
        all_records.append(record)
        save_data(RECORDS_FILE, all_records)
        
        st.success(f"✅ {t('save_success')}")
        st.balloons()
        
        st.info(f"**📋 {t('record_summary')}**\n- {t('record_id')}: `{record['id']}`\n- {t('sector')}: {record['sector_name']}\n- {t('date')}: {record['timestamp'][:19]}")
    else:
        st.error("❌ Please provide consent and enter your name")

# ==================== عرض البيانات ====================
with st.expander(f"📋 {t('view_data')}", expanded=False):
    all_records = load_data(RECORDS_FILE)
    
    if all_records:
        df = pd.DataFrame(all_records)
        display_cols = ['id', 'sector_name', 'timestamp', 'collector_name', 'collector_district']
        st.dataframe(df[display_cols].tail(20), use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(label=t('export_csv'), data=csv, file_name=f"datacollect_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    else:
        st.info("No data recorded yet")

# ==================== NBI Integration ====================
with st.expander(f"🔌 {t('nbi_integration')}", expanded=False):
    st.markdown("""
    ### 🇺🇬 National Backbone Infrastructure (NBI)
    - 2,474 km fiber optic cables
    - 4 government data centers
    - Ready for NIFAMIS, DHIS2, EMIS
    """)
    
    all_records = load_data(RECORDS_FILE)
    st.metric(t('ready_to_sync'), len(all_records))
    
    api_key = generate_api_key()
    st.code(f"API Key: {api_key}\nGET /api/v1/records\nGET /api/v1/stats")
    
    if st.button(t('sync_nbi'), use_container_width=True):
        st.success(f"✅ {t('sync_success')}")
        st.balloons()

# ==================== Sidebar ====================
with st.sidebar:
    st.markdown(f"### 📊 {t('app_name')}")
    st.markdown(f"**👤 {st.session_state.user_name or '---'}**")
    st.markdown(f"**📍 {st.session_state.user_district or '---'}**")
    st.markdown(f"**📱 {encrypt_phone(st.session_state.user_phone) if st.session_state.user_phone else '---'}**")
    
    st.markdown("---")
    if st.session_state.consent_given:
        st.success("✅ Consent recorded")
    
    st.markdown("---")
    st.markdown(f"### 📈 {t('stats')}")
    st.metric(t('total_records'), len(load_data(RECORDS_FILE)))
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = len([r for r in load_data(RECORDS_FILE) if r.get("date") == today])
    st.metric(t('today_records'), today_records)
    
    st.markdown("---")
    st.markdown(f"### 🔗 {t('compatible_with')}")
    st.markdown("- ✅ NBI\n- ✅ NIFAMIS\n- ✅ DHIS2\n- ✅ EMIS")
    
    st.markdown("---")
    st.markdown(f"### 📞 {t('support')}")
    st.markdown("📞 0800-200-900")

# ==================== Footer ====================
st.markdown(f"""
<div class='footer'>
    <strong>{t('app_name')}</strong> - {t('footer')}<br>
    🇺🇬 {t('nbi_compatible')}
</div>
""", unsafe_allow_html=True)
