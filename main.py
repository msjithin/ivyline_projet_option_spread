import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from scipy.stats import norm
import streamlit as st
import debit_spread
import credit_spread
import intro
import next_step

st.sidebar.markdown(
    """
# Control Panel
"""
)
PAGES = {
    "Introduction": intro,
    "Debit Spread": debit_spread,
    "Credit Spread": credit_spread,
    "next step" : next_step
}
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()