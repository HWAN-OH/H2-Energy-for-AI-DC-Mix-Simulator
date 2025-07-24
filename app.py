import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_business_case
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI Service Executive Dashboard", page_icon="💡", layout="wide")

@st.cache_data
def load_data():
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading 'config.yml': {e}")
        return None
    return config

config = load_data()
if config is None:
    st.stop()

# --- 2. Language and State Management ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'ko'
def t(key, **kwargs):
    return loc_strings[st.session_state.lang].get(key, key).format(**kwargs)

# --- 3. UI: Sidebar ---
st.sidebar.title(t('sidebar_title'))

st.sidebar.header(t('section_tech_strategy'))
high_perf_hw_ratio = st.sidebar.slider(t('hw_ratio_label'), 0, 100, 50, 5, help=t('hw_ratio_help'))
apply_advanced_arch = st.sidebar.toggle(t('arch_toggle_label'), value=False, help=t('arch_toggle_help'))

st.sidebar.header(t('section_financial_strategy'))
target_irr = st.sidebar.slider(t('target_irr_label'), 5.0, 25.0, 8.0, 0.5, help=t('target_irr_help'))
electricity_scenario = st.sidebar.radio(
    t('electricity_label'),
    ['standard_grid', 'net_zero_ppa'],
    format_func=lambda x: t(x),
    help=t('electricity_help')
)

# --- 4. Main Page ---
st.title(t('app_title'))
st.markdown(t('app_subtitle'))
st.session_state.lang = 'ko' if st.radio(t('lang_selector_label'), ['한국어', 'English'], index=0, horizontal=True) == '한국어' else 'en'

if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    elec_price = config.get('operating_scenarios', {}).get('electricity_pricing', {}).get(electricity_scenario, 0.13)

    user_inputs = {
        'high_perf_hw_ratio': high_perf_hw_ratio,
        'target_irr': target_irr,
        'apply_advanced_arch': apply_advanced_arch,
        'electricity_price': elec_price
    }
    summary = calculate_business_case(config, user_inputs)
    pnl = summary.get('pnl', {})
    unit_pnl = summary.get('unit_pnl', {})
    breakeven = summary.get('breakeven', {})

    st.markdown("---")
    st.header(t('results_header'))

    # --- A. Overall P&L ---
    st.subheader(t('section_A_title'))
    col_a1, col_a2, col_a3 = st.columns(3)
    col_a1.metric(t('pnl_revenue'), f"${pnl.get('revenue', 0):,.0f}")
    col_a2.metric(t('pnl_cost'), f"${pnl.get('cost', 0):,.0f}")
    col_a3.metric(t('pnl_profit'), f"${pnl.get('profit', 0):,.0f}", delta="수익" if pnl.get('profit', 0) >= 0 else "손실")

    # --- B. Per-User P&L ---
    st.subheader(t('section_B_title'))
    cols_b = st.columns(len(unit_pnl))
    tier_names = {'free': t('free_tier'), 'paid': t('paid_tier'), 'premium': t('premium_tier')}
    for i, (tier_name, data) in enumerate(unit_pnl.items()):
        with cols_b[i]:
            with st.container(border=True):
                st.markdown(f"**{tier_names.get(tier_name)}**")
                st.text(f"{t('user_pnl_usage')}: {data.get('usage', 0):.2f}M Tokens")
                st.text(f"{t('user_pnl_revenue')}: ${data.get('revenue', 0):,.2f}")
                st.text(f"{t('user_pnl_cost')}: ${data.get('cost', 0):,.2f}")
                st.markdown("---")
                profit = data.get('profit', 0)
                st.metric(t('user_pnl_profit'), f"${profit:,.2f}", delta="수익" if profit >= 0 else "손실")

    # --- C. Break-Even Analysis ---
    st.subheader(t('section_C_title'))
    col_c1, col_c2 = st.columns(2)
    payback = breakeven.get('payback_period', float('inf'))
    payback_display = f"{payback:.2f} {t('years_suffix')}" if payback != float('inf') else t('payback_inf')
    col_c1.metric(t('breakeven_payback'), payback_display)
    
    required_users = breakeven.get('required_users', float('inf'))
    users_display = f"{required_users:,.0f}" if required_users != float('inf') else t('users_inf')
    col_c2.metric(t('breakeven_users'), users_display)

    # --- D. Strategic Recommendations ---
    st.subheader(t('section_D_title'))
    recommendations = []
    if pnl.get('profit', 0) < 0:
        if not apply_advanced_arch:
            recommendations.append(t('reco_arch_off'))
        if high_perf_hw_ratio > 70:
            recommendations.append(t('reco_hw_balance'))
        recommendations.append(t('reco_price_increase'))
    else:
        recommendations.append(t('reco_all_good'))
    
    for reco in recommendations:
        st.info(reco, icon="💡")

else:
    st.info(t('initial_prompt'))
