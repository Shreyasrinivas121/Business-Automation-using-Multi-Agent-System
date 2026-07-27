# ==================================
# DASHBOARD
# ==================================

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils.ui import metric_card

def show_dashboard():

    st.title("🏢 Business Automation AI Dashboard")

    # ==================================
    # SECURITY ALERT BANNER
    # ==================================

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

            st.error(
                f"🚨 {active_count} Active Security Alert(s)"
            )

    except Exception as e:

        st.error(
            f"Security Alert Error: {e}"
        )

    # ==================================
    # BUSINESS METRICS
    # ==================================

    cash = requests.get(
        f"http://127.0.0.1:8000/cash-balance/{st.session_state.business_id}"
    ).json()

    inventory = requests.get(
        "http://127.0.0.1:8000/inventory-value",
        params={
            "business_id":
            st.session_state.business_id
        }
    ).json()

    business = requests.get(
        f"http://127.0.0.1:8000/business-value/{st.session_state.business_id}"
    ).json()
    
    from utils.ui import metric_card
    
    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "💰 Cash Balance",
            f"₹{cash['cash_balance']}"
        )

    with c2:
        metric_card(
        "📦 Inventory Value",
        f"₹{inventory['inventory_value']}"
    )

    with c3:
        metric_card(
            "🏦 Business Value",
            f"₹{business['business_value']}"
        )

    st.divider()

    # ==================================
    # KPI
    # ==================================

    try:

        report = requests.get(
            "http://127.0.0.1:8000/sales-report",
            params={
                "business_id":
                st.session_state.business_id
            }
        ).json()

        from utils.ui import metric_card

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card(
                "💰 Revenue",
                f"₹{report['total_revenue']}"
            )

        with c2:
            metric_card(
                "🧾 Bills",
                report["total_bills"]
            )

        with c3:
            metric_card(
                "👥 Customers",
                report["total_customers"]
            )

        with c4:
            metric_card(
                "📦 Products",
                report["total_products"]
            )

    except Exception as e:

        st.error(
            f"Sales Report Error: {e}"
        )

    st.divider()

    # ==================================
    # LOW STOCK
    # ==================================

    st.subheader("⚠️ Low Stock Alerts")

    try:

        low_stock = requests.get(
    "http://127.0.0.1:8000/low-stock",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        if low_stock:

            for item in low_stock:

                st.warning(
                    f"{item['product_name']} - {item['quantity']} left"
                )

        else:

            st.success(
                "No Low Stock Products"
            )

    except:

        st.error(
            "Low Stock API Error"
        )

    st.divider()

    # ==================================
    # INVENTORY ANALYTICS
    # ==================================

    try:

        products = requests.get(
    "http://127.0.0.1:8000/products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        df = pd.DataFrame(products)

        st.subheader(
            "📦 Inventory Analytics"
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                df,
                x="product_name",
                y="quantity",
                title="Inventory Quantity"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        with col2:

            fig = px.pie(
                df,
                names="product_name",
                values="quantity",
                title="Inventory Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except:

        st.error(
            "Inventory Analytics Error"
        )

    st.divider()

    # ==================================
    # SALES TREND + TOP PRODUCTS
    # ==================================

    try:

        trend = requests.get(
    "http://127.0.0.1:8000/sales-trend",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        top_products = requests.get(
    "http://127.0.0.1:8000/top-products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        c1, c2 = st.columns(2)

        with c1:

            trend_df = pd.DataFrame(trend)

            fig = px.line(
                trend_df,
                x="date",
                y="revenue",
                markers=True,
                title="Sales Trend"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with c2:

            top_df = pd.DataFrame(top_products)

            fig = px.bar(
                top_df,
                x="product",
                y="sold",
                title="Top Selling Products"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    except:

        st.error(
            "Analytics Error"
        )

    st.divider()

    # ==================================
    # AI ASSISTANT
    # ==================================

    st.subheader("🤖 AI Assistant")

    question = st.text_input(
        "Ask Business Question",
        key="admin_ai"
    )

    if st.button(
        "Ask AI",
        key="admin_ai_btn"
    ):

        try:

            result = requests.post(
                "http://127.0.0.1:8000/ask-ai",
                json={
                    "question": question,
                    "business_id": st.session_state.business_id
                }
            ).json()

            st.success(
                result["answer"]
            )

        except:

            st.error(
                "AI Error"
            )

    st.divider()

    # ==================================
    # ACTIVITY LOGS
    # ==================================

    st.subheader("📝 Activity Logs")

    try:

        logs = requests.get(
    "http://127.0.0.1:8000/activity-logs",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        logs_df = pd.DataFrame(logs)

        st.dataframe(
            logs_df,
            width="stretch"
        )

    except:

        st.error(
            "Activity Log Error"
        )