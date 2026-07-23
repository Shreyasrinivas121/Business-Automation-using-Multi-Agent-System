import streamlit as st
import requests


def show_stock_assistant():

    st.title(
        "🤖 Stock Assistant"
    )

    question = st.text_input(
        "Ask stock related question"
    )

    if st.button(
        "Ask"
    ):

        try:

            result = requests.post(
                "http://127.0.0.1:8000/ask-ai",
                json={
                    "question": question
                }
            ).json()

            st.success(
                result["answer"]
            )

        except Exception as e:

            st.error(
                str(e)
            )