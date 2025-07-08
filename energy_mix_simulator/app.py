
import streamlit as st
import yaml
import pandas as pd

# Load configuration
with open("energy_mix_simulator/config.yml", "r") as file:
    config = yaml.safe_load(file)

# Load demand profile
demand_df = pd.read_csv("energy_mix_simulator/demand_profile.csv")

# Sidebar – Inputs
st.sidebar.header("Simulation Settings")
phase = st.sidebar.selectbox("Select Simulation Phase", ["Initial Phase (NG + Grid)", "Transition Phase (Renewables + H2 + Diesel)"])
selected_year = st.sidebar.selectbox("Select Year", demand_df['year'])

demand_kwh = demand_df[demand_df['year'] == selected_year]['annual_demand_mwh'].values[0] * 1000

st.title("⚡ Energy Mix Transition Simulator")
st.subheader(f"Year: {selected_year} | Total Demand: {demand_kwh/1000:.2f} MWh")

if phase == "Initial Phase (NG + Grid)":
    ng_ratio = st.sidebar.slider("NG SOFC Ratio", 0.0, 1.0, 0.7)
    grid_ratio = 1.0 - ng_ratio
    ng = config['initial_phase']['energy_sources']['NG_SOFC']
    grid = config['initial_phase']['energy_sources']['grid']

    ng_kwh = demand_kwh * ng_ratio
    grid_kwh = demand_kwh * grid_ratio

    cost = ng_kwh * ng['fuel_cost_per_kwh'] + grid_kwh * grid['price_per_kwh']
    emission = ng_kwh * ng['carbon_emission_factor'] + grid_kwh * grid['carbon_emission_factor']
    ef = emission / demand_kwh

    st.write(f"🟦 NG SOFC Supply: {ng_kwh/1000:.1f} MWh")
    st.write(f"🟥 Grid Supply: {grid_kwh/1000:.1f} MWh")
    st.success(f"💰 Total Cost: ${cost:,.2f}")
    st.info(f"🌍 Carbon Emission Factor: {ef:.3f} kg/kWh")

else:
    # Renewable + H2 + Diesel
    solar_ratio = st.sidebar.slider("Solar Ratio", 0.0, 1.0, 0.25)
    wind_ratio = st.sidebar.slider("Wind Ratio", 0.0, 1.0 - solar_ratio, 0.25)
    h2_ratio = st.sidebar.slider("H2 SOFC Ratio", 0.0, 1.0 - solar_ratio - wind_ratio, 0.4)
    diesel_ratio = 1.0 - solar_ratio - wind_ratio - h2_ratio

    solar = config['transition_phase']['energy_sources']['solar']
    wind = config['transition_phase']['energy_sources']['wind']
    elec = config['transition_phase']['energy_sources']['hydrogen']['electrolyzer']
    h2 = config['transition_phase']['energy_sources']['hydrogen']['SOFC']
    diesel = config['transition_phase']['energy_sources']['diesel_backup']

    solar_lcoe = solar['capex_per_kw'] / (solar['capacity_factor'] * 8760 * 20)
    wind_lcoe = wind['capex_per_kw'] / (wind['capacity_factor'] * 8760 * 20)
    h2_cost = (1 / elec['efficiency']) * 0.06 / h2['efficiency']

    solar_kwh = demand_kwh * solar_ratio
    wind_kwh = demand_kwh * wind_ratio
    h2_kwh = demand_kwh * h2_ratio
    diesel_kwh = demand_kwh * diesel_ratio

    cost = solar_kwh * solar_lcoe + wind_kwh * wind_lcoe + h2_kwh * h2_cost + diesel_kwh * diesel['fuel_cost_per_kwh']
    emission = diesel_kwh * diesel['carbon_emission_factor']
    ef = emission / demand_kwh

    st.write(f"🟨 Solar: {solar_kwh/1000:.1f} MWh")
    st.write(f"🟩 Wind: {wind_kwh/1000:.1f} MWh")
    st.write(f"🟦 H2 SOFC: {h2_kwh/1000:.1f} MWh")
    st.write(f"🟥 Diesel Backup: {diesel_kwh/1000:.1f} MWh")
    st.success(f"💰 Total Cost: ${cost:,.2f}")
    st.info(f"🌍 Carbon Emission Factor: {ef:.3f} kg/kWh")
