import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from datetime import date

API_URL = "http://127.0.0.1:8000"


def show_profit_analytics():
    business_id = st.session_state.business_id

    st.title("📈 Profit Analytics")


    # ==================================
    # KPI CARDS
    # ==================================

    try:
        monthly = requests.get(
            f"{API_URL}/profit/monthly",
            params={
                "business_id": business_id
            }
        )

        if monthly.status_code == 200:
            monthly_df = pd.DataFrame(monthly.json())

            if not monthly_df.empty:

                total_revenue = monthly_df["revenue"].sum()
                total_expense = monthly_df["expense"].sum()
                total_profit = monthly_df["profit"].sum()

                margin = (
                    total_profit / total_revenue * 100
                    if total_revenue > 0 else 0
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "💰 Revenue",
                    f"₹{total_revenue:,.2f}"
                )

                col2.metric(
                    "💸 Expense",
                    f"₹{total_expense:,.2f}"
                )

                col3.metric(
                    "📈 Profit",
                    f"₹{total_profit:,.2f}"
                )

                col4.metric(
                    "📊 Margin %",
                    f"{margin:.2f}%"
                )

            else:
                st.info("No financial data available.")

        else:
            st.error(monthly.text)

    except Exception as e:
        st.error(str(e))

    st.divider()
    
    col1, col2 = st.columns(2)

    with col1:
        from_date = st.date_input(
            "From Date",
            value=date.today().replace(day=1)
        )

    with col2:
        to_date = st.date_input(
            "To Date",
            value=date.today()
        )

    st.divider()
    # ==================================
    # DAILY PROFIT
    # ==================================

    st.subheader("📅 Daily Profit Trend")

    daily_df = pd.DataFrame()

    try:
        daily = requests.get(
            f"{API_URL}/profit/daily",
            params={
                "business_id": business_id,
                "from_date": str(from_date),
                "to_date": str(to_date)
            }
        )

        if daily.status_code == 200:
            daily_df = pd.DataFrame(daily.json())

            if not daily_df.empty:
                fig = px.line(
                    daily_df,
                    x="date",
                    y="profit",
                    markers=True,
                    title="Daily Profit Trend"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            else:
                st.info("No Daily Profit Data")

        else:
            st.error(daily.text)

    except Exception as e:
        st.error(str(e))

    st.divider()

    # ==================================
    # WEEKLY PROFIT
    # ==================================

    st.subheader("📊 Weekly Profit Trend")

    try:
        weekly = requests.get(
            f"{API_URL}/profit/weekly",
            params={
                "business_id": business_id
            }
        )

        if weekly.status_code == 200:
            weekly_df = pd.DataFrame(weekly.json())

            if not weekly_df.empty:
                fig = px.area(
                    weekly_df,
                    x="week",
                    y="profit",
                    title="Weekly Profit"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            else:
                st.info("No Weekly Profit Data")

        else:
            st.error(weekly.text)

    except Exception as e:
        st.error(str(e))

    st.divider()

    # ==================================
    # MONTHLY PROFIT
    # ==================================

    st.subheader("📈 Monthly Revenue vs Expense vs Profit")

    monthly_df = pd.DataFrame()

    try:
        monthly = requests.get(
            f"{API_URL}/profit/monthly",
            params={
                "business_id": business_id
            }
        )

        if monthly.status_code == 200:
            monthly_df = pd.DataFrame(monthly.json())

            if not monthly_df.empty:
                fig = px.line(
                    monthly_df,
                    x="month",
                    y=[
                        "revenue",
                        "expense",
                        "profit"
                    ],
                    markers=True,
                    title="Monthly Financial Performance"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # ==================================
                # PIE CHART
                # ==================================

                st.subheader("💰 Revenue Distribution")

                pie_df = pd.DataFrame({
                    "Type": [
                        "Revenue",
                        "Expense",
                        "Profit"
                    ],
                    "Amount": [
                        total_revenue,
                        total_expense,
                        total_profit
                    ]
                })

                fig = px.pie(
                    pie_df,
                    names="Type",
                    values="Amount",
                    hole=0.5
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No Monthly Profit Data")

        else:
            st.error(monthly.text)

    except Exception as e:
        st.error(str(e))

    st.divider()

    # ==================================
    # YEARLY PROFIT
    # ==================================

    st.subheader("🏆 Yearly Profit Trend")

    try:
        yearly = requests.get(
            f"{API_URL}/profit/yearly",
            params={
                "business_id": business_id
            }
        )

        if yearly.status_code == 200:
            yearly_df = pd.DataFrame(yearly.json())

            if not yearly_df.empty:
                fig = px.bar(
                    yearly_df,
                    x="year",
                    y="profit",
                    title="Yearly Profit"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No Yearly Profit Data")

        else:
            st.error(yearly.text)

    except Exception as e:
        st.error(str(e))