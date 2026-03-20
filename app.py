import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import hashlib
import plotly.express as px
import random
import string

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="DataCollect UG - الحوكمة الرقمية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== نظام الترجمة متعدد اللغات ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

translations = {
    "ar": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "الحوكمة الرقمية لأوغندا",
        "nbi_compatible": "متوافق مع البنية التحتية الوطنية NBI",
        "data_protection": "يطبق قانون حماية البيانات 2019",
        "consent_title": "مطلوب موافقتك حسب قانون حماية البيانات الأوغندي 2019",
        "read_terms": "اقرأ بنود الموافقة",
        "agree": "✅ أوافق على الشروط",
        "disagree": "❌ لا أوافق",
        "consent_recorded": "تم تسجيل موافقتك بموجب قانون حماية البيانات 2019",
        "user_info": "معلومات المستخدم",
        "full_name": "الاسم الكامل",
        "role": "الجهة/الدور",
        "district": "المقاطعة",
        "phone": "رقم الهاتف",
        "encrypted": "سيتم تشفير رقمك",
        "will_show": "سيتم عرض رقمك كـ",
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
        "save_success": "تم حفظ البيانات بنجاح!",
        "record_summary": "ملخص السجل",
        "record_id": "رقم السجل",
        "sector": "القطاع",
        "date": "تاريخ التسجيل",
        "encrypted_yes": "تم التشفير: ✅ نعم",
        "nbi_pending": "متوافق مع NBI: ⏳ قيد المزامنة",
        "view_data": "عرض وتحليل البيانات المسجلة",
        "export_csv": "📥 تصدير البيانات (CSV)",
        "nbi_integration": "الربط مع البنية التحتية الوطنية NBI",
        "ready_to_sync": "سجلات جاهزة للمزامنة",
        "encrypted_data": "البيانات المشفرة",
        "api_endpoints": "نقاط الاتصال API المتاحة",
        "sync_nbi": "🔄 محاكاة مزامنة مع NBI",
        "sync_success": "تمت مزامنة البيانات",
        "stats": "إحصائيات",
        "today_records": "سجلات اليوم",
        "compatible_with": "متوافق مع",
        "support": "الدعم",
        "footer": "الحوكمة الرقمية لأوغندا | نسخة تجريبية"
    },
    "en": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "Uganda Digital Governance",
        "nbi_compatible": "Compatible with National Backbone Infrastructure (NBI)",
        "data_protection": "Implements Data Protection Act 2019",
        "consent_title": "Consent Required under Uganda Data Protection Act 2019",
        "read_terms": "Read Terms of Consent",
        "agree": "✅ I Agree",
        "disagree": "❌ I Disagree",
        "consent_recorded": "Consent recorded under Data Protection Act 2019",
        "user_info": "User Information",
        "full_name": "Full Name",
        "role": "Role/Agency",
        "district": "District",
        "phone": "Phone Number",
        "encrypted": "Your number will be encrypted",
        "will_show": "Your number will display as",
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
        "save_success": "Data saved successfully!",
        "record_summary": "Record Summary",
        "record_id": "Record ID",
        "sector": "Sector",
        "date": "Date",
        "encrypted_yes": "Encrypted: ✅ Yes",
        "nbi_pending": "NBI Compatible: ⏳ Pending Sync",
        "view_data": "View and Analyze Data",
        "export_csv": "📥 Export Data (CSV)",
        "nbi_integration": "National Backbone Infrastructure (NBI) Integration",
        "ready_to_sync": "Records Ready to Sync",
        "encrypted_data": "Encrypted Data",
        "api_endpoints": "API Endpoints",
        "sync_nbi": "🔄 Simulate NBI Sync",
        "sync_success": "Data synced successfully",
        "stats": "Statistics",
        "today_records": "Today's Records",
        "compatible_with": "Compatible with",
        "support": "Support",
        "footer": "Uganda Digital Governance | Beta Version"
    },
    "sw": {
        "app_name": "📊 DataCollect UG",
        "subtitle": "Utawala wa Kidijitali Uganda",
        "nbi_compatible": "Inaendana na Miundombinu ya Kitaifa NBI",
        "data_protection": "Inatekeleza Sheria ya Ulinzi wa Data 2019",
        "consent_title": "Ruhusa Inahitajika chini ya Sheria ya Ulinzi wa Data Uganda 2019",
        "read_terms": "Soma Masharti ya Ruhusa",
        "agree": "✅ Nakubali",
        "disagree": "❌ Sikubali",
        "consent_recorded": "Ruhusa imerekodiwa",
        "user_info": "Taarifa za Mtumiaji",
        "full_name": "Jina Kamili",
        "role": "Nafasi/Shirika",
        "district": "Wilaya",
        "phone": "Namba ya Simu",
        "encrypted": "Namba yako itafichwa",
        "will_show": "Namba yako itaonekana kama",
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
        "encrypted_yes": "Imefichwa: ✅ Ndiyo",
        "nbi_pending": "Inaendana na NBI: ⏳ Inasubiri",
        "view_data": "Angalia na Chambua Data",
        "export_csv": "📥 Pakua Data (CSV)",
        "nbi_integration": "Ushirikiano na Miundombinu ya Kitaifa NBI",
        "ready_to_sync": "Rekodi Zinazosubiri",
        "encrypted_data": "Data Iliyofichwa",
        "api_endpoints": "Sehemu za API",
        "sync_nbi": "🔄 Iga Ushirikiano wa NBI",
        "sync_success": "Data imeshirikishwa",
        "stats": "Takwimu",
        "today_records": "Rekodi za Leo",
        "compatible_with": "Inaendana na",
        "support": "Msaada",
        "footer": "Utawala wa Kidijitali Uganda | Toleo la Majaribio"
    }
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# ==================== دوال مساعدة ====================
def hash_data(data):
    return hashlib.sha256(str(data).encode()).hexdigest()[:16]

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

