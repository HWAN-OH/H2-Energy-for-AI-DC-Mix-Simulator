import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_business_case
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI Service Business Case Simulator", page_icon="💡", layout="wide")

@st.cache_data
def load_data():
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
def t(key):
    return loc_strings[st.session_state.lang].get(key, key)

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
    format_func=lambda x: "Standard Grid" if x == 'standard_grid' else "Net-Zero (Carbon Free)",
    help=t('electricity_help')
)
apply_advanced_arch = st.sidebar.toggle(t('arch_toggle_label'), value=False, help=t('arch_toggle_help'))

st.sidebar.header(t('section_3_header'))
assumed_low_tier_fee = st.sidebar.number_input(
    t('assumed_fee_label'), 
    min_value=5.0, max_value=100.0, 
    value=config['user_assumptions']['assumed_low_tier_fee'], 
    step=1.0,
    help=t('assumed_fee_help')
)

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
            'assumed_low_tier_fee': assumed_low_tier_fee,
            'electricity_price': config['electricity_pricing_scenarios'][electricity_scenario]['price_per_kwh']
        }
        summary = calculate_business_case(config, user_inputs)

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # --- Output Section A ---
    st.subheader(t('output_section_A_title'))
    col_a1, col_a2 = st.columns(2)
    col_a1.metric(t('annual_revenue_label'), f"${summary.get('required_annual_revenue', 0):,.0f}")
    col_a2.metric(t('token_price_label'), f"${summary.get('price_per_million_tokens', 0):.4f}")
    
    # --- Output Section B ---
    st.subheader(t('output_section_B_title'))
    payback = summary.get('payback_period', float('inf'))
    payback_display = f"{payback:.2f}" if payback != float('inf') else t('payback_inf')
    st.metric(t('payback_period_label'), payback_display)

    # --- Footnote for Advanced Architecture ---
    if apply_advanced_arch:
        st.markdown("---")
        st.info(f"**{t('footnote_title')}**\n\n{t('footnote_text')}", icon="ℹ️")

else:
    st.info("사이드바에서 변수를 조정한 후 '분석 실행' 버튼을 클릭하세요. / Adjust variables in the sidebar and click 'Run Analysis'.")
