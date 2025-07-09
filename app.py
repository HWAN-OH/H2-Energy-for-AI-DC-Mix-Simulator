import streamlit as st
import pandas as pd
import plotly.express as px
import yaml
from calculator import calculate_5yr_tco

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Data Center Energy Strategy Simulator",
    page_icon="💡",
    layout="wide"
)

# --- Load Data and Config ---
@st.cache_data
def load_data():
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
st.title("💡 AI Data Center Energy Strategy Simulator")
st.markdown("Design an optimal energy portfolio and analyze the 5-year Total Cost of Ownership (TCO).")

# --- FIX: Add Expander for Context and Credit ---
with st.expander("About this Simulator & Key Assumptions"):
    st.markdown("""
    **Developed by: [OH SEONG-HWAN](https://www.linkedin.com/in/shoh1224/)**

    This tool was built to provide a high-level strategic analysis of energy portfolios for AI data centers. It reflects a core belief that the most pressing challenges of our time can only be solved by bridging deep industry knowledge with data-driven, systems-level thinking.

    ---

    **How is the Data Center scale defined?**

    You are correct, the scale of a data center is often discussed in terms of its **IT Load (MW)**, which is the power consumed by servers, storage, and network equipment.

    This simulation, however, uses **Peak Demand (MW)** as a primary input, which represents the **Total Facility Power**. This includes not only the IT Load but also all supporting infrastructure like cooling, lighting, and power distribution systems.

    The relationship is defined by the Power Usage Effectiveness (PUE):
    `Total Facility Power = IT Load * PUE`

    For context, the default `demand_profile.csv` simulates a data center with a peak demand starting at **8.5 MW**. Assuming a PUE of 1.5, this would correspond to an **IT Load of approximately 5.7 MW**.

    You can tailor the simulation to your specific project by modifying the `demand_profile.csv` file.
    """)
# --- END OF FIX ---


# --- Sidebar ---
st.sidebar.title("📊 Scenario Configuration")
# ... (The rest of the sidebar code remains the same)
st.sidebar.header("1. Energy Mix Design (%)")
st.sidebar.info("Adjust the share of each power source. The total must be 100%.")

grid_mix = st.sidebar.slider("Grid", 0, 100, 60)
solar_mix = st.sidebar.slider("Solar", 0, 100, 20)
wind_mix = st.sidebar.slider("Wind", 0, 100, 0)
h2_sofc_mix = st.sidebar.slider("H2 Fuel Cell (SOFC)", 0, 100, 20)

total_mix = grid_mix + solar_mix + wind_mix + h2_sofc_mix
if total_mix != 100:
    st.sidebar.error(f"Total energy mix must be 100%. (Currently: {total_mix}%)")
    st.stop()

energy_mix = {'grid': grid_mix, 'solar': solar_mix, 'wind': wind_mix, 'hydrogen_SOFC': h2_sofc_mix}

st.sidebar.header("2. Economic Assumptions")
discount_rate = st.sidebar.slider("Discount Rate (%)", 3.0, 15.0, 8.0, 0.1) / 100
grid_escalation = st.sidebar.slider("Annual Grid Price Escalation (%)", 0.0, 10.0, 3.0, 0.1) / 100
h2_fuel_cost = st.sidebar.number_input("Initial H2 Fuel Cost ($/kWh)", 0.05, 0.30, 0.12, 0.01)
fuel_escalation = st.sidebar.slider("Annual Fuel Cost Escalation (%)", -5.0, 10.0, 0.0, 0.5) / 100

st.sidebar.header("3. Carbon Tax Scenario")
carbon_tax_year = st.sidebar.select_slider("Carbon Tax Intro Year", options=[None, 2, 3, 4, 5], value=3, format_func=lambda x: "None" if x is None else f"Year {x}")
carbon_tax_price = st.sidebar.number_input("Carbon Tax Price ($/ton)", 0, 200, 50, 5)


# --- Calculation & Display ---
if st.button("🚀 Run Analysis", use_container_width=True):
    user_inputs = {
        'demand_profile': demand_profile,
        'energy_mix': energy_mix,
        'econ_assumptions': {
            'discount_rate': discount_rate, 'grid_escalation': grid_escalation,
            'h2_fuel_cost': h2_fuel_cost, 'fuel_escalation': fuel_escalation,
            'carbon_tax_year': carbon_tax_year, 'carbon_tax_price': carbon_tax_price
        }
    }

    with st.spinner("Calculating... Please wait."):
        df_results, summary = calculate_5yr_tco(config, user_inputs)

    st.markdown("---")
    st.header("Comprehensive Analysis (5-Year TCO)")

    if summary:
        col1, col2, col3 = st.columns(3)
        col1.metric("5-Year Total Cost (TCO)", f"${summary.get('5_Year_TCO', 0):,.0f}")
        col2.metric("5-Year Avg. LCOE", f"${summary.get('LCOE_Avg_5yr', 0):.2f} / MWh")
        col3.metric("Total CAPEX (PV)", f"${summary.get('Total_CAPEX_PV', 0):,.0f}")

        tab1, tab2, tab3 = st.tabs(["📈 Cost Trend Analysis", "💰 Detailed Cost Breakdown", "📄 Raw Data"])

        with tab1:
            st.subheader("Annual Cost Composition (Present Value)")
            if not df_results.empty:
                fig = px.bar(df_results, x='year', y=['capex (pv)', 'opex (pv)'],
                             title="Annual Cost Trend (CAPEX vs OPEX)",
                             labels={'value': 'Cost (USD)', 'variable': 'Cost Type', 'year': 'Year'},
                             template='plotly_white')
                fig.update_layout(barmode='stack', yaxis_title='Cost (USD)', xaxis_title='Year')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("5-Year Detailed Cost Breakdown (in USD)")
            if not df_results.empty:
                display_df = df_results.copy()
                display_df = display_df.set_index('year')
                formatters = {col: '{:,.0f}' for col in display_df.columns if 'lcoe' not in col}
                formatters['lcoe ($/mwh)'] = '{:,.2f}'
                st.dataframe(display_df.style.format(formatters), use_container_width=True)

        with tab3:
            st.subheader("Input Data Used for This Simulation")
            st.markdown("#### Demand Profile (`demand_profile.csv`)")
            st.dataframe(demand_profile, use_container_width=True)
            
            st.markdown("#### Configuration (`config.yml`)")
            with st.expander("Click to view full configuration parameters"):
                st.json(config)
    else:
        st.warning("Could not calculate results. Please check your configuration and input files.")
else:
    st.info("Please configure your scenario in the sidebar and click 'Run Analysis'.")

