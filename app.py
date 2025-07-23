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
selected_lang_display = st.sidebar.radio(
    t('lang_selector_label'), ['한국어', 'English'],
    index=0 if st.session_state.lang == 'ko' else 1
)
st.session_state.lang = 'ko' if selected_lang_display == '한국어' else 'en'

# --- 3.1. Input Variables ---
st.sidebar.header(t('section_1_header'))
target_irr = st.sidebar.slider(t('target_irr_label'), 5.0, 25.0, 8.0, 0.5, help=t('target_irr_help'))

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

if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    with st.spinner(t('spinner_text')):
        user_inputs = {
            'demand_profile': demand_profile,
            'apply_advanced_arch': apply_advanced_arch,
            'high_perf_hw_ratio': high_perf_hw_ratio,
            'target_irr': target_irr,
            'paid_tier_fee': paid_tier_fee,
            'premium_tier_fee': premium_tier_fee,
            'electricity_price': config.get('electricity_pricing_scenarios', {}).get(electricity_scenario, {}).get('price_per_kwh', 0.13)
        }
        summary = calculate_business_case(config, user_inputs)
        analysis_years = config.get('business_assumptions', {}).get('analysis_years', 10)

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # --- Output Section A: Cost Basis ---
    st.subheader(t('output_section_A_title'))
    col_a1, col_a2 = st.columns(2)
    col_a1.metric(t('annual_revenue_label'), f"${summary.get('required_annual_revenue', 0):,.0f}")
    col_a2.metric(t('token_price_label'), f"${summary.get('price_per_million_tokens', 0):.4f}")

    # --- Output Section B: Unit Economics ---
    st.subheader(t('output_section_B_title'))
    unit_economics = summary.get('unit_economics', {})
    cols = st.columns(len(unit_economics))
    tier_names = {'free': t('free_tier'), 'paid': t('paid_tier'), 'premium': t('premium_tier')}
    
    for i, (tier_name, data) in enumerate(unit_economics.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{tier_names.get(tier_name)}**")
                st.metric(label=t('monthly_usage_label'), value=f"{data.get('token_usage', 0):.1f}M Tokens")
                st.metric(label=t('monthly_cost_label'), value=f"${data.get('cost', 0):.2f}")
                st.metric(label=t('monthly_revenue_label'), value=f"${data.get('revenue', 0):.2f}")
                profit = data.get('profit', 0)
                st.metric(label=t('monthly_profit_label'), value=f"${profit:.2f}",
                            delta=f"{t('profit_status_profit') if profit >= 0 else t('profit_status_loss')}")

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

    # --- Footnote for Advanced Architecture ---
    if apply_advanced_arch:
        st.markdown("---")
        st.info(f"**{t('footnote_title')}**\n\n{t('footnote_text')}", icon="ℹ️")

else:
    st.info(t('initial_prompt'))
