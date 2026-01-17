import streamlit as st
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta, timezone

# 1. Page Configuration & Custom Styling
st.set_page_config(page_title="ProProperty PSF Analyzer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #3498db; color: white; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.title("📄 Report Details")
    dev_name = st.text_input("Development", "KRHR")
    unit_no  = st.text_input("Unit Number", "02-57")
    sqft     = st.number_input("Size (sqft)", value=1079)
    u_type   = st.text_input("Unit Type", "3 Room")
    
    st.divider()
    st.title("💰 Pricing Data")
    fmv    = st.number_input("Fair Market Value (PSF)", value=1150)
    my_ask = st.number_input("Your Asking (PSF)", value=1250)
    
    st.divider()
    st.title("📊 Market Range")
    t_low  = st.number_input("Min Transacted PSF", value=1000)
    t_high = st.number_input("Max Transacted PSF", value=1200)
    a_low  = st.number_input("Min Asking PSF", value=1050)
    a_high = st.number_input("Max Asking PSF", value=1300)

# --- CALCULATIONS ---
lower_5, upper_5 = fmv * 0.95, fmv * 1.05
lower_10, upper_10 = fmv * 0.90, fmv * 1.10
diff_pct = (my_ask - fmv) / fmv

if abs(diff_pct) <= 0.05:
    status_text, status_color = "GOOD VALUE", "#2ecc71"
elif abs(diff_pct) <= 0.10:
    status_text, status_color = "PREMIUM", "#f1c40f"
else:
    status_text, status_color = "HIGH PREMIUM", "#e74c3c"

# Force GMT+8 Timestamp
tz_sg = timezone(timedelta(hours=8))
gen_time = datetime.now(tz_sg).strftime("%d %b %Y, %H:%M (GMT+8)")

# --- MAIN DASHBOARD ---
st.title(f"🏢 {dev_name} | Market Positioning Report")
st.caption(f"Unit: {unit_no} • {sqft} sqft • {u_type} | Data as of {gen_time}")

# Metric Cards
m1, m2, m3, m4 = st.columns(4)
m1.metric("Asking PSF", f"${my_ask:,.0f}")
m2.metric("Est. FMV", f"${fmv:,.0f}")
m3.metric("Premium %", f"{diff_pct:+.1%}")
m4.metric("Total Asking", f"${(my_ask * sqft):,.0f}")

st.divider()

# --- PLOTTING LOGIC ---
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor('#f8f9fa')

# Three-Tier Background Zones
ax.axvspan(lower_5, upper_5, color
