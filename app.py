
import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

@st.cache_resource
def load_model():
    return joblib.load("ai_model.pkl")

model = load_model()

st.title("♻️ AI vs Non-AI Waste-to-Energy Plant Simulator")
st.markdown("""
This simulator compares energy and environmental performance of a Waste-to-Energy (WTE) plant **with** and **without** AI optimization.
""")

st.sidebar.header("🧪 Input Waste Composition")
organic = st.sidebar.slider("Organic Content (%)", 20, 80, 50)
moisture = st.sidebar.slider("Moisture Content (%)", 10, 60, 30)
plastic = st.sidebar.slider("Plastic Content (%)", 5, 40, 15)
temp = st.sidebar.slider("Gasifier Temp (°C)", 700, 1200, 900)
er = st.sidebar.slider("Equivalence Ratio (ER)", 0.2, 0.6, 0.35)
tpd = st.sidebar.slider("Feedstock Rate (TPD)", 50, 200, 100)
ai_mode = st.sidebar.toggle("Enable AI Optimization", value=True)

features = np.array([[organic, moisture, plastic, temp, er]])

if ai_mode:
    syngas = model.predict(features)[0]
    mode = "AI-Optimized"
else:
    syngas = 220 + (organic * 0.5) - (moisture * 0.4) + (plastic * 0.6)
    mode = "Static Non-AI"

total_energy = syngas * tpd
co2_saved = total_energy * 0.7
revenue = total_energy * 0.035

st.subheader(f"📊 Simulation Results – {mode} Mode")
st.metric("Syngas Yield (kWh/ton)", f"{syngas:.2f}")
st.metric("Total Energy (kWh/day)", f"{total_energy:,.0f}")
st.metric("CO₂ Saved (kg/day)", f"{co2_saved:,.0f}")
st.metric("Daily Revenue (BHD)", f"{revenue:,.2f}")

modes = ["Energy (kWh)", "CO₂ Saved (kg)", "Revenue (BHD)"]
values = [total_energy, co2_saved, revenue]
fig, ax = plt.subplots()
ax.bar(modes, values, color=["skyblue", "green", "orange"])
ax.set_title("WTE Plant Daily Performance")
ax.set_ylabel("Value")
st.pyplot(fig)

st.markdown("---")
st.markdown("Developed for academic simulation of WTE technology impact in Bahrain 🇧🇭")
