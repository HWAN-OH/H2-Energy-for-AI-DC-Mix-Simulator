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
        pnl = summary.get('pnl', {})
        unit_pnl = summary.get('unit_pnl', {})

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # --- Output Section A: Annual P&L Table ---
    st.subheader(t('output_section_A_title'))
    
    pnl_data = {
        '항목': [
            t('pnl_revenue'),
            t('pnl_cost_of_revenue'),
            t('pnl_gross_profit'),
            t('pnl_operating_expenses'),
            t('pnl_operating_profit')
        ],
        '금액 ($)': [
            f"{pnl.get('revenue', 0):,.0f}",
            f"{pnl.get('cost_of_revenue', 0):,.0f}",
            f"{pnl.get('gross_profit', 0):,.0f}",
            f"{pnl.get('operating_expenses', 0):,.0f}",
            f"{pnl.get('operating_profit', 0):,.0f}"
        ]
    }
    pnl_df = pd.DataFrame(pnl_data)
    st.dataframe(pnl_df, hide_index=True, use_container_width=True)


    # --- Output Section B: Per-User P&L ---
    st.subheader(t('output_section_B_title'))
    cols = st.columns(len(unit_pnl))
    tier_names = {'free': t('free_tier'), 'paid': t('paid_tier'), 'premium': t('premium_tier')}
    
    for i, (tier_name, data) in enumerate(unit_pnl.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{tier_names.get(tier_name)}**")
                st.metric(label=t('pnl_user_revenue'), value=f"${data.get('revenue', 0):.2f}")
                st.metric(label=t('pnl_user_cost'), value=f"${data.get('cost', 0):.2f}")
                profit = data.get('profit', 0)
                st.metric(label=t('pnl_user_profit'), value=f"${profit:.2f}",
                            delta="수익" if profit >= 0 else "손실")

else:
    st.info(t('initial_prompt'))
