import streamlit as st
import requests
import pandas as pd

from io import BytesIO


API_URL = "http://127.0.0.1:8000"


def download_excel(df, filename):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    output.seek(0)

    st.download_button(
        label=f"📥 Download {filename}",
        data=output,
        file_name=f"{filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def show_reports():

    st.title("📊 Reports Center")

    st.markdown(
        """
        Download detailed business reports
        in Excel format.
        """
    )

    st.divider()

    # ==================================
    # PRODUCT REPORT
    # ==================================

    st.subheader("📦 Product Report")

    try:

        products = requests.get(
    f"{API_URL}/products",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        product_df = pd.DataFrame(products)

        st.write(
            f"Records : {len(product_df)}"
        )

        download_excel(
            product_df,
            "Product_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # CUSTOMER REPORT
    # ==================================

    st.subheader("👥 Customer Report")

    try:

        customers = requests.get(
    f"{API_URL}/customers",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        customer_df = pd.DataFrame(customers)

        st.write(
            f"Records : {len(customer_df)}"
        )

        download_excel(
            customer_df,
            "Customer_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # BILLING REPORT
    # ==================================

    st.subheader("🧾 Billing Report")

    try:

        sales = requests.get(
    f"{API_URL}/sales-report",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        sales_df = pd.DataFrame([sales])
        
        st.write(
    f"Total Bills : {sales['total_bills']}"
)
        
        download_excel(
            sales_df,
            "Billing_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # STAFF REPORT
    # ==================================

    st.subheader("👨‍💼 Staff Report")

    try:

        staff = requests.get(
    f"{API_URL}/staff",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        staff_df = pd.DataFrame(staff)

        st.write(
            f"Records : {len(staff_df)}"
        )

        download_excel(
            staff_df,
            "Staff_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # WHOLESALER REPORT
    # ==================================

    st.subheader("🏭 Wholesaler Report")

    try:

        wholesalers = requests.get(
            f"{API_URL}/wholesalers"
        ).json()

        wholesaler_df = pd.DataFrame(
            wholesalers
        )

        st.write(
            f"Records : {len(wholesaler_df)}"
        )

        download_excel(
            wholesaler_df,
            "Wholesaler_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # PROCUREMENT REPORT
    # ==================================

    st.subheader("🚚 Procurement Report")

    try:

        orders = requests.get(
    f"{API_URL}/wholesaler-orders",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        orders_df = pd.DataFrame(
            orders
        )

        st.write(
            f"Records : {len(orders_df)}"
        )

        download_excel(
            orders_df,
            "Procurement_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # SECURITY REPORT
    # ==================================

    st.subheader("🔐 Security Alert Report")

    try:

        alerts = requests.get(
    f"{API_URL}/security-alerts",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        alerts_df = pd.DataFrame(
            alerts
        )

        st.write(
            f"Records : {len(alerts_df)}"
        )

        download_excel(
            alerts_df,
            "Security_Report"
        )

    except Exception as e:

        st.error(str(e))

    st.divider()

    # ==================================
    # BUSINESS SUMMARY
    # ==================================

    st.subheader("📈 Business Summary")

    try:

        summary = requests.get(
    f"{API_URL}/dashboard",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        summary_df = pd.DataFrame(
            [summary]
        )
        
        st.write(
    f"Revenue : ₹{summary['total_revenue']}"
)
        
        download_excel(
            summary_df,
            "Business_Summary"
        )

    except Exception as e:

        st.error(str(e))