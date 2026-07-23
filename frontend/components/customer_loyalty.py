import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"


def show_customer_loyalty():

    st.title("👑 Customer Loyalty Agent")

    business_id = st.session_state.business_id

    response = requests.get(
        f"{API_URL}/customer-loyalty",
        params={
            "business_id": business_id
        }
    )

    if response.status_code != 200:

        st.error(response.text)
        return

    df = pd.DataFrame(
        response.json()
    )

    if df.empty:

        st.info(
            "No Customer Data Found"
        )
        return

    # =========================
    # KPI CARDS
    # =========================

    total_customers = len(df)

    platinum = len(
        df[df["tier"] == "Platinum"]
    )

    gold = len(
        df[df["tier"] == "Gold"]
    )

    silver = len(
        df[df["tier"] == "Silver"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Customers",
        total_customers
    )

    c2.metric(
        "Platinum",
        platinum
    )

    c3.metric(
        "Gold",
        gold
    )

    c4.metric(
        "Silver",
        silver
    )

    st.divider()

    # =========================
    # TIER DISTRIBUTION
    # =========================

    st.subheader(
        "🏆 Loyalty Distribution"
    )

    fig = px.pie(
        df,
        names="tier",
        hole=0.60
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =========================
    # TOP CUSTOMERS
    # =========================

    st.subheader(
        "💰 Top Customers"
    )

    fig = px.bar(
        df.head(10),
        x="customer",
        y="total_spent",
        color="tier",
        text="total_spent"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =========================
    # CUSTOMER TABLE
    # =========================

    st.subheader(
        "📋 Loyalty Report"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )