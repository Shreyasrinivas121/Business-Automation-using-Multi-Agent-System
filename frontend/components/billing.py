# ==================================
# BILLING
# ==================================

import streamlit as st
import requests
import pandas as pd

from io import BytesIO
from openpyxl import Workbook


def show_billing():

    st.title("🧾 Generate Bill")

    customers = requests.get(
    "http://127.0.0.1:8000/customers",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

    products = requests.get(
    "http://127.0.0.1:8000/products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

    filtered_products = []
    seen = set()

    for product in products:

        if product["quantity"] <= 0:
            continue

        name = product["product_name"].lower()

        if name in seen:
            continue

        seen.add(name)
        filtered_products.append(product)

    products = filtered_products

    customer_names = [
        c["customer_name"]
        for c in customers
    ]

    selected_customer = st.selectbox(
        "Customer",
        customer_names
    )

    st.subheader("Products")

    bill_items = []

    for product in products:

        qty = st.number_input(
            f"{product['product_name']} (Stock: {product['quantity']})",
            min_value=0,
            key=f"qty_{product['product_id']}"
        )

        if qty > 0:

            bill_items.append(
                {
                    "product_id": product["product_id"],
                    "quantity": qty
                }
            )

    if st.button("Generate Bill"):

        customer_id = next(
            c["customer_id"]
            for c in customers
            if c["customer_name"] == selected_customer
        )

        payload = {
            "business_id": st.session_state.business_id,
            "customer_id": customer_id,
            "items": bill_items
        }

        try:

            result = requests.post(
                "http://127.0.0.1:8000/bills",
                json=payload
            )

            if result.status_code == 200:

                bill_data = result.json()

                requests.post(
                    "http://127.0.0.1:8000/activity-log",
                    json={
                        "user_id": st.session_state.user_id,
                        "business_id": st.session_state.business_id,
                        "action": (
                            f"{st.session_state.username} "
                            f"generated bill #{bill_data['bill_id']}"
                        )
                    }
                )

                st.success(
                    f"Bill #{bill_data['bill_id']} Generated Successfully"
                )

                st.markdown("---")

                st.subheader(
                    f"Invoice - Bill #{bill_data['bill_id']}"
                )

                st.write(
                    f"### Customer : {bill_data['customer_name']}"
                )

                # ==================================
                # LOYALTY DISCOUNT
                # ==================================

                if bill_data["loyalty_discount_percent"] > 0:

                    st.success(
                        f"""
👑 Loyalty Discount Applied

**Discount:** {bill_data['loyalty_discount_percent']}%

**Savings:** ₹{round(bill_data['discount_amount'], 2)}
"""
                    )

                invoice_df = pd.DataFrame(
                    bill_data["items"]
                )

                st.table(invoice_df)

                st.markdown("---")

                # ==================================
                # BILL SUMMARY
                # ==================================

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.metric(
                        "Subtotal",
                        f"₹{round(bill_data['subtotal'], 2)}"
                    )

                with c2:

                    st.metric(
                        "Loyalty Discount",
                        f"₹{round(bill_data['discount_amount'], 2)}"
                    )

                with c3:

                    st.metric(
                        "GST 18%",
                        f"₹{round(bill_data['tax'], 2)}"
                    )

                with c4:

                    st.metric(
                        "Grand Total",
                        f"₹{round(bill_data['grand_total'], 2)}"
                    )

                # ==================================
                # EXCEL INVOICE
                # ==================================

                wb = Workbook()
                ws = wb.active
                ws.title = "Invoice"

                ws.append(
                    [
                        "Product",
                        "Quantity",
                        "Price",
                        "Subtotal"
                    ]
                )

                for item in bill_data["items"]:

                    ws.append(
                        [
                            item["product_name"],
                            item["quantity"],
                            item["price"],
                            item["subtotal"]
                        ]
                    )

                ws.append([])

                ws.append(
                    [
                        "",
                        "",
                        "Subtotal",
                        bill_data["subtotal"]
                    ]
                )

                ws.append(
                    [
                        "",
                        "",
                        "Loyalty Discount",
                        f"-{bill_data['discount_amount']}"
                    ]
                )

                ws.append(
                    [
                        "",
                        "",
                        "GST 18%",
                        bill_data["tax"]
                    ]
                )

                ws.append(
                    [
                        "",
                        "",
                        "Grand Total",
                        bill_data["grand_total"]
                    ]
                )

                excel_file = BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                st.download_button(
                    label="📥 Download Invoice Excel",
                    data=excel_file,
                    file_name=f"invoice_{bill_data['bill_id']}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:

                st.error(result.text)

        except Exception as e:

            st.error(str(e))