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
    except FileNotFoundError:
        st.error("Error: 'demand_profile.csv' not found. Please ensure the file is in the project folder.")
        return None, None
        
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        st.error("Error: 'config.yml' not found. Please ensure the file is in the project folder.")
        return None, None
    except Exception as e:
        st.error(f"Error loading or parsing 'config.yml': {e}")
        return None, None
        
    return demand_df, config

demand_profile, config = load_data()

if config is None or demand_profile is None:
    st.stop()

# --- UI ---
st.title("💡 AI Data Center Energy Strategy Simulator")
st.markdown("Design your optimal energy portfolio and analyze the 5-year Total Cost of Ownership (TCO) considering various future scenarios.")

# --- Sidebar for User Inputs ---
st.sidebar.title("📊 Scenario Configuration")

st.sidebar.header("1. Energy Mix Design (%)")
st.sidebar.info("Adjust the share of each power source. The total must be 100%.")

# Energy Mix Sliders
grid_mix = st.sidebar.slider("Grid", 0, 100, 60)
solar_mix = st.sidebar.slider("Solar", 0, 100, 20)
wind_mix = st.sidebar.slider("Wind", 0, 100, 0)
h2_sofc_mix = st.sidebar.slider("H2 Fuel Cell (SOFC)", 0, 100, 20)

# Validate total mix is 100%
total_mix = grid_mix + solar_mix + wind_mix + h2_sofc_mix
if total_mix != 100:
    st.sidebar.error(f"The total energy mix must be 100%. (Currently: {total_mix}%)")
    st.stop()

energy_mix = {
    'grid': grid_mix,
    'solar': solar_mix,
    'wind': wind_mix,
    'hydrogen_SOFC': h2_sofc_mix
}

st.sidebar.header("2. Economic Assumptions")
discount_rate = st.sidebar.slider("Discount Rate (%)", 3.0, 15.0, 8.0, 0.1) / 100
grid_escalation = st.sidebar.slider("Annual Grid Price Escalation (%)", 0.0, 10.0, 3.0, 0.1) / 100
h2_fuel_cost = st.sidebar.number_input("Initial H2 Fuel Cost ($/kWh)", 0.05, 0.30, 0.12, 0.01)
fuel_escalation = st.sidebar.slider("Annual Fuel Cost Escalation (%)", -5.0, 10.0, 0.0, 0.5) / 100

st.sidebar.header("3. Carbon Tax Scenario")
carbon_tax_year = st.sidebar.select_slider(
    "Carbon Tax Introduction Year",
    options=[None, 2, 3, 4, 5],
    value=3,
    format_func=lambda x: "Not Introduced" if x is None else f"Year {x}"
)
carbon_tax_price = st.sidebar.number_input("Carbon Tax Price ($/ton)", 0, 200, 50, 5)

# --- Calculation ---
user_inputs = {
    'demand_profile': demand_profile,
    'energy_mix': energy_mix,
    'econ_assumptions': {
        'discount_rate': discount_rate,
        'grid_escalation': grid_escalation,
        'h2_fuel_cost': h2_fuel_cost,
        'fuel_escalation': fuel_escalation,
        'carbon_tax_year': carbon_tax_year,
        'carbon_tax_price': carbon_tax_price
    }
}

df_results, summary = calculate_5yr_tco(config, user_inputs)

# --- Display Results ---
st.markdown("---")
st.header("Comprehensive Analysis (5-Year TCO)")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("5-Year Total Cost (TCO)", f"${summary['5_Year_TCO']:,.0f}")
col2.metric("5-Year Avg. LCOE", f"${summary['LCOE_Avg_5yr']:.2f} / MWh")
col3.metric("Total CAPEX (PV)", f"${summary['Total_CAPEX_PV']:,.0f}")

# Tabs for detailed analysis
tab1, tab2, tab3 = st.tabs(["📈 Cost Trend Analysis", "💰 Detailed Cost Breakdown", "📄 Raw Data"])

with tab1:
    st.subheader("Annual Cost Composition (Present Value)")
    fig = px.bar(df_results, x='Year', y=['CAPEX (PV)', 'OPEX (PV)'],
                 title="Annual Cost Trend (CAPEX vs OPEX)",
                 labels={'value': 'Cost (USD)', 'variable': 'Cost Type'},
                 template='plotly_white')
    fig.update_layout(barmode='stack', yaxis_title='Cost (USD)', xaxis_title='Year')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("5-Year Detailed Cost Breakdown (in USD)")
    st.dataframe(df_results.style.format({
        "Annual CAPEX": "{:,.0f}", "Annual OPEX": "{:,.0f}",
        "Total Annual Cost": "{:,.0f}", "CAPEX (PV)": "{:,.0f}",
        "OPEX (PV)": "{:,.0f}", "Total Cost (PV)": "{:,.0f}",
        "LCOE ($/MWh)": "{:,.2f}"
    }), use_container_width=True)

with tab3:
    st.subheader("Input Data")
    st.markdown("`demand_profile.csv`")
    st.dataframe(demand_profile, use_container_width=True)
    st.markdown("`config.yml`")
    st.json(config)