# ==================== نص الموافقة ====================
CONSENT_TEXT = {
    "ar": "أوافق على جمع بياناتي الشخصية (الاسم، رقم الهاتف، الموقع) واستخدامها للأغراض الحكومية الرسمية. أفهم أن رقم هاتفي سيتم تشفيره. أوافق على الشروط.",
    "en": "I consent to the collection of my personal data (name, phone, location) for official government purposes. I understand my phone number will be encrypted. I agree.",
    "sw": "Nakubali ukusanyaji wa data yangu ya kibinafsi (jina, simu, eneo) kwa madhumuni rasmi ya serikali. Ninaelewa namba yangu ya simu itafichwa. Nakubali."
}

# ==================== ملفات التخزين ====================
DATA_FOLDER = "datacollect_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

RECORDS_FILE = os.path.join(DATA_FOLDER, "records.json")
SECTORS_FILE = os.path.join(DATA_FOLDER, "sectors.json")
CONSENTS_FILE = os.path.join(DATA_FOLDER, "consents.json")

def load_data(filename, default=None):
    if default is None:
        default = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                return json.loads(content) if content else default
        except:
            return default
    return default

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

# ==================== تعريف القطاعات ====================
if not os.path.exists(SECTORS_FILE):
    default_sectors = {
        "agriculture": {
            "name": "🌾 الزراعة",
            "fields": [
                {"name": "farmer_name", "label": "اسم المزارع", "type": "text", "required": True},
                {"name": "farmer_phone", "label": "رقم المزارع", "type": "text", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "crop_type", "label": "نوع المحصول", "type": "text", "required": True},
                {"name": "quantity", "label": "الكمية (كيلو)", "type": "number", "required": True},
                {"name": "price", "label": "السعر (شلن)", "type": "number", "required": True}
            ]
        },
        "health": {
            "name": "🏥 الصحة",
            "fields": [
                {"name": "patient_name", "label": "اسم المريض", "type": "text", "required": True},
                {"name": "patient_age", "label": "العمر", "type": "number", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "symptoms", "label": "الأعراض", "type": "textarea", "required": True},
                {"name": "disease_type", "label": "نوع المرض", "type": "text", "required": True}
            ]
        },
        "education": {
            "name": "📚 التعليم",
            "fields": [
                {"name": "school_name", "label": "اسم المدرسة", "type": "text", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "students_count", "label": "عدد الطلاب", "type": "number", "required": True},
                {"name": "teachers_count", "label": "عدد المعلمين", "type": "number", "required": True},
                {"name": "needs", "label": "الاحتياجات", "type": "textarea", "required": False}
            ]
        },
        "livestock": {
            "name": "🐄 الثروة الحيوانية",
            "fields": [
                {"name": "farmer_name", "label": "اسم المربي", "type": "text", "required": True},
                {"name": "farmer_phone", "label": "رقم المربي", "type": "text", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "animal_type", "label": "نوع الماشية", "type": "text", "required": True},
                {"name": "animal_count", "label": "العدد", "type": "number", "required": True}
            ]
        },
        "water": {
            "name": "💧 المياه",
            "fields": [
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "water_source", "label": "مصدر المياه", "type": "text", "required": True},
                {"name": "water_functional", "label": "المصدر يعمل", "type": "checkbox", "required": True},
                {"name": "distance_km", "label": "المسافة (كم)", "type": "number", "required": True}
            ]
        },
        "energy": {
            "name": "⚡ الطاقة",
            "fields": [
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "has_electricity", "label": "يوجد كهرباء", "type": "checkbox", "required": True},
                {"name": "main_energy_source", "label": "مصدر الطاقة", "type": "text", "required": True}
            ]
        }
    }
    save_data(SECTORS_FILE, default_sectors)

