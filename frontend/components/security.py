import streamlit as st
import requests


def show_security():

    st.title("🔐 Security Center")

    if "spoken_alerts" not in st.session_state:

        st.session_state.spoken_alerts = set()

    try:

        alerts = requests.get(
    "http://127.0.0.1:8000/security-alerts",
    params={
        "business_id":
        st.session_state.business_id
    }
).json()

        active_alerts = [
            alert
            for alert in alerts
            if alert["status"] == "Active"
        ]

        if not active_alerts:

            st.success(
                "No Active Security Alerts"
            )

            st.components.v1.html(
                """
                <script>
                window.speechSynthesis.cancel();
                </script>
                """,
                height=0
            )

            return

        for alert in active_alerts:

            st.error(
                f"🚨 {alert['alert_type']}"
            )

            st.write(
                alert["message"]
            )

            if (
                alert.get("voice_message")
                and alert["alert_id"]
                not in st.session_state.spoken_alerts
            ):

                st.session_state.spoken_alerts.add(
                    alert["alert_id"]
                )

                st.components.v1.html(
                    f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance(
                        "{alert['voice_message']}"
                    );
                    window.speechSynthesis.speak(msg);
                    </script>
                    """,
                    height=0
                )

            st.write(
                f"Severity : {alert['severity']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Yes I Know",
                    key=f"resolve_{alert['alert_id']}"
                ):

                    response = requests.post(
                        f"http://127.0.0.1:8000/resolve-alert/{alert['alert_id']}"
                    )

                    if response.status_code == 200:

                        st.components.v1.html(
                            """
                            <script>
                            window.speechSynthesis.cancel();
                            </script>
                            """,
                            height=0
                        )

                        if (
                            alert["alert_id"]
                            in st.session_state.spoken_alerts
                        ):

                            st.session_state.spoken_alerts.remove(
                                alert["alert_id"]
                            )

                        st.success(
                            "Alert Resolved"
                        )

                        st.rerun()

                    else:

                        st.error(
                            response.text
                        )

            with col2:

                if st.button(
                    "🔍 Take Action",
                    key=f"action_{alert['alert_id']}"
                ):

                    st.info(
                        "Open Activity Logs to investigate this alert."
                    )

            st.divider()

    except Exception as e:

        st.error(
            str(e)
        )