import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_integrated_tco
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI DC TCO Simulator", page_icon="💡", layout="wide")

@st.cache_data
def load_data():
    try:
        demand_df = pd.read_csv('demand_profile.csv')
        demand_df.columns = [col.strip().lower() for col in demand_df.columns]
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
    """Returns the localized string for the given key."""
    return loc_strings[st.session_state.lang].get(key, key)

# --- 3. UI: Sidebar ---
st.sidebar.title(t('sidebar_title'))

# Language Selector
selected_lang_display = st.sidebar.radio(
    t('lang_selector_label'),
    ['한국어', 'English'],
    index=0 if st.session_state.lang == 'ko' else 1
)
st.session_state.lang = 'ko' if selected_lang_display == '한국어' else 'en'

# Core Strategic Choices
st.sidebar.header(t('section_1_header'))
apply_mirrormind = st.sidebar.toggle(
    t('mirrormind_toggle_label'),
    value=True,
    help=t('mirrormind_toggle_help')
)

high_perf_hw_ratio = st.sidebar.slider(
    t('hw_ratio_label'),
    min_value=0, max_value=100, value=100, step=5,
    help=t('hw_ratio_help')
)

# Market and Economic Assumptions
st.sidebar.header(t('section_2_header'))
selected_scenario_key = st.sidebar.selectbox(
    t('market_label'),
    options=list(config.get('market_scenarios', {}).keys())
)

discount_rate = st.sidebar.slider(t('discount_rate_label'), 3.0, 15.0, 8.0, 0.1)

# --- 4. Main Page ---
st.title(t('app_title'))
st.markdown(t('app_subtitle'))

if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    with st.spinner(t('spinner_text')):
        # --- 4.1. Calculate User's Scenario ---
        user_inputs = {
            'demand_profile': demand_profile,
            'apply_mirrormind': apply_mirrormind,
            'high_perf_hw_ratio': high_perf_hw_ratio,
            'scenario_params': config['market_scenarios'][selected_scenario_key],
            'econ_assumptions': {'discount_rate': discount_rate / 100.0}
        }
        user_summary = calculate_integrated_tco(config, user_inputs)

        # --- 4.2. Calculate 4 Benchmark Scenarios ---
        scenarios = {
            t('option_1_name'): {'apply_mirrormind': False, 'high_perf_hw_ratio': 100, 'desc': t('strategy_1_desc')},
            t('option_2_name'): {'apply_mirrormind': False, 'high_perf_hw_ratio': 0, 'desc': t('strategy_2_desc')},
            t('option_3_name'): {'apply_mirrormind': True, 'high_perf_hw_ratio': 100, 'desc': t('strategy_3_desc')},
            t('option_4_name'): {'apply_mirrormind': True, 'high_perf_hw_ratio': 0, 'desc': t('strategy_4_desc')},
        }
        
        benchmark_results = []
        for name, params in scenarios.items():
            inputs = user_inputs.copy()
            inputs.update(params)
            result = calculate_integrated_tco(config, inputs)
            benchmark_results.append({
                t('strategy_col_1'): name,
                t('strategy_col_2'): params['desc'],
                t('strategy_col_3'): f"${result.get('investment_per_mw', 0):,.2f} M"
            })
        
        benchmark_df = pd.DataFrame(benchmark_results)

    # --- 4.3. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    # Display User's Result
    st.subheader(t('user_scenario_header'))
    col1, col2 = st.columns(2)
    col1.metric(
        t('tco_metric_label'),
        f"${user_summary.get('final_integrated_tco_5yr', 0):,.0f}"
    )
    col2.metric(
        t('investment_metric_label'),
        f"${user_summary.get('investment_per_mw', 0):,.2f} M / MW"
    )

    # Display Benchmark Comparison Table
    st.subheader(t('comparison_header'))
    st.dataframe(benchmark_df, use_container_width=True, hide_index=True)

else:
    st.info("사이드바에서 시나리오를 구성한 후 'TCO 분석 실행' 버튼을 클릭하세요. / Configure your scenario in the sidebar and click 'Run TCO Analysis'.")

st.markdown("---")
st.caption(t('footer_text'))
