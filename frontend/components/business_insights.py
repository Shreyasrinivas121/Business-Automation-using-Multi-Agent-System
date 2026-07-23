import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_business_insights():

    st.title("🤖 AI Business Insights")

    response = requests.get(
        f"{API_URL}/business-insights",
        params={
            "business_id":
            st.session_state.business_id
        }
    )

    if response.status_code != 200:

        st.error(response.text)
        return

    insights = response.json()

    if not insights:

        st.info(
            "No insights available."
        )
        return

    for insight in insights:

        if insight["type"] == "success":

            st.success(
                insight["message"]
            )

        elif insight["type"] == "warning":

            st.warning(
                insight["message"]
            )

        elif insight["type"] == "danger":

            st.error(
                insight["message"]
            )

        else:

            st.info(
                insight["message"]
            )