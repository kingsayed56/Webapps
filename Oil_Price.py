import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import requests
import plotly.express as px

# ----- Constants -----
EIA_API_KEY = "N0jptJHNjB4mo10RnKdULgFcfr4wMQzTGl6w5PQC"
# EIA_SERIES_ID = "PET.RWTC.D"  # WTI Spot Price (Daily)

# ----- Functions -----


def calculate_npv(oil_price, capex, opex_per_bbl, production_rate, years, discount_rate):
    days_per_year = 365
    annual_production = production_rate * days_per_year
    annual_revenue = oil_price * annual_production
    annual_opex = opex_per_bbl * annual_production
    annual_cash_flow = annual_revenue - annual_opex
    cash_flows = [-capex] + [annual_cash_flow] * years
    npv = npf.npv(discount_rate / 100, cash_flows)

    return {
        "Annual Production (bbl)": annual_production,
        "Annual Revenue ($)": annual_revenue,
        "Annual OPEX ($)": annual_opex,
        "Annual Cash Flow ($)": annual_cash_flow,
        "NPV ($)": npv
    }

# ----- Streamlit UI -----

st.set_page_config(page_title="Oil Price Impact Calculator", layout="centered")

st.title("🛢️ Oil Price Impact Calculator")

with st.sidebar:
    st.header("Project Inputs")
    capex = st.number_input("CAPEX ($)", value=10_000_000, step=500_000)
    opex = st.number_input("OPEX ($/bbl)", value=15.0)
    production = st.number_input("Production Rate (bbl/day)", value=1000)
    years = st.slider("Project Life (Years)", 1, 20, 5)
    discount = st.slider("Discount Rate (%)", 5, 20, 10)
    oil_price = st.slider("Oil Price ($/bbl)", 30, 150, 80)

# ----- NPV Calculation -----

results = calculate_npv(
    oil_price=oil_price,
    capex=capex,
    opex_per_bbl=opex,
    production_rate=production,
    years=years,
    discount_rate=discount
)

st.subheader("📈 Project Economics")
for k, v in results.items():
    st.metric(label=k, value=f"${v:,.2f}" if "($)" in k else f"{v:,.2f}")
