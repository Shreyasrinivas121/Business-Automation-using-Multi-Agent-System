import streamlit as st
import requests


def show_stock_assistant():

    st.title("🤖 AI Assistant")

    question = st.text_input("Ask your business question")

    if st.button("Ask AI"):

        payload = {
            "question": question,
            "business_id": st.session_state.business_id
        }

        st.write("Payload Sent:", payload)

        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask-ai",
                json=payload
            )

            st.write("Status Code:", response.status_code)
            st.write("Response:", response.text)

            if response.status_code == 200:
                st.success(response.json()["answer"])
            else:
                st.error(response.text)

        except Exception as e:
            st.exception(e)