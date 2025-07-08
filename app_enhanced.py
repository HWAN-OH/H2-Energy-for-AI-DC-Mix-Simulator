
import streamlit as st
import yaml
import pandas as pd

# Load configuration
with open("energy_mix_simulator/config.yml", "r") as file:
    config = yaml.safe_load(file)

# Load demand profile
demand_df = pd.read_csv("energy_mix_simulator/demand_profile.csv")

# Sidebar – Section Selector
section = st.sidebar.radio("Select Tool", ["Energy Mix Simulator", "SOFC LCOE Estimator"])

if section == "Energy Mix Simulator":
    st.title("⚡ Energy Mix Transition Simulator")

    # Sidebar – Inputs
    st.sidebar.header("Simulation Settings")
    phase = st.sidebar.selectbox("Simulation Phase", ["Initial Phase (NG + Grid)", "Transition Phase (Renewables + H2 + Diesel)"])
    selected_year = st.sidebar.selectbox("Select Year", demand_df['year'])
    simulate = st.sidebar.button("🔁 Run Simulation")

    if simulate:
        demand_kwh = demand_df[demand_df['year'] == selected_year]['annual_demand_mwh'].values[0] * 1000
        st.subheader(f"Year: {selected_year} | Total Demand: {demand_kwh/1000:.2f} MWh")

        result_data = {"Year": selected_year, "Total Demand (MWh)": demand_kwh / 1000}

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

            result_data.update({
                "NG Supply (MWh)": ng_kwh / 1000,
                "Grid Supply (MWh)": grid_kwh / 1000,
                "Solar": 0, "Wind": 0, "H2 SOFC": 0, "Diesel": 0,
                "Total Cost (USD)": round(cost, 2),
                "Emissions (ton)": round(emission / 1000, 2),
                "Emission Factor (kg/kWh)": round(ef, 3)
            })

        else:
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

            result_data.update({
                "NG Supply (MWh)": 0,
                "Grid Supply (MWh)": 0,
                "Solar (MWh)": solar_kwh / 1000,
                "Wind (MWh)": wind_kwh / 1000,
                "H2 SOFC (MWh)": h2_kwh / 1000,
                "Diesel (MWh)": diesel_kwh / 1000,
                "Total Cost (USD)": round(cost, 2),
                "Emissions (ton)": round(emission / 1000, 2),
                "Emission Factor (kg/kWh)": round(ef, 3)
            })

        # 결과 출력
        result_df = pd.DataFrame([result_data])
        st.dataframe(result_df)

elif section == "SOFC LCOE Estimator":
    st.title("🔍 SOFC LCOE Estimator with ESS & Policy Credit")

    h2_price = st.slider("Hydrogen Price ($/kg)", 1.5, 10.0, 3.0, step=0.1)
    sofc_eff = st.slider("SOFC Efficiency (%)", 40, 70, 55, step=1)

    H2_ENERGY_DENSITY = 33.33
    ess_cost_per_kwh = 400
    ess_life_years = 10
    ess_efficiency = 0.85
    annual_cycles = 300
    policy_credit = 0.03

    base_lcoe = h2_price / (H2_ENERGY_DENSITY * (sofc_eff / 100))
    ess_lcoe_add = ess_cost_per_kwh / (annual_cycles * ess_life_years * ess_efficiency)
    adjusted_lcoe = base_lcoe + ess_lcoe_add - policy_credit

    st.markdown(f"### 🔹 Base LCOE: **${base_lcoe:.3f}/kWh**")
    st.markdown(f"### 🔹 Adjusted LCOE: **${adjusted_lcoe:.3f}/kWh**")

    if adjusted_lcoe <= 0.12:
        st.success("✅ Grid Parity Achieved! Competitive.")
    elif adjusted_lcoe <= 0.18:
        st.warning("⚠️ Borderline: Needs DR/REC or incentive.")
    else:
        st.error("❌ Too expensive. Needs tech or subsidy boost.")
