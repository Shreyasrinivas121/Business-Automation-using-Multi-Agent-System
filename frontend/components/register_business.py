import streamlit as st
import requests


def show_register_business():

    st.title("🏢 Register New Business")

    business_name = st.text_input(
        "Business Name"
    )

    admin_username = st.text_input(
        "Admin Username"
    )

    email = st.text_input(
        "Email"
    )

    phone = st.text_input(
        "Phone Number"
    )

    address = st.text_area(
        "Business Address"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Register Business"
    ):

        payload = {
            "business_name": business_name,
            "admin_username": admin_username,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/register-business",
                json=payload
            )

            data = response.json()

            if response.status_code == 200:

                st.success(
                    data["message"]
                )

                st.success(
                    f"Business ID : {data['business_id']}"
                )

            else:

                st.error(
                    data["detail"]
                )

        except Exception as e:

            st.error(str(e))