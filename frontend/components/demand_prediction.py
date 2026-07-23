import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"


def show_demand_prediction():

    st.title("📦 AI Demand Prediction Dashboard")

    business_id = st.session_state.business_id

    try:

        response = requests.get(
            f"{API_URL}/demand-predictions",
            params={
                "business_id": business_id
            }
        )

        if response.status_code != 200:
            st.error(response.text)
            return

        df = pd.DataFrame(response.json())

    except Exception as e:
        st.error(str(e))
        return

    if df.empty:
        st.info("No Prediction Data Available")
        return

    # ====================================================
    # KPI CARDS
    # ====================================================

    total_products = len(df)

    high_risk = len(
        df[df["risk"] == "High"]
    )

    medium_risk = len(
        df[df["risk"] == "Medium"]
    )

    low_risk = len(
        df[df["risk"] == "Low"]
    )

    orders_required = len(
        df[df["recommended_order"] > 0]
    )

    avg_coverage = round(
        df["coverage_days"].mean(),
        1
    )

    forecast_total = int(
        df["forecast_30_days"].sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📦 Products",
        total_products
    )

    c2.metric(
        "🔴 High Risk",
        high_risk
    )

    c3.metric(
        "🛒 Orders Required",
        orders_required
    )

    c4.metric(
        "📈 Forecast Demand",
        forecast_total
    )

    st.divider()

    # ====================================================
    # BUSINESS HEALTH
    # ====================================================

    st.subheader("📊 Business Health Indicators")

    inventory_score = max(
        0,
        min(
            100,
            int(avg_coverage * 5)
        )
    )

    demand_score = max(
        0,
        min(
            100,
            int(forecast_total / max(total_products, 1))
        )
    )

    procurement_score = max(
        0,
        100 - high_risk * 20
    )

    stock_score = max(
        0,
        int(low_risk / max(total_products, 1) * 100)
    )

    def create_gauge(title, value):

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,

                title={
                    "text": title
                },

                gauge={

                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "darkblue"
                    },

                    "steps": [

                        {
                            "range": [0, 40],
                            "color": "#ffcccc"
                        },

                        {
                            "range": [40, 70],
                            "color": "#ffe699"
                        },

                        {
                            "range": [70, 100],
                            "color": "#b6d7a8"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            height=260,
            margin=dict(
                l=20,
                r=20,
                t=40,
                b=20
            )
        )

        return fig

    g1, g2, g3, g4 = st.columns(4)

    with g1:

        st.plotly_chart(
            create_gauge(
                "Inventory",
                inventory_score
            ),
            use_container_width=True
        )

    with g2:

        st.plotly_chart(
            create_gauge(
                "Demand",
                demand_score
            ),
            use_container_width=True
        )

    with g3:

        st.plotly_chart(
            create_gauge(
                "Procurement",
                procurement_score
            ),
            use_container_width=True
        )

    with g4:

        st.plotly_chart(
            create_gauge(
                "Stock Health",
                stock_score
            ),
            use_container_width=True
        )

    st.divider()
    
    # ====================================================
    # RISK DISTRIBUTION & STOCK STATUS
    # ====================================================

    left, right = st.columns(2)

    # -------------------------------
    # Risk Distribution
    # -------------------------------

    with left:

        st.subheader("🔴 Risk Distribution")

        risk_df = (
            df.groupby("risk")
            .size()
            .reset_index(name="Products")
        )

        fig = px.pie(
            risk_df,
            names="risk",
            values="Products",
            hole=0.60,
            color="risk",
            color_discrete_map={
                "High": "#EF4444",
                "Medium": "#F59E0B",
                "Low": "#10B981"
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------------
    # Stock Status
    # -------------------------------

    with right:

        st.subheader("📦 Stock Status")

        status_df = (
            df.groupby("status")
            .size()
            .reset_index(name="Products")
        )

        fig = px.pie(
            status_df,
            names="status",
            values="Products",
            hole=0.60
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # RECOMMENDED PROCUREMENT
    # ====================================================

    st.subheader("🛒 Recommended Procurement")

    procurement_df = df.sort_values(
        by="recommended_order",
        ascending=True
    )

    fig = px.bar(
        procurement_df,
        x="recommended_order",
        y="product",
        orientation="h",
        color="risk",
        text="recommended_order",
        color_discrete_map={
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Recommended Quantity",
        yaxis_title="",
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ====================================================
    # INVENTORY COVERAGE & DEMAND FORECAST
    # ====================================================

    left, right = st.columns(2)

    # -------------------------------
    # Inventory Coverage
    # -------------------------------

    with left:

        st.subheader("📈 Inventory Coverage")

        fig = px.line(
            df.sort_values("coverage_days"),
            x="product",
            y="coverage_days",
            markers=True
        )

        fig.update_layout(
            height=420,
            xaxis_title="Product",
            yaxis_title="Coverage Days"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------------
    # Demand Forecast
    # -------------------------------

    with right:

        st.subheader("🌳 30-Day Demand Forecast")

        fig = px.treemap(
            df,
            path=["product"],
            values="forecast_30_days",
            color="forecast_30_days",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # TOP PRODUCTS TO REORDER
    # ====================================================

    st.subheader("🏆 Top Products To Reorder")

    top_df = (
        df.sort_values(
            "recommended_order",
            ascending=False
        )
        .head(10)
    )

    fig = px.funnel(
        top_df,
        x="recommended_order",
        y="product",
        color="risk",
        color_discrete_map={
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()    # ====================================================
    # AI PROCUREMENT RECOMMENDATIONS
    # ====================================================

    st.subheader("🤖 AI Suggested Procurement Orders")

    order_df = (
        df[df["recommended_order"] > 0]
        .sort_values(
            "recommended_order",
            ascending=False
        )
    )

    if order_df.empty:

        st.success(
            "✅ All products have sufficient stock."
        )

    else:

        for _, row in order_df.iterrows():

            with st.container():

                left, right = st.columns([5, 1])

                # -----------------------------
                # Left Side
                # -----------------------------
                with left:

                    st.markdown(
                        f"""
### 📦 {row['product']}

**Risk Level:** {row['risk']}

**Current Stock:** {row['current_stock']}

**Forecast (30 Days):** {row['forecast_30_days']}

**Coverage:** {row['coverage_days']} Days

**Recommended Order:** **{row['recommended_order']} Units**

**🤖 AI Reason:**

{row['reason']}
"""
                    )

                # -----------------------------
                # Right Side
                # -----------------------------
                with right:

                    suppliers_response = requests.get(
                        f"{API_URL}/product-suppliers/{int(row['product_id'])}"
                    )

                    suppliers = []

                    if suppliers_response.status_code == 200:
                        suppliers = suppliers_response.json()

                    if suppliers:

                        supplier_map = {
                            f"{s['wholesaler_name']} (₹{s['purchase_price']})":
                            s["wholesaler_id"]
                            for s in suppliers
                        }

                        selected_supplier = st.selectbox(
                            "Supplier",
                            list(supplier_map.keys()),
                            key=f"supplier_{row['product_id']}"
                        )

                        cheapest = min(
                            suppliers,
                            key=lambda x: x["purchase_price"]
                        )

                        st.success(
                            f"""
⭐ Recommended Supplier

{cheapest['wholesaler_name']}

Lowest Price:
₹{cheapest['purchase_price']} per unit
"""
                        )

                        if st.button(
                            "Create Order",
                            key=f"order_{row['product_id']}"
                        ):

                            create = requests.post(
                                f"{API_URL}/create-suggested-order",
                                params={
                                    "product_id": int(row["product_id"]),
                                    "wholesaler_id": supplier_map[selected_supplier],
                                    "quantity": int(row["recommended_order"])
                                }
                            )

                            if create.status_code == 200:

                                st.success(
                                    f"Order Created for {row['product']}"
                                )

                            else:

                                st.error(create.text)

                    else:

                        st.warning("No suppliers available.")

            st.divider()
    # ====================================================
    # PRODUCT RISK TABLE
    # ====================================================

    st.subheader("📋 Product Risk Assessment")

    display_df = df.copy()

    display_df = display_df.rename(
        columns={
            "product": "Product",
            "current_stock": "Current Stock",
            "daily_sales_rate": "Daily Sales",
            "forecast_7_days": "7 Day Forecast",
            "forecast_30_days": "30 Day Forecast",
            "coverage_days": "Coverage (Days)",
            "recommended_order": "Recommended Order",
            "risk": "Risk",
            "status": "Status"
        }
    )

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    st.success(
        "✅ Demand prediction completed successfully."
    )

    # ====================================================
    # SMART DISCOUNT AGENT
    # ====================================================

    st.divider()

    st.subheader("🏷️ Smart Discount Recommendations")

    discount_df = df[df["discount"] > 0]

    if discount_df.empty:

        st.info("No discount recommendations available.")

    else:

        for _, row in discount_df.iterrows():

            st.warning(
                f"""
📦 {row['product']}

Suggested Discount:
{row['discount']}%

Current Stock:
{row['current_stock']}

30 Day Forecast:
{row['forecast_30_days']}

Reason:
{row['discount_reason']}
"""
            )

            if st.button(
                f"Apply {row['discount']}% Discount",
                key=f"discount_{row['product_id']}"
            ):

                response = requests.post(
                    f"{API_URL}/apply-discount",
                    params={
                        "product_id": int(row["product_id"]),
                        "discount": float(row["discount"])
                    }
                )

                if response.status_code == 200:

                    st.success("Discount Applied Successfully")
                    st.rerun()

                else:

                    st.error(response.text)