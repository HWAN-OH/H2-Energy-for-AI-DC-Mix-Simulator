import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_business_case
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI Service Business Case Simulator", page_icon="💡", layout="wide")

@st.cache_data
def load_data():
    """Loads data and configuration files."""
    try:
        demand_df = pd.read_csv('demand_profile.csv')
    except Exception as e:
        st.error(f"Error loading 'demand_profile.csv': {e}")
        return None, None
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading 'config.yml': {e}")
        return None, None
    return demand_df, config

demand_profile, config = load_data()
if config is None or demand_profile is None:
    st.stop()

# --- 2. Language and State Management ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'ko'
def t(key, **kwargs):
    """Gets the localized string for a given key."""
    return loc_strings[st.session_state.lang].get(key, key).format(**kwargs)

# --- 3. UI: Sidebar ---
st.sidebar.title(t('sidebar_title'))
st.sidebar.header(t('section_2_header'))
high_perf_hw_ratio = st.sidebar.slider(t('hw_ratio_label'), 0, 100, 100, 5, help=t('hw_ratio_help'))
electricity_scenario = st.sidebar.radio(
    t('electricity_label'),
    ['standard_grid', 'net_zero_ppa'],
    format_func=lambda x: t(x),
    help=t('electricity_help')
)
apply_advanced_arch = st.sidebar.toggle(t('arch_toggle_label'), value=False, help=t('arch_toggle_help'))

st.sidebar.header(t('section_3_header'))
paid_tier_fee = st.sidebar.slider(t('paid_tier_fee_label'), 5.0, 50.0, 20.0, 1.0, help=t('paid_tier_fee_help'))
premium_tier_fee = st.sidebar.slider(t('premium_tier_fee_label'), 50.0, 200.0, 100.0, 5.0, help=t('premium_tier_fee_help'))

# --- 4. Main Page ---
st.title(t('app_title'))
st.markdown(t('app_subtitle'))
selected_lang_display = st.radio(
    t('lang_selector_label'), ['한국어', 'English'],
    index=0 if st.session_state.lang == 'ko' else 1, horizontal=True
)
st.session_state.lang = 'ko' if selected_lang_display == '한국어' else 'en'


if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    with st.spinner(t('spinner_text')):
        user_inputs = {
            'demand_profile': demand_profile,
            'apply_advanced_arch': apply_advanced_arch,
            'high_perf_hw_ratio': high_perf_hw_ratio,
            'paid_tier_fee': paid_tier_fee,
            'premium_tier_fee': premium_tier_fee,
            'electricity_price': config.get('electricity_pricing_scenarios', {}).get(electricity_scenario, {}).get('price_per_kwh', 0.13)
        }
        summary = calculate_business_case(config, user_inputs)
        analysis_years = config.get('business_assumptions', {}).get('analysis_years', 10)
        pnl = summary.get('pnl', {})

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # --- Output Section A: P&L ---
    st.subheader(t('output_section_A_title'))
    with st.container(border=True):
        rev = pnl.get('revenue', 0)
        op_cost = pnl.get('op_cost_electricity', 0) + pnl.get('op_cost_maintenance', 0)
        dep_amort = pnl.get('depreciation_amortization_asset', 0) + pnl.get('depreciation_amortization_rd', 0)
        op_profit = pnl.get('operating_profit', 0)

        st.markdown(f"**{t('pnl_revenue')}:** `${rev:,.0f}`")
        st.markdown("---")
        st.markdown(f"**{t('pnl_op_cost')}:** `${op_cost:,.0f}`")
        st.markdown(f"&nbsp;&nbsp;&nbsp;{t('pnl_op_cost_electric')}: `${pnl.get('op_cost_electricity', 0):,.0f}`")
        st.markdown(f"&nbsp;&nbsp;&nbsp;{t('pnl_op_cost_maint')}: `${pnl.get('op_cost_maintenance', 0):,.0f}`")
        st.markdown("---")
        st.markdown(f"**{t('pnl_dep_amort')}:** `${dep_amort:,.0f}`")
        st.markdown(f"&nbsp;&nbsp;&nbsp;{t('pnl_dep_amort_asset')}: `${pnl.get('depreciation_amortization_asset', 0):,.0f}`")
        st.markdown(f"&nbsp;&nbsp;&nbsp;{t('pnl_dep_amort_rd')}: `${pnl.get('depreciation_amortization_rd', 0):,.0f}`")
        st.markdown("---")
        st.markdown(f"#### **{t('pnl_op_profit')}:** `${op_profit:,.0f}`")


    # --- Output Section B: Unit Economics ---
    st.subheader(t('output_section_B_title'))
    unit_economics = summary.get('unit_economics', {})
    cols = st.columns(len(unit_economics))
    tier_names = {'free': t('free_tier'), 'paid': t('paid_tier'), 'premium': t('premium_tier')}
    
    for i, (tier_name, data) in enumerate(unit_economics.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{tier_names.get(tier_name)}**")
                st.metric(label=t('monthly_cost_label'), value=f"${data.get('cost', 0):.2f}")
                st.metric(label=t('monthly_revenue_label'), value=f"${data.get('revenue', 0):.2f}")
                profit = data.get('profit', 0)
                st.metric(label=t('monthly_profit_label'), value=f"${profit:.2f}",
                            delta="수익" if profit >= 0 else "손실")

    # --- Output Section C: Overall Viability ---
    st.subheader(t('output_section_C_title'))
    payback = summary.get('payback_period', float('inf'))
    
    if payback == float('inf'):
        payback_display = t('payback_inf')
    elif payback > analysis_years:
        payback_display = f"{payback:.2f} {t('years_suffix_projected')}"
    else:
        payback_display = f"{payback:.2f} {t('years_suffix')}"

    st.metric(t('payback_period_label'), payback_display)

else:
    st.info(t('initial_prompt'))
