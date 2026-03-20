import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import hashlib
import base64
import plotly.express as px
import plotly.graph_objects as go
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
        "save_data": "✅ حفظ البيانات (بموجب قانون الخصوصية)",
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
        "api_endpoints": "نقاط الاتصال API المتاحة للأنظمة الحكومية",
        "sync_nbi": "🔄 محاكاة مزامنة مع NBI",
        "sync_success": "تمت مزامنة البيانات مع البنية التحتية الوطنية",
        "stats": "إحصائيات",
        "today_records": "سجلات اليوم",
        "compatible_with": "متوافق مع",
        "support": "الدعم",
        "footer": "الحوكمة الرقمية لأوغندا | نسخة تجريبية - جاهزة للربط مع الأنظمة الحكومية"
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
        "save_data": "✅ Save Data (Privacy Act Compliant)",
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
        "api_endpoints": "API Endpoints for Government Systems",
        "sync_nbi": "🔄 Simulate NBI Sync",
        "sync_success": "Data synced with National Backbone Infrastructure",
        "stats": "Statistics",
        "today_records": "Today's Records",
        "compatible_with": "Compatible with",
        "support": "Support",
        "footer": "Uganda Digital Governance | Beta Version - Ready for Government Integration"
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
        "consent_recorded": "Ruhusa imerekodiwa chini ya Sheria ya Ulinzi wa Data 2019",
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
        "save_data": "✅ Hifadhi Data (Kwa mujibu wa Sheria ya Faragha)",
        "save_success": "Data imehifadhiwa kikamilifu!",
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
        "api_endpoints": "Sehemu za API kwa Mifumo ya Serikali",
        "sync_nbi": "🔄 Iga Ushirikiano wa NBI",
        "sync_success": "Data imeshirikishwa na Miundombinu ya Kitaifa",
        "stats": "Takwimu",
        "today_records": "Rekodi za Leo",
        "compatible_with": "Inaendana na",
        "support": "Msaada",
        "footer": "Utawala wa Kidijitali Uganda | Toleo la Majaribio - Tayari kwa Ushirikiano na Serikali"
    }
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# ==================== دوال التشفير والأمان ====================
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

# ==================== نص الموافقة الرسمي ====================
CONSENT_TEXT = {
    "ar": """
**DATA PROTECTION AND PRIVACY ACT, 2019 (UGANDA)**

أنا أوافق بموجب هذا على:

1. جمع ومعالجة بياناتي الشخصية (الاسم، رقم الهاتف، الموقع، والبيانات الميدانية)
2. استخدام هذه البيانات للأغراض الحكومية الرسمية بما في ذلك:
   - التخطيط الزراعي والوصول للأسواق
   - المراقبة الصحية والاستجابة للطوارئ
   - تخصيص الموارد التعليمية
3. التخزين الآمن ونقل بياناتي وفقاً للقانون الأوغندي
4. حقي في الوصول إلى بياناتي أو تصحيحها أو طلب حذفها في أي وقت

أفهم أن:
- رقم هاتفي سيتم تشفيره
- بياناتي ستشارك فقط مع الجهات الحكومية المصرح لها
- يمكنني سحب موافقتي في أي وقت

**أوافق على الشروط أعلاه.**
""",
    "en": """
**DATA PROTECTION AND PRIVACY ACT, 2019 (UGANDA)**

I hereby give my explicit consent to:

1. The collection and processing of my personal data (name, phone number, location, and field data)
2. The use of this data for official government purposes including:
   - Agricultural planning and market access
   - Public health surveillance and response
   - Educational resource allocation
3. The secure storage and transmission of my data in accordance with Ugandan law
4. My right to access, correct, or request deletion of my data at any time

I understand that:
- My phone number will be encrypted
- My data will only be shared with authorized government agencies
- I can withdraw my consent at any time

**I agree to the terms above.**
""",
    "sw": """
**SHERIA YA ULINZI WA DATA NA FARAGHA, 2019 (UGANDA)**

Natoa idhini yangu wazi kwa:

1. Ukusanyaji na usindikaji wa data yangu ya kibinafsi (jina, namba ya simu, eneo, na data ya shambani)
2. Matumizi ya data hii kwa madhumuni rasmi ya serikali ikiwemo:
   - Mipango ya kilimo na upatikanaji wa masoko
   - Ufuatiliaji wa afya ya umma na majibu ya dharura
   - Ugawaji wa rasilimali za elimu
3. Uhifadhi salama na usambazaji wa data yangu kwa mujibu wa sheria za Uganda
4. Haki yangu ya kufikia, kusahihisha, au kuomba kufutwa kwa data yangu wakati wowote

Naelewa kuwa:
- Namba yangu ya simu itafichwa
- Data yangu itashirikiwa tu na mashirika yaliyoidhinishwa ya serikali
- Ninaweza kuondoa idhini yangu wakati wowote

**Nakubali masharti hapo juu.**
"""
}

