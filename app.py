
import streamlit as st
import yaml
import pandas as pd

# Load configuration and demand profile
with open("energy_mix_simulator/config.yml", "r") as file:
    config = yaml.safe_load(file)

demand_df = pd.read_csv("energy_mix_simulator/demand_profile.csv")

st.title("⚡ Full-Year Energy Mix Simulator (2025~2029)")

st.sidebar.header("Scenario Parameters")
phase = st.sidebar.selectbox("Scenario Type", ["Initial Phase (NG + Grid)", "Transition Phase (Renewables + H2 + Diesel)"])

# Define sliders OUTSIDE the loop to avoid duplication error
if phase == "Initial Phase (NG + Grid)":
    ng_ratio = st.sidebar.slider("NG SOFC Ratio", 0.0, 1.0, 0.7, key="ng")
    grid_ratio = 1.0 - ng_ratio
else:
    solar_ratio = st.sidebar.slider("Solar Ratio", 0.0, 1.0, 0.25, key="solar")
    wind_ratio = st.sidebar.slider("Wind Ratio", 0.0, 1.0 - solar_ratio, 0.25, key="wind")
    h2_ratio = st.sidebar.slider("H2 SOFC Ratio", 0.0, 1.0 - solar_ratio - wind_ratio, 0.4, key="h2")
    diesel_ratio = 1.0 - solar_ratio - wind_ratio - h2_ratio

run = st.sidebar.button("🔁 Run Full Simulation")

if run:
    results = []

    for idx, row in demand_df.iterrows():
        year = row['year']
        demand_kwh = row['annual_demand_mwh'] * 1000
        row_result = {"Year": year, "Total Demand (MWh)": demand_kwh / 1000}

        if phase == "Initial Phase (NG + Grid)":
            ng = config['initial_phase']['energy_sources']['NG_SOFC']
            grid = config['initial_phase']['energy_sources']['grid']

            ng_kwh = demand_kwh * ng_ratio
            grid_kwh = demand_kwh * grid_ratio

            cost = ng_kwh * ng['fuel_cost_per_kwh'] + grid_kwh * grid['price_per_kwh']
            emission = ng_kwh * ng['carbon_emission_factor'] + grid_kwh * grid['carbon_emission_factor']
            ef = emission / demand_kwh

            row_result.update({
                "NG (MWh)": ng_kwh / 1000,
                "Grid (MWh)": grid_kwh / 1000,
                "Solar": 0, "Wind": 0, "H2 SOFC": 0, "Diesel": 0,
                "Total Cost (USD)": round(cost, 2),
                "Emissions (ton)": round(emission / 1000, 2),
                "Emission Factor (kg/kWh)": round(ef, 3)
            })

        else:
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

            row_result.update({
                "NG (MWh)": 0,
                "Grid (MWh)": 0,
                "Solar (MWh)": solar_kwh / 1000,
                "Wind (MWh)": wind_kwh / 1000,
                "H2 SOFC (MWh)": h2_kwh / 1000,
                "Diesel (MWh)": diesel_kwh / 1000,
                "Total Cost (USD)": round(cost, 2),
                "Emissions (ton)": round(emission / 1000, 2),
                "Emission Factor (kg/kWh)": round(ef, 3)
            })

        results.append(row_result)

    result_df = pd.DataFrame(results)

    styled_df = result_df.style         .format({
            "Total Cost (USD)": "${:,.0f}",
            "Emissions (ton)": "{:.1f}",
            "Emission Factor (kg/kWh)": "{:.3f}"
        })         .background_gradient(subset=["Total Cost (USD)", "Emissions (ton)"], cmap="YlOrRd")

    st.markdown("### 📊 Annual Results (All Years)")
    st.dataframe(styled_df, use_container_width=True)
