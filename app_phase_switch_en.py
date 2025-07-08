
import streamlit as st
import pandas as pd

# Sidebar Inputs
st.sidebar.title("Input Parameters")

# Phase switch year
phase_switch_year = st.sidebar.slider("Start of Phase 2 (Year)", 1, 5, 3)

# Annual electricity demand
annual_demand_kwh = st.sidebar.number_input("Annual Electricity Demand (kWh)", value=50_000_000)

# Phase 1 settings
st.sidebar.subheader("Phase 1 Settings")
phase1_cost_per_kwh = st.sidebar.number_input("Cost per kWh (USD) - Phase 1", value=0.15)
phase1_emission_factor = st.sidebar.number_input("Emission Factor (kg/kWh) - Phase 1", value=0.4)

# Phase 2 settings
st.sidebar.subheader("Phase 2 Settings")
phase2_cost_per_kwh = st.sidebar.number_input("Cost per kWh (USD) - Phase 2", value=0.08)
phase2_emission_factor = st.sidebar.number_input("Emission Factor (kg/kWh) - Phase 2", value=0.05)

# Simulation period
total_years = 5
data = []

for year in range(1, total_years + 1):
    if year < phase_switch_year:
        phase = "Phase 1"
        cost = phase1_cost_per_kwh * annual_demand_kwh
        emissions = phase1_emission_factor * annual_demand_kwh
        emission_factor = phase1_emission_factor
        cost_per_mwh = phase1_cost_per_kwh * 1000
    else:
        phase = "Phase 2"
        cost = phase2_cost_per_kwh * annual_demand_kwh
        emissions = phase2_emission_factor * annual_demand_kwh
        emission_factor = phase2_emission_factor
        cost_per_mwh = phase2_cost_per_kwh * 1000

    data.append({
        "Year": f"Year {year}",
        "Phase": phase,
        "Total Cost (USD)": cost,
        "Carbon Emissions (ton CO₂)": emissions / 1000,
        "Emission Factor (kg/kWh)": emission_factor,
        "LCOE (USD/MWh)": cost_per_mwh
    })

df_result = pd.DataFrame(data)

st.title("Energy Mix Scenario for AI Data Center - Phase Transition Analysis")
st.dataframe(df_result.style.format({
    "Total Cost (USD)": "${:,.0f}",
    "Carbon Emissions (ton CO₂)": "{:,.1f}",
    "Emission Factor (kg/kWh)": "{:.3f}",
    "LCOE (USD/MWh)": "{:.1f}"
}), use_container_width=True)