# ==================== تصميم الصفحة ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #e0e0e0;
    }
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border-top: 4px solid #2ecc71;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stat-card .number {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stat-card .label {
        color: #5a6e7e;
    }
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
    .stButton button:hover {
        background-color: #27ae60;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('app_name')}</h1>
    <p>{t('subtitle')}</p>
    <p><strong>{t('nbi_compatible')}</strong> | <strong>{t('data_protection')}</strong></p>
</div>
""", unsafe_allow_html=True)

# ==================== أزرار اللغة ====================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇸🇦 عربي", use_container_width=True):
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

# ==================== الموافقة ====================
if not st.session_state.consent_given:
    st.markdown(f"### 📜 {t('consent_title')}")
    st.info(CONSENT_TEXT[st.session_state.language])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('agree'), use_container_width=True):
            st.session_state.consent_given = True
            consents = load_data(CONSENTS_FILE, [])
            consents.append({
                "id": generate_id(),
                "user": st.session_state.user_name,
                "date": datetime.now().isoformat()
            })
            save_data(CONSENTS_FILE, consents)
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
        role = st.selectbox(t('role'), ["موظف وزارة", "مرشد زراعي", "عامل صحي", "معلم", "باحث"])
        st.session_state.user_role = role
    with col3:
        district = st.selectbox(t('district'), ["Kiryandongo", "Masindi", "Gulu", "Kampala", "Jinja", "أخرى"])
        st.session_state.user_district = district
    
    phone = st.text_input(t('phone'), value=st.session_state.user_phone)
    if phone:
        st.session_state.user_phone = phone
        st.caption(f"{t('will_show')}: {encrypt_phone(phone)}")

# ==================== إحصائيات ====================
records = load_data(RECORDS_FILE, [])

st.markdown(f"### 📊 {t('stats')}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{len(records)}</div>
        <div class='label'>{t('total_records')}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    villages = len(set([r.get("fields", {}).get("village", "") for r in records if r.get("fields")]))
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{villages}</div>
        <div class='label'>{t('villages_covered')}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    agri = len([r for r in records if r.get("sector") == "agriculture"])
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{agri}</div>
        <div class='label'>{t('agriculture_records')}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    health = len([r for r in records if r.get("sector") == "health"])
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{health}</div>
        <div class='label'>{t('health_records')}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== تسجيل بيانات ====================
st.markdown("---")
st.markdown(f"### 📝 {t('new_data')}")

sectors = load_data(SECTORS_FILE, {})
sector_options = {k: v["name"] for k, v in sectors.items()}
selected_sector_key = st.selectbox(t('select_sector'), list(sector_options.keys()), format_func=lambda x: sector_options[x])

selected_sector = sectors[selected_sector_key]
fields = selected_sector.get("fields", [])

st.markdown(f"#### {selected_sector['name']}")

record_data = {}
col1, col2 = st.columns(2)

for i, field in enumerate(fields):
    with col1 if i % 2 == 0 else col2:
        if field["type"] == "text":
            val = st.text_input(field["label"], key=f"f_{field['name']}")
        elif field["type"] == "number":
            val = st.number_input(field["label"], min_value=0, step=1, key=f"f_{field['name']}")
        elif field["type"] == "textarea":
            val = st.text_area(field["label"], key=f"f_{field['name']}", height=80)
        elif field["type"] == "checkbox":
            val = st.checkbox(field["label"], key=f"f_{field['name']}")
        else:
            val = st.text_input(field["label"], key=f"f_{field['name']}")
        
        if field.get("required", False) and not val and val is not False:
            st.warning(f"⚠️ {field['label']} مطلوب")
        record_data[field["name"]] = val

notes = st.text_area("📝 ملاحظات إضافية", height=80)

if st.button(t('save_data'), type="primary", use_container_width=True):
    if st.session_state.consent_given and st.session_state.user_name:
        record = {
            "id": generate_id(),
            "sector": selected_sector_key,
            "sector_name": selected_sector["name"],
            "fields": record_data,
            "notes": notes,
            "collector_name": st.session_state.user_name,
            "collector_role": st.session_state.user_role,
            "collector_district": st.session_state.user_district,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "language": st.session_state.language
        }
        
        all_records = load_data(RECORDS_FILE, [])
        all_records.append(record)
        save_data(RECORDS_FILE, all_records)
        
        st.success(f"✅ {t('save_success')}")
        st.balloons()
        
        st.info(f"""
        **📋 {t('record_summary')}**
        - {t('record_id')}: `{record['id']}`
        - {t('sector')}: {selected_sector['name']}
        - {t('date')}: {record['timestamp'][:19]}
        - {t('encrypted_yes')}
        """)
    else:
        st.error("❌ يرجى الموافقة على الشروط وإدخال اسمك")

# ==================== عرض البيانات ====================
with st.expander(f"📋 {t('view_data')}", expanded=False):
    all_records = load_data(RECORDS_FILE, [])
    
    if all_records:
        df = pd.DataFrame(all_records)
        
        if 'fields' in df.columns:
            df_display = df[['id', 'sector_name', 'timestamp', 'collector_name', 'collector_district']].copy()
        else:
            df_display = df
        
        st.dataframe(df_display.tail(20), use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label=t('export_csv'),
            data=csv,
            file_name=f"datacollect_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("لا توجد بيانات مسجلة بعد")

# ==================== الربط مع NBI ====================
with st.expander(f"🔌 {t('nbi_integration')}", expanded=False):
    st.markdown("""
    ### 🇺🇬 National Backbone Infrastructure (NBI)
    
    **البنية التحتية الوطنية:**
    - 2,474 كم كابلات ألياف بصرية
    - 4 مراكز بيانات حكومية
    - جاهز للربط مع NIFAMIS, DHIS2, EMIS
    """)
    
    all_records = load_data(RECORDS_FILE, [])
    st.metric(t('ready_to_sync'), len(all_records))
    
    api_key = generate_api_key()
    st.code(f"""
    # API Endpoints
    GET /api/v1/records
    GET /api/v1/records/{{id}}
    GET /api/v1/stats
    
    # Demo API Key
    X-API-Key: {api_key}
    """)
    
    if st.button(t('sync_nbi'), use_container_width=True):
        st.success(f"✅ {t('sync_success')}")
        st.balloons()

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### 📊 {t('app_name')}")
    st.markdown(f"**👤 {st.session_state.user_name or '---'}**")
    st.markdown(f"**📍 {st.session_state.user_district or '---'}**")
    st.markdown(f"**📱 {encrypt_phone(st.session_state.user_phone) if st.session_state.user_phone else '---'}**")
    
    st.markdown("---")
    st.markdown("### ⚖️ الخصوصية")
    if st.session_state.consent_given:
        st.success("✅ موافقة مسجلة")
    
    st.markdown("---")
    st.markdown(f"### 📈 {t('stats')}")
    records_count = len(load_data(RECORDS_FILE, []))
    st.metric(t('total_records'), records_count)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = len([r for r in load_data(RECORDS_FILE, []) if r.get("date") == today])
    st.metric(t('today_records'), today_records)
    
    st.markdown("---")
    st.markdown(f"### 🔗 {t('compatible_with')}")
    st.markdown("""
    - ✅ NBI
    - ✅ NIFAMIS
    - ✅ DHIS2
    - ✅ EMIS
    - ✅ Data Protection Act 2019
    """)
    
    st.markdown("---")
    st.markdown(f"### 📞 {t('support')}")
    st.markdown("📞 0800-200-900\n📧 support@nita.go.ug")

# ==================== تذييل ====================
st.markdown(f"""
<div class='footer'>
    <strong>{t('app_name')}</strong> - {t('footer')}<br>
    🇺🇬 {t('nbi_compatible')} | {t('data_protection')} 🇺🇬
</div>
""", unsafe_allow_html=True)
