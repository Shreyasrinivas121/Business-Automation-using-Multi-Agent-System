import streamlit as st
from utils.ui import metric_card

metric_card(
    title="Revenue",
    value="₹12,500",
    icon="💰",
    growth=12.5
)