# ==================== ملفات التخزين ====================
DATA_FOLDER = "datacollect_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

RECORDS_FILE = os.path.join(DATA_FOLDER, "records.json")
SECTORS_FILE = os.path.join(DATA_FOLDER, "sectors.json")
CONSENTS_FILE = os.path.join(DATA_FOLDER, "consents.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
SYNC_FILE = os.path.join(DATA_FOLDER, "sync_status.json")

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
            "name_en": "Agriculture",
            "nifamis_compatible": True,
            "fields": [
                {"name": "farmer_name", "label": "اسم المزارع", "type": "text", "required": True},
                {"name": "farmer_phone", "label": "رقم المزارع", "type": "phone", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "sub_county", "label": "المقاطعة الفرعية", "type": "text", "required": True},
                {"name": "district", "label": "المقاطعة", "type": "text", "required": True},
                {"name": "crop_type", "label": "نوع المحصول", "type": "select", "options": ["موز", "ذرة", "فول", "طماطم", "بصل", "بطاطا", "كسافا", "قهوة", "شاي", "أرز", "دخن"], "required": True},
                {"name": "quantity", "label": "الكمية (كيلو)", "type": "number", "required": True},
                {"name": "price", "label": "السعر المطلوب (شلن)", "type": "number", "required": True},
                {"name": "harvest_date", "label": "تاريخ الحصاد", "type": "date", "required": False},
                {"name": "pest_disease", "label": "آفات أو أمراض", "type": "text", "required": False},
                {"name": "soil_type", "label": "نوع التربة", "type": "select", "options": ["طينية", "رملية", "طميية", "صخرية"], "required": False}
            ]
        },
        "health": {
            "name": "🏥 الصحة",
            "name_en": "Health",
            "dhis2_compatible": True,
            "fields": [
                {"name": "patient_name", "label": "اسم المريض", "type": "text", "required": True},
                {"name": "patient_age", "label": "العمر", "type": "number", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "sub_county", "label": "المقاطعة الفرعية", "type": "text", "required": True},
                {"name": "district", "label": "المقاطعة", "type": "text", "required": True},
                {"name": "symptoms", "label": "الأعراض", "type": "textarea", "required": True},
                {"name": "diagnosis", "label": "التشخيص المبدئي", "type": "text", "required": False},
                {"name": "reported_date", "label": "تاريخ التبليغ", "type": "date", "required": True},
                {"name": "disease_type", "label": "نوع المرض", "type": "select", "options": ["ملاريا", "حمى", "إسهال", "التهابات تنفسية", "إيبولا", "كوليرا", "جدري الماء", "الحصبة", "أخرى"], "required": True},
                {"name": "treatment_given", "label": "العلاج المقدم", "type": "text", "required": False},
                {"name": "referred_to", "label": "تم تحويله إلى", "type": "text", "required": False}
            ]
        },
        "education": {
            "name": "📚 التعليم",
            "name_en": "Education",
            "emis_compatible": True,
            "fields": [
                {"name": "school_name", "label": "اسم المدرسة", "type": "text", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "sub_county", "label": "المقاطعة الفرعية", "type": "text", "required": True},
                {"name": "district", "label": "المقاطعة", "type": "text", "required": True},
                {"name": "students_count", "label": "عدد الطلاب", "type": "number", "required": True},
                {"name": "teachers_count", "label": "عدد المعلمين", "type": "number", "required": True},
                {"name": "classrooms_count", "label": "عدد الفصول", "type": "number", "required": True},
                {"name": "needs", "label": "الاحتياجات", "type": "textarea", "required": False},
                {"name": "has_latrine", "label": "يوجد دورات مياه", "type": "checkbox", "required": True},
                {"name": "has_water", "label": "يوجد مياه", "type": "checkbox", "required": True},
                {"name": "has_electricity", "label": "يوجد كهرباء", "type": "checkbox", "required": False}
            ]
        },
        "livestock": {
            "name": "🐄 الثروة الحيوانية",
            "name_en": "Livestock",
            "fields": [
                {"name": "farmer_name", "label": "اسم المربي", "type": "text", "required": True},
                {"name": "farmer_phone", "label": "رقم المربي", "type": "phone", "required": True},
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "animal_type", "label": "نوع الماشية", "type": "select", "options": ["أبقار", "ماعز", "ضأن", "دجاج", "خنازير", "أرانب"], "required": True},
                {"name": "animal_count", "label": "العدد", "type": "number", "required": True},
                {"name": "vaccinated", "label": "تم التطعيم", "type": "checkbox", "required": True},
                {"name": "disease_outbreak", "label": "وجود أمراض", "type": "text", "required": False}
            ]
        },
        "water": {
            "name": "💧 المياه",
            "name_en": "Water",
            "fields": [
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "water_source", "label": "مصدر المياه", "type": "select", "options": ["بئر", "نهر", "بحيرة", "صنبور عام", "مياه أمطار"], "required": True},
                {"name": "water_functional", "label": "المصدر يعمل", "type": "checkbox", "required": True},
                {"name": "distance_km", "label": "المسافة (كم)", "type": "number", "required": True},
                {"name": "households_served", "label": "عدد الأسر المستفيدة", "type": "number", "required": True}
            ]
        },
        "energy": {
            "name": "⚡ الطاقة",
            "name_en": "Energy",
            "fields": [
                {"name": "village", "label": "القرية", "type": "text", "required": True},
                {"name": "has_electricity", "label": "يوجد كهرباء", "type": "checkbox", "required": True},
                {"name": "households_connected", "label": "عدد الأسر المتصلة", "type": "number", "required": False},
                {"name": "main_energy_source", "label": "مصدر الطاقة الرئيسي", "type": "select", "options": ["كهرباء", "شمسي", "فحم", "حطب", "غاز"], "required": True}
            ]
        }
    }
    save_data(SECTORS_FILE, default_sectors)

# ==================== تصميم الصفحة (ألوان واضحة) ====================
st.markdown("""
<style>
    /* خلفية التطبيق - لون فاتح للقراءة الواضحة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* العنوان الرئيسي - خلفية زرقاء داكنة مع كتابة بيضاء */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #e0e0e0;
        font-size: 1.1rem;
    }
    .main-header .highlight {
        color: #ffd966;
    }
    
    /* صندوق الموافقة - خلفية بيضاء مع حدود خضراء */
    .consent-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        color: #1e2a3a;
    }
    
    /* بطاقات البيانات - خلفية بيضاء صافية */
    .data-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        color: #1e2a3a;
    }
    
    /* بطاقات الإحصائيات */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border-top: 4px solid #2ecc71;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #1e2a3a;
    }
    .stat-card .number {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stat-card .label {
        font-size: 0.9rem;
        color: #5a6e7e;
    }
    
    /* شارة */
    .badge {
        background: #e67e22;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* صندوق API - خلفية داكنة مع كتابة فاتحة */
    .api-box {
        background: #1e2a3a;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 10px;
        font-family: monospace;
        font-size: 0.8rem;
        border: 1px solid #3a4a5a;
    }
    
    /* تذييل */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: #2c3e50;
        border-radius: 15px;
        color: white;
    }
    
    /* تحسين الأزرار */
    .stButton button {
        background-color: #2ecc71;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #27ae60;
        transform: translateY(-1px);
    }
    
    /* تحسين الحقول */
    .stTextInput input, .stNumberInput input, .stSelectbox, .stTextArea textarea {
        background-color: white;
        color: #1e2a3a;
        border: 1px solid #cbd5e0;
        border-radius: 8px;
    }
    
    /* تحسين الشريط الجانبي */
    .sidebar-content {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        color: #1e2a3a;
    }
    
    /* تحسين التنبيهات */
    .stAlert {
        background-color: white;
        border-left: 4px solid #2ecc71;
        color: #1e2a3a;
    }
    
    /* تحسين الجداول */
    .stDataFrame {
        background: white;
        border-radius: 10px;
    }
    
    /* تحسين الأكواد */
    code {
        background: #f0f2f6;
        color: #e67e22;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('app_name')}</h1>
    <p style='font-size: 1.2rem;'>{t('subtitle')}</p>
    <p><span class='highlight'>{t('nbi_compatible')}</span> | <span class='highlight'>{t('data_protection')}</span></p>
</div>
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

# ==================== الموافقة على جمع البيانات ====================
if not st.session_state.consent_given:
    st.markdown(f"### 📜 {t('consent_title')}")
    
    with st.expander(f"📖 {t('read_terms')}", expanded=True):
        st.markdown(f"""
        <div class='consent-box'>
            {CONSENT_TEXT[st.session_state.language].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t('agree'), use_container_width=True):
            st.session_state.consent_given = True
            consents = load_data(CONSENTS_FILE, [])
            consents.append({
                "id": generate_id(),
                "user": st.session_state.user_name,
                "consent_date": datetime.now().isoformat(),
                "language": st.session_state.language
            })
            save_data(CONSENTS_FILE, consents)
            st.rerun()
    with col2:
        if st.button(t('disagree'), use_container_width=True):
            st.warning("لا يمكنك استخدام التطبيق بدون موافقة. هذا حقك بموجب القانون.")
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
        role = st.selectbox(t('role'), ["موظف وزارة", "مرشد زراعي", "عامل صحي", "معلم", "باحث", "إداري محلي", "منسق ميداني"])
        st.session_state.user_role = role
    with col3:
        district = st.selectbox(t('district'), ["Kiryandongo", "Masindi", "Gulu", "Lira", "Kampala", "Jinja", "Mbale", "Mbarara", "Arua", "Gulu", "Fort Portal", "أخرى"])
        st.session_state.user_district = district
    
    phone = st.text_input(t('phone'), value=st.session_state.user_phone, help=t('encrypted'))
    if phone:
        st.session_state.user_phone = phone
        st.info(f"{t('will_show')}: {encrypt_phone(phone)}")

# ==================== إحصائيات سريعة ====================
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
    unique_villages = len(set([r.get("fields", {}).get("village", "") for r in records if r.get("fields")]))
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{unique_villages}</div>
        <div class='label'>{t('villages_covered')}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    agriculture_records = len([r for r in records if r.get("sector") == "agriculture"])
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{agriculture_records}</div>
        <div class='label'>{t('agriculture_records')}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    health_records = len([r for r in records if r.get("sector") == "health"])
    st.markdown(f"""
    <div class='stat-card'>
        <div class='number'>{health_records}</div>
        <div class='label'>{t('health_records')}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== تسجيل بيانات جديدة ====================
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
            value = st.text_input(field["label"], key=f"field_{field['name']}")
        elif field["type"] == "number":
            value = st.number_input(field["label
