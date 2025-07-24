import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_business_case
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI Datacenter Business Case Simulator", page_icon="💡", layout="wide")

@st.cache_data
def load_data():
    """Loads configuration files."""
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
    """Gets the localized string for a given key."""
    return loc_strings[st.session_state.lang].get(key, key).format(**kwargs)

# --- 3. UI: Sidebar ---
st.sidebar.title(t('sidebar_title'))
st.sidebar.header(t('section_hw_header'))
high_perf_hw_ratio = st.sidebar.slider(
    t('hw_ratio_label'), 0, 100, 50, 5, help=t('hw_ratio_help')
)

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
        user_inputs = {'high_perf_hw_ratio': high_perf_hw_ratio}
        summary = calculate_business_case(config, user_inputs)

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # --- Section A: Performance ---
    st.subheader(t('section_A_title'))
    col_a1, col_a2, col_a3 = st.columns(3)
    col_a1.metric(t('metric_hw_investment'), f"${summary.get('hw_investment', 0):,.0f}")
    col_a2.metric(t('metric_performance_score'), f"{summary.get('total_performance_score', 0):,.0f}")
    col_a3.metric(t('metric_token_capacity'), f"{summary.get('annual_token_capacity', 0) / 1e6:,.1f} T") # In Trillions

    # --- Section B: Cost ---
    st.subheader(t('section_B_title'))
    col_b1, col_b2 = st.columns(2)
    col_b1.metric(t('metric_annual_cost'), f"${summary.get('total_annual_cost', 0):,.0f}")
    col_b2.metric(t('metric_cost_per_token'), f"${summary.get('cost_per_million_tokens', 0):.4f}")

    # --- Section C: Profitability ---
    st.subheader(t('section_C_title'))
    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric(t('metric_users_supported'), f"{summary.get('total_users_supported', 0):,.0f}")
    col_c2.metric(t('metric_annual_revenue'), f"${summary.get('annual_revenue', 0):,.0f}")
    op_profit = summary.get('operating_profit', 0)
    col_c3.metric(
        t('metric_operating_profit'),
        f"${op_profit:,.0f}",
        delta="수익" if op_profit >= 0 else "손실"
    )

else:
    st.info(t('initial_prompt'))
