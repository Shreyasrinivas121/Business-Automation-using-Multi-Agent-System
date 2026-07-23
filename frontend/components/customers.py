import streamlit as st
import requests
import pandas as pd


def show_customers():

    st.title("👥 Customer Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "View Customers",
            "Add Customer",
            "Edit/Delete Customer"
        ]
    )

    # -----------------------
    # VIEW CUSTOMERS
    # -----------------------

    with tab1:

        try:

            customers = requests.get(
    "http://127.0.0.1:8000/customers",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

            st.dataframe(
                pd.DataFrame(customers),
                use_container_width=True
            )

        except Exception as e:

            st.error(str(e))

    # -----------------------
    # ADD CUSTOMER
    # -----------------------

    with tab2:

        name = st.text_input(
            "Customer Name"
        )

        phone = st.text_input(
            "Phone"
        )

        email = st.text_input(
            "Email"
        )

        address = st.text_input(
            "Address"
        )

        if st.button(
            "Add Customer"
        ):

            payload = {
                "business_id": st.session_state.business_id,
                "customer_name": name,
                "phone": phone,
                "email": email,
                "address": address
            }            
            try:

                response = requests.post(
                    "http://127.0.0.1:8000/customers",
                    json=payload
                )

                if response.status_code == 200:

                    requests.post(
                        "http://127.0.0.1:8000/activity-log",
                        json={
                            "user_id": st.session_state.user_id,
                            "business_id": st.session_state.business_id,
                            "action": f"{st.session_state.username} added customer {name}"
                        }
                    )

                    st.success(
                        "Customer Added"
                    )

                    st.rerun()

                else:

                    st.error(
                        response.text
                    )

            except Exception as e:

                st.error(
                    str(e)
                )
    # -----------------------
    # EDIT / DELETE CUSTOMER
    # -----------------------

    with tab3:

        try:

            customers = requests.get(
    "http://127.0.0.1:8000/customers",
    params={
        "business_id": st.session_state.business_id
    }
).json()

            customer_map = {
                f"{c['customer_id']} - {c['customer_name']}": c
                for c in customers
            }

            selected = st.selectbox(
                "Select Customer",
                list(customer_map.keys())
            )

            customer = customer_map[selected]

            name = st.text_input(
                "Customer Name",
                value=customer["customer_name"]
            )

            phone = st.text_input(
                "Phone",
                value=customer["phone"]
            )

            email = st.text_input(
                "Email",
                value=customer["email"]
            )

            address = st.text_input(
                "Address",
                value=customer["address"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Update Customer"
                ):

                    payload = {
                        "business_id": st.session_state.business_id,
                        "customer_name": name,
                        "phone": phone,
                        "email": email,
                        "address": address
                    }

                    response = requests.put(
                        f"http://127.0.0.1:8000/customers/{customer['customer_id']}",
                        json=payload
                    )

                    if response.status_code == 200:

                        st.success(
                            "Customer Updated"
                        )

                        st.rerun()

                    else:

                        st.error(
                            response.text
                        )

            with col2:

                if st.button(
                    "Delete Customer"
                ):

                    response = requests.delete(
                        f"http://127.0.0.1:8000/customers/{customer['customer_id']}"
                    )

                    if response.status_code == 200:

                        st.success(
                            "Customer Deleted"
                        )

                        st.rerun()

                    else:

                        st.error(
                            response.text
                        )

        except Exception as e:

            st.error(str(e))