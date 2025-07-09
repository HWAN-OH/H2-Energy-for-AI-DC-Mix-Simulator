import streamlit as st
import pandas as pd
import plotly.express as px
import yaml
from calculator import calculate_5yr_tco

# --- Page Configuration ---
st.set_page_config(page_title="AI DC Energy Strategy Simulator", page_icon="💡", layout="wide")

# --- Load Data and Config ---
@st.cache_data
def load_data():
    # ... (load_data function remains the same)
    try:
        demand_df = pd.read_csv('demand_profile.csv')
        demand_df.columns = [col.strip().lower() for col in demand_df.columns]
        required_cols = ['year', 'demand_mwh', 'peak_demand_mw']
        if not all(col in demand_df.columns for col in required_cols):
            st.error(f"Error: 'demand_profile.csv' must contain the columns: {', '.join(required_cols)}")
            return None, None
    except FileNotFoundError:
        st.error("Error: 'demand_profile.csv' not found. Please ensure it's in your repository.")
        return None, None
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        st.error("Error: 'config.yml' not found. Please ensure it's in your repository.")
        return None, None
    except Exception as e:
        st.error(f"Error parsing 'config.yml': {e}")
        return None, None
    return demand_df, config

demand_profile, config = load_data()

if config is None or demand_profile is None:
    st.stop()

# --- UI ---
st.title("💡 AI Data Center Global Energy Strategy Simulator")
initial_peak_demand = demand_profile['peak_demand_mw'].iloc[0]
final_peak_demand = demand_profile['peak_demand_mw'].iloc[-1]
st.markdown(f"Design an optimal energy portfolio for a data center scaling from **{initial_peak_demand:.1f} MW** to **{final_peak_demand:.1f} MW** and analyze its 5-year Total Cost of Ownership (TCO).")

with st.expander("About this Simulator & Key Assumptions"):
    st.markdown(f"""
    **Developed by: [OH SEONG-HWAN](https://www.linkedin.com/in/shoh1224/)**

    This tool was built to provide a high-level strategic analysis of energy portfolios for AI data centers.
    
    ---
    #### **Key Assumptions & Definitions**

    * **Data Center Scale:** The scale is defined by **Peak Demand (MW)**. The default `demand_profile.csv` simulates a data center scaling from **{initial_peak_demand:.1f} MW** to **{final_peak_demand:.1f} MW**.
    * **Market Scenarios:** The initial grid and natural gas prices are loaded based on the selected market scenario.
    * **LCOE & TCO:** The LCOE (Levelized Cost of Energy) is calculated based on the asset's full lifetime (20 years) to provide a true annualized cost. The TCO reflects the 5-year total cost outlay from the operator's perspective.
    * **No Subsidies:** **Crucially, this model does NOT include any government subsidies, tax credits (like the U.S. IRA), or other incentives.** It is a pure cost-based analysis.
    """)

# --- Sidebar ---
st.sidebar.title("📊 Scenario Configuration")
# ... (Sidebar remains the same)
st.sidebar.header("1. Select Market Scenario")
scenario_options = list(config.get('market_scenarios', {}).keys())
if not scenario_options:
    st.sidebar.error("No market scenarios found in config.yml. Please check the file.")
    st.stop()
selected_scenario = st.sidebar.selectbox("Market / Region", scenario_options)
scenario_params = config['market_scenarios'][selected_scenario]
st.sidebar.caption(scenario_params.get('description', ''))
st.sidebar.header("2. Energy Mix Design (%)")
st.sidebar.info("Adjust the share of each power source. The total must be 100%.")
grid_mix = st.sidebar.slider("Grid", 0, 100, 60)
solar_mix = st.sidebar.slider("Solar", 0, 100, 10)
wind_mix = st.sidebar.slider("Wind", 0, 100, 0)
h2_sofc_mix = st.sidebar.slider("H2 Fuel Cell (SOFC)", 0, 100, 10)
ng_sofc_mix = st.sidebar.slider("NG Fuel Cell (NG-SOFC)", 0, 100, 20)
total_mix = grid_mix + solar_mix + wind_mix + h2_sofc_mix + ng_sofc_mix
if total_mix != 100:
    st.sidebar.error(f"Total energy mix must be 100%. (Currently: {total_mix}%)")
    st.stop()
energy_mix = {'grid': grid_mix, 'solar': solar_mix, 'wind': wind_mix, 'hydrogen_SOFC': h2_sofc_mix, 'NG_SOFC': ng_sofc_mix}
st.sidebar.header("3. Economic Assumptions")
discount_rate = st.sidebar.slider("Discount Rate (%)", 3.0, 15.0, 8.0, 0.1) / 100
grid_escalation = st.sidebar.slider("Annual Grid Price Escalation (%)", 0.0, 10.0, 3.0, 0.1) / 100
h2_fuel_cost = st.sidebar.number_input("Initial H2 Fuel Cost ($/kWh)", 0.05, 0.30, 0.15, 0.01)
fuel_escalation = st.sidebar.slider("Annual Fuel Cost Escalation (%)", -5.0, 10.0, 2.0, 0.5) / 100
st.sidebar.header("4. Carbon Tax Scenario")
carbon_tax_year = st.sidebar.select_slider("Carbon Tax Intro Year", options=[None, 2, 3, 4, 5], value=3, format_func=lambda x: "None" if x is None else f"Year {x}")
carbon_tax_price = st.sidebar.number_input("Carbon Tax Price ($/ton)", 0, 200, 50, 5)


if st.button("🚀 Run Analysis", use_container_width=True):
    user_inputs = {
        'demand_profile': demand_profile,
        'energy_mix': energy_mix,
        'scenario_params': scenario_params,
        'econ_assumptions': {
            'discount_rate': discount_rate, 'grid_escalation': grid_escalation,
            'h2_fuel_cost': h2_fuel_cost, 'fuel_escalation': fuel_escalation,
            'carbon_tax_year': carbon_tax_year, 'carbon_tax_price': carbon_tax_price
        }
    }
    with st.spinner("Calculating... Please wait."):
        df_results, summary, capex_details, opex_breakdown = calculate_5yr_tco(config, user_inputs)
    
    st.markdown("---")
    st.header(f"Analysis for: **{selected_scenario}**")

    if summary:
        total_fc_capex = capex_details.get('hydrogen_SOFC_capex', 0) + capex_details.get('NG_SOFC_capex', 0)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("5-Year Total Cost (TCO)", f"${summary.get('5_Year_TCO', 0):,.0f}")
        col2.metric("Avg. LCOE (20-yr lifetime)", f"${summary.get('LCOE_Avg_5yr', 0):.2f} / MWh")
        col3.metric("Total Initial CAPEX", f"${summary.get('Total_CAPEX_Initial', 0):,.0f}")
        col4.metric("Total Fuel Cell CAPEX", f"${total_fc_capex:,.0f}")

        tab1, tab2 = st.tabs(["💰 Detailed Cost Breakdown", "📄 Raw Data"])

        with tab1:
            st.subheader("Initial CAPEX Breakdown")
            capex_df = pd.DataFrame.from_dict(capex_details, orient='index', columns=['Cost (USD)'])
            st.dataframe(capex_df.style.format("${:,.0f}"), use_container_width=True)

            st.subheader("Annual OPEX Composition (Year 1)")
            opex_df_yr1 = df_results.iloc[0][['grid_purchase_cost', 'h2_fuel_cost', 'ng_fuel_cost', 'o&m_cost', 'carbon_tax_cost']]
            st.bar_chart(opex_df_yr1)

        with tab2:
            st.subheader("Full Annual Calculation Results")
            st.dataframe(df_results, use_container_width=True)
            st.subheader("Input Data")
            with st.expander("Click to view configuration"):
                st.json(config)
    else:
        st.warning("Could not calculate results.")
else:
    st.info("Configure your scenario and click 'Run Analysis'.")
