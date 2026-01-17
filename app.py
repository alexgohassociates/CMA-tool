import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# 1. Page Config & Custom Styling
st.set_page_config(page_title="Property Portfolio Analyzer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_stdio=True)

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.title("Property Data")
    dev_name = st.text_input("Development", "KRHR")
    unit_no  = st.text_input("Unit", "02-57")
    sqft     = st.number_input("Size (sqft)", value=1079)
    u_type   = st.text_input("Type", "3 Room")
    
    st.divider()
    
    fmv    = st.number_input("Fair Market Value (PSF)", value=1150)
    my_ask = st.number_input("Your Asking (PSF)", value=1250)
    
    st.divider()
    
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

tz_sg = timezone(timedelta(hours=8))
gen_time = datetime.now(tz_sg).strftime("%d %b %Y, %H:%M (GMT+8)")

# --- MAIN INTERFACE ---
st.title(f"🏢 {dev_name} Analysis Report")
st.caption(f"Unit {unit_no} • {sqft} sqft • {u_type} | Generated: {gen_time}")

# Metric Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Your Asking PSF", f"${my_ask:,.0f}")
col2.metric("Market Value (FMV)", f"${fmv:,.0f}")
col3.metric("Premium %", f"{diff_pct:+.1%}")
col4.metric("Total Asking Price", f"${(my_ask * sqft):,.0f}")

st.divider()

# Plotting
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor('#f8f9fa')

# Zones
ax.axvspan(lower_5, upper_5, color='#2ecc71', alpha=0.12)
ax.axvspan(lower_10, lower_5, color='#f1c40f', alpha=0.1)
ax.axvspan(upper_5, upper_10, color='#f1c40f', alpha=0.1)

# Lines
ax.plot([t_low, t_high], [2, 2], color='#3498db', marker='o', linewidth=6, label="Transacted")
ax.plot([a_low, a_high], [1, 1], color='#34495e', marker='o', linewidth=6, label="Market Asking")

# Indicators
ax.scatter(fmv, 2, color='black', s=150, zorder=5)
ax.plot([fmv, fmv], [2, 0.4], color='#bdc3c7', linestyle='--', alpha=0.5)
ax.scatter(my_ask, 1, color=status_color, s=250, edgecolors='black', zorder=6)
ax.plot([my_ask, my_ask], [1, 0.4], color=status_color, linestyle='--', linewidth=2.5)

# Labels
ax.text(min(t_low, a_low, fmv) - 50, 2, 'TRANSACTED', weight='bold', color='#2980b9', ha='right')
ax.text(min(t_low, a_low, fmv) - 50, 1, 'MARKET ASKING', weight='bold', color='#2c3e50', ha='right')

ax.text(fmv, 0.2, f'FMV\n${fmv:,.0f}', ha='center', weight='bold')
ax.text(my_ask, 0.2, f'MY ASK\n${my_ask:,.0f}', ha='center', weight='bold', color=status_color)

# Status Title
ax.text((t_low + t_high)/2, 2.7, f"POSITIONING: {status_text}", fontsize=16, weight='bold', color=status_color, ha='center')

ax.axis('off')
ax.set_ylim(0, 3)
st.pyplot(fig)

st.success(f"This property is priced {abs(diff_pct):.1%} {'above' if diff_pct > 0 else 'below'} the estimated Fair Market Value.")
