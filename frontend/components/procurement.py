import streamlit as st
import requests


def show_procurement():

    st.title("📦 Procurement Center")

    try:

        orders = requests.get(
    "http://127.0.0.1:8000/wholesaler-orders",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        if not orders:

            st.success(
                "No Procurement Orders Found"
            )

            return

        pending_orders = [
            order
            for order in orders
            if order["status"] == "Pending"
        ]

        approved_orders = [
            order
            for order in orders
            if order["status"] == "Approved"
        ]

        rejected_orders = [
            order
            for order in orders
            if order["status"] == "Rejected"
        ]

        tab1, tab2, tab3 = st.tabs(
            [
                "📦 Pending Orders",
                "✅ Approved Orders",
                "❌ Rejected Orders"
            ]
        )

        # ==========================
        # PENDING
        # ==========================

        with tab1:

            if not pending_orders:

                st.success(
                    "No Pending Orders"
                )

            for order in pending_orders:

                st.warning(
                    f"📦 Purchase Order #{order['order_id']}"
                )

                st.write(
                    f"**Product :** {order['product_name']}"
                )

                st.write(
                    f"**Supplier :** {order['wholesaler_name']}"
                )

                st.write(
                    f"**Unit Price :** ₹{order['purchase_price']}"
                )

                st.write(
                    f"**Quantity :** {order['quantity']}"
                )

                st.write(
                    f"**Total Cost :** ₹{order['total_cost']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve",
                        key=f"approve_{order['order_id']}"
                    ):

                        response = requests.post(
                            f"http://127.0.0.1:8000/approve-order/{order['order_id']}"
                        )

                        if response.status_code == 200:

                            st.success(
                                "Order Approved"
                            )

                            st.rerun()

                        else:

                            st.error(
                                response.text
                            )

                with col2:

                    if st.button(
                        "❌ Reject",
                        key=f"reject_{order['order_id']}"
                    ):

                        response = requests.post(
                            f"http://127.0.0.1:8000/reject-order/{order['order_id']}"
                        )

                        if response.status_code == 200:

                            st.success(
                                "Order Rejected"
                            )

                            st.rerun()

                        else:

                            st.error(
                                response.text
                            )

                st.divider()

        # ==========================
        # APPROVED
        # ==========================

        with tab2:

            if not approved_orders:

                st.info(
                    "No Approved Orders"
                )

            for order in approved_orders:

                st.success(
                    f"✅ Approved Order #{order['order_id']}"
                )

                st.write(
                    f"**Product :** {order['product_name']}"
                )

                st.write(
                    f"**Supplier :** {order['wholesaler_name']}"
                )

                st.write(
                    f"**Quantity :** {order['quantity']}"
                )

                st.write(
                    f"**Total Cost :** ₹{order['total_cost']}"
                )

                st.divider()

        # ==========================
        # REJECTED
        # ==========================

        with tab3:

            if not rejected_orders:

                st.info(
                    "No Rejected Orders"
                )

            for order in rejected_orders:

                st.error(
                    f"❌ Rejected Order #{order['order_id']}"
                )

                st.write(
                    f"**Product :** {order['product_name']}"
                )

                st.write(
                    f"**Supplier :** {order['wholesaler_name']}"
                )

                st.write(
                    f"**Quantity :** {order['quantity']}"
                )

                st.write(
                    f"**Total Cost :** ₹{order['total_cost']}"
                )

                if st.button(
                    "✅ Approve Anyway",
                    key=f"approve_rejected_{order['order_id']}"
                ):

                    response = requests.post(
                        f"http://127.0.0.1:8000/approve-order/{order['order_id']}"
                    )

                    if response.status_code == 200:

                        st.success(
                            "Rejected Order Approved"
                        )

                        st.rerun()

                st.divider()

    except Exception as e:

        st.error(
            str(e)
        )