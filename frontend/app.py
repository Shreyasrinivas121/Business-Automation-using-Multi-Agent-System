import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from io import BytesIO
from openpyxl import Workbook
import base64

from components.dashboard import show_dashboard
from components.products import show_products
from components.customers import show_customers
from components.billing import show_billing
from components.reports import show_reports
from components.stock_assistant import show_stock_assistant
from components.security import show_security
from components.staff import show_staff
from components.wholesalers import show_wholesalers
from components.procurement import show_procurement
from components.profit_analytics import show_profit_analytics
from components.demand_prediction import show_demand_prediction
from components.customer_loyalty import (
    show_customer_loyalty
)
from components.business_insights import (
    show_business_insights
)
from components.customer_churn import (
    show_customer_churn
)
from components.register_business import show_register_business
from components.about_project import show_about_project
 

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Business Automation AI",
    layout="wide"
)

def set_login_background():

    with open(
        "assets/login_bg.jpg",
        "rb"
    ) as image_file:

        encoded = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
            linear-gradient(
                rgba(0,0,0,0.55),
                rgba(0,0,0,0.55)
            ),
            url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        section[data-testid="stSidebar"] {{
            background-color:
            rgba(20,20,20,0.95);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )# ==================================
# SESSION STATE INIT
# ==================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "business_id" not in st.session_state:
    st.session_state.business_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    
if "page" not in st.session_state:
    st.session_state.page = "login"    
    
if "show_about" not in st.session_state:
    st.session_state.show_about = False    

# ==================================
# LOGIN PAGE
# ==================================

if not st.session_state.logged_in:

    if st.session_state.show_about:

        show_about_project()

        if st.button("⬅ Back to Login"):
            st.session_state.show_about = False
            st.rerun()

        st.stop()
    
    set_login_background()

    st.markdown(
    """
    <style>

    /* ==========================================
       PAGE
    ========================================== */

    .block-container{
        padding-top:35px;
    }

    header{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    /* ==========================================
       TITLE
    ========================================== */

    h1{
        color:white !important;
        font-weight:700;
    }

    h4{
        color:#57C6FF !important;
        font-weight:500;
    }

    /* ==========================================
       LABELS
    ========================================== */

    label{
        color:#EAF6FF !important;
        font-size:17px !important;
        font-weight:600 !important;
    }

    /* ==========================================
       TEXT INPUTS
    ========================================== */

    .stTextInput input{

        background:#081424 !important;

        color:white !important;

        border:2px solid #1EA7FF !important;

        border-radius:12px !important;

        height:50px !important;

        font-size:16px !important;

        padding-left:14px !important;
    }

    .stTextInput input::placeholder{

        color:#AFC6D8 !important;

        opacity:1 !important;
    }

    .stTextInput input:focus{

        border:2px solid #49C6FF !important;

        box-shadow:
            0 0 10px rgba(30,167,255,.45);

    }

    /* ==========================================
       PASSWORD EYE ICON
    ========================================== */

    button[kind="icon"]{

        color:#57C6FF !important;

    }

    /* ==========================================
       BUTTONS
    ========================================== */

    .stButton{

        display:flex;

        justify-content:center;

    }

    .stButton > button{

        width:70%;

        height:52px;

        border:none;

        border-radius:14px;

        font-size:18px;

        font-weight:bold;

        color:white;

        cursor:pointer;

        transition:all .25s ease;

        background:
            linear-gradient(
                90deg,
                #1EA7FF,
                #7B2CFF
            );
    }

    .stButton > button:hover{

        transform:translateY(-2px);

        box-shadow:
            0 0 20px rgba(30,167,255,.55);

    }

    /* ==========================================
       SUCCESS / ERROR
    ========================================== */

    .stAlert{

        border-radius:12px;

    }

    /* ==========================================
       REGISTER BUSINESS PAGE
    ========================================== */

    .stSelectbox div[data-baseweb="select"]{

        background:#081424;

        border-radius:10px;

    }

    .stNumberInput input{

        background:#081424 !important;

        color:white !important;

        border-radius:10px;

    }

    .stTextArea textarea{

        background:#081424 !important;

        color:white !important;

        border-radius:10px;

    }

    .stDateInput input{

        background:#081424 !important;

        color:white !important;

        border-radius:10px;

    }

    .stCheckbox{

        color:white;

    }

    </style>
    """,
    unsafe_allow_html=True
)

    left, center, right = st.columns([1.5,2,1.5])

    with center:

        st.markdown('<div class="login-marker"></div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align:center;font-size:70px;">
                🤖
            </div>

            <h1 style="text-align:center;color:white;margin-bottom:0;">
                Agent Operations Hub
            </h1>

            <h4 style="
                text-align:center;
                color:#46c3ff;
                margin-top:5px;
                margin-bottom:10px;">
                AI Powered Business Automation
            </h4>

            <hr style="
                border:2px solid #1ea7ff;
                width:120px;
                margin:auto;
                margin-bottom:25px;">
            """,
            unsafe_allow_html=True
        ) 

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )
    
# -------------------------------
# About Platform Button
# -------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 2, 1])

    with middle:

        if st.button(
        "📖 Learn About Platform",
        width="stretch"
    ):
            st.session_state.show_about = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 2, 1])

    with middle:

        login = st.button(
            "🚀 Login",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 2, 1])

    with middle:

        register = st.button(
            "🏢 Register Business",
            use_container_width=True
        )

    if login:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.logged_in = True
                st.session_state.role = data["role"]
                st.session_state.business_id = data["business_id"]
                st.session_state.username = data["username"]
                st.session_state.user_id = data["user_id"]

                st.rerun()

            else:

                st.error("Invalid Credentials")

        except Exception as e:

            st.error(f"Backend Error: {e}")

    if register:

        show_register_business()

    st.stop()
    
# ==================================
# SIDEBAR
# ==================================

st.sidebar.title(
    "Business Automation AI"
)

st.sidebar.success(
    f"Role : {st.session_state.role}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.business_id = None
    st.session_state.username = None
    st.session_state.user_id = None

    st.rerun()
# ==================================
# SECURITY ALERT INDICATOR
# ==================================

security_menu = "Security"

try:

    alerts = requests.get(
     "http://127.0.0.1:8000/security-alerts",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

    active_count = len(
        [
            alert
            for alert in alerts
            if alert["status"] == "Active"
        ]
    )

    if active_count > 0:

        security_menu = (
            f"🚨 Security ({active_count})"
        )

        st.sidebar.markdown(
            f"""
            <div style="
                color:red;
                font-size:20px;
                font-weight:bold;
                text-align:center;
                animation: blinker 1s linear infinite;
            ">
                🚨 {active_count} ACTIVE ALERTS
            </div>

            <style>
            @keyframes blinker {{
                50% {{
                    opacity: 0;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

except:
    security_menu = "Security"
    
# ==================================
# MENU
# ==================================

if st.session_state.role == "admin":

    menu = st.sidebar.radio(
        "Menu",
        [
        "Dashboard",
         "AI Insights",
        "Products",
        "Customers",
        "Billing",
        "Reports",
        "Wholesalers",
       "Procurement",
        security_menu,
        "Staff",
        "Profit Analytics",
        "Demand Prediction",
        "Customer Loyalty",
        "Customer Churn"
    ]
    )

else:

    menu = st.sidebar.radio(
        "Menu",
        [
            "Products",
            "Customers",
            "Billing",
            "Reports",
            "Stock Assistant"
        ]
    ) 
    
if menu == "Dashboard":
    show_dashboard()

elif menu == "Products":
    show_products()

elif menu == "Customers":
    show_customers()

elif menu == "Billing":
    show_billing()

elif menu == "Reports":
    show_reports()

elif menu == "Stock Assistant":
    show_stock_assistant()
    
elif menu == "Staff":

    show_staff()    

elif menu == "Wholesalers":

    show_wholesalers()
    
elif menu == "Procurement":

    show_procurement()    
        
elif "Security" in menu:

    show_security()    
    
elif menu == "Profit Analytics":

    show_profit_analytics()   
    
elif menu == "Demand Prediction":

    show_demand_prediction()   
    
elif menu == "Customer Loyalty":

    show_customer_loyalty()  
    
elif menu == "AI Insights":

    show_business_insights()   
    
elif menu == "Customer Churn":

    show_customer_churn()        