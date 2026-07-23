import streamlit as st
import requests
import pandas as pd


def show_staff():

    st.title(
        "👨‍💼 Staff Management"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "View Staff",
            "Add Staff",
            "Delete Staff"
        ]
    )

    # =====================
    # VIEW STAFF
    # =====================

    with tab1:

        try:

            staff = requests.get(
    "http://127.0.0.1:8000/staff",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

            df = pd.DataFrame(staff)

            if "password_hash" in df.columns:

                df = df.drop(
                    columns=["password_hash"]
                )

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:

            st.error(
                str(e)
            )

    # =====================
    # ADD STAFF
    # =====================

    with tab2:

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Create Staff"
        ):

            payload = {
                "username": username,
                "email": email,
                "password": password,
                "business_id": st.session_state.business_id
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/staff",
                    json=payload
                )

                if response.status_code == 200:

                    st.success(
                        "Staff Created Successfully"
                    )

                    st.rerun()

                else:

                    st.error(
                        response.text
                    )

            except Exception as e:

                st.error(str(e))

    # =====================
    # DELETE STAFF
    # =====================

    with tab3:

        try:

            staff = requests.get(
    "http://127.0.0.1:8000/staff",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

            if len(staff) == 0:

                st.info(
                    "No Staff Found"
                )

            else:

                staff_map = {
                    f"{s['id']} - {s['username']}":
                    s["id"]
                    for s in staff
                }

                selected_staff = st.selectbox(
                    "Select Staff",
                    list(staff_map.keys())
                )

                if st.button(
                    "Delete Staff"
                ):

                    staff_id = staff_map[
                        selected_staff
                    ]

                    response = requests.delete(
    f"http://127.0.0.1:8000/staff/{staff_id}",
    params={
        "business_id":
        st.session_state.business_id
    }
)

                    if response.status_code == 200:

                        st.success(
                            "Staff Deleted Successfully"
                        )

                        st.rerun()

                    else:

                        st.error(
                            response.text
                        )

        except Exception as e:

            st.error(str(e))