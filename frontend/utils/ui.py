import streamlit as st

def metric_card(title, value):

    st.markdown(
        f"""
<div style="
background:#87CEEB;
padding:20px;
border-radius:18px;
border:1px solid #2F3C4E;
text-align:center;
height:140px;
box-shadow:0px 5px 5px rgba(0,0,0,.35);
">

<div style="
font-size:16px;
color:#000000;
font-weight:600;
margin-bottom:15px;
">
{title}
</div>

<div style="
font-size:34px;
font-weight:700;
color:white;
">
{value}
</div>

</div>
""",
        unsafe_allow_html=True
    )