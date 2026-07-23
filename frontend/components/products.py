# ==================================
# PRODUCTS
# ==================================
import streamlit as st
import requests
import pandas as pd

def show_products():

    st.title("📦 Product Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "View Products",
            "Add Product",
            "Edit Product"
        ]
    )

    # -----------------------
    # VIEW PRODUCTS
    # -----------------------

    with tab1:

        try:

            products = requests.get(
    "http://127.0.0.1:8000/products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

            df = pd.DataFrame(products)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.subheader("Delete Product")

            product_options = {
                f"{p['product_id']} - {p['product_name']}":
                p["product_id"]
                for p in products
            }

            selected_product = st.selectbox(
                "Select Product",
                list(product_options.keys())
            )

            if st.button(
                "Delete Product",
                key="delete_product"
            ):

                product_id = product_options[
                    selected_product
                ]

                response = requests.delete(
                    f"http://127.0.0.1:8000/products/{product_id}"
                )

                if response.status_code == 200:

                    st.success(
                        "Product Deleted Successfully"
                    )

                    st.rerun()

                else:

                    st.error(response.text)

        except Exception as e:

            st.error(str(e))
            
        # -----------------------
    # ADD PRODUCT
    # -----------------------

    with tab2:

        name = st.text_input(
            "Product Name"
        )

        category = st.text_input(
            "Category"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1
        )

        price = st.number_input(
            "Price",
            min_value=0.0
        )

        reorder = st.number_input(
            "Reorder Level",
            min_value=1
        )

        if st.button(
            "Add Product"
        ):

            payload = {
                "business_id": st.session_state.business_id,
                "product_name": name,
                "category": category,
                "quantity": quantity,
                "price": price,
                "reorder_level": reorder
            }

            response = requests.post(
                "http://127.0.0.1:8000/products",
                json=payload
            )

            if response.status_code == 200:

                requests.post(
                   "http://127.0.0.1:8000/activity-log",
                   json={
                         "user_id": st.session_state.user_id,
                         "business_id": st.session_state.business_id,
                         "action": f"{st.session_state.username} added product {name}"
        }
    )

                st.success(
                    "Product Added Successfully"
    )

                st.rerun()

            else:

                st.error(
                    response.text
                )        
    # -----------------------
    # EDIT PRODUCT
    # -----------------------

    with tab3:

        st.subheader(
            "Edit Product"
        )

        try:

            products = requests.get(
    "http://127.0.0.1:8000/products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()
            product_map = {
                f"{p['product_id']} - {p['product_name']}": p
                for p in products
            }

            selected = st.selectbox(
                "Select Product",
                list(product_map.keys()),
                key="edit_product"
            )

            product = product_map[selected]

            name = st.text_input(
                "Product Name",
                value=product["product_name"]
            )

            category = st.text_input(
                "Category",
                value=product["category"]
            )

            quantity = st.number_input(
                "Quantity",
                value=int(product["quantity"])
            )

            price = st.number_input(
                "Price",
                value=float(product["price"])
            )

            reorder = st.number_input(
                "Reorder Level",
                value=int(product["reorder_level"])
            )

            if st.button(
                "Update Product"
            ):

                payload = {
                    "business_id": st.session_state.business_id,
                    "product_name": name,
                    "category": category,
                    "quantity": quantity,
                    "price": price,
                    "reorder_level": reorder
                }

                response = requests.put(
                    f"http://127.0.0.1:8000/products/{product['product_id']}",
                    json=payload
                )

                if response.status_code == 200:

                    st.success(
                        "Product Updated Successfully"
                    )

                    st.rerun()

                else:

                    st.error(
                        response.text
                    )

        except Exception as e:

            st.error(str(e))