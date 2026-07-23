import streamlit as st
import requests
import pandas as pd


def show_wholesalers():

    st.title("🏭 Wholesaler Management")

    tab1, tab2 = st.tabs(
        [
            "View Wholesalers",
            "Add Wholesaler"
        ]
    )

    # ==================================
    # VIEW WHOLESALERS
    # ==================================

    with tab1:

        try:

            wholesalers = requests.get(
                "http://127.0.0.1:8000/wholesalers"
            ).json()

            if wholesalers:

                df = pd.DataFrame(
                    wholesalers
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No Wholesalers Found"
                )

        except Exception as e:

            st.error(
                str(e)
            )

    # ==================================
    # ADD WHOLESALER
    # ==================================

    with tab2:

        with st.form(
            "add_wholesaler_form"
        ):

            wholesaler_name = st.text_input(
                "Wholesaler Name"
            )

            product_name = st.text_input(
                "Product Name"
            )

            purchase_price = st.number_input(
                "Purchase Price",
                min_value=0.0,
                step=1.0
            )

            available_quantity = st.number_input(
                "Available Quantity",
                min_value=0,
                step=1
            )

            submitted = st.form_submit_button(
                "Add Wholesaler"
            )

            if submitted:

                payload = {
                    "wholesaler_name":
                        wholesaler_name,

                    "product_name":
                        product_name,

                    "purchase_price":
                        purchase_price,

                    "available_quantity":
                        available_quantity
                }

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/wholesalers",
                        json=payload
                    )

                    if response.status_code == 200:

                        st.success(
                            f"{wholesaler_name} added successfully"
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