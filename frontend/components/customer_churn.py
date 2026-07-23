import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"


def show_customer_churn():

    st.title("🔥 Customer Churn Prediction")

    response = requests.get(
        f"{API_URL}/customer-churn",
        params={
            "business_id":
            st.session_state.business_id
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
            "No customer data found."
        )
        return

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "High Risk",
        len(
            df[df["risk"] == "High"]
        )
    )

    c2.metric(
        "Medium Risk",
        len(
            df[df["risk"] == "Medium"]
        )
    )

    c3.metric(
        "Low Risk",
        len(
            df[df["risk"] == "Low"]
        )
    )

    st.divider()

    fig = px.pie(
        df,
        names="risk",
        title="Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    fig = px.bar(
        df,
        x="customer",
        y="days_since_last_purchase",
        color="risk",
        title="Days Since Last Purchase"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )