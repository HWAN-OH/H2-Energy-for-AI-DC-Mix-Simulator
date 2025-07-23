import streamlit as st
import pandas as pd
import yaml
from calculator import calculate_integrated_tco
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI DC Strategy Simulator", page_icon="💡", layout="wide")

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
    return loc_strings[st.session_state.lang].get(key, key)

# --- 3. UI: Sidebar ---
st.sidebar.title(t('sidebar_title'))

selected_lang_display = st.sidebar.radio(
    t('lang_selector_label'), ['한국어', 'English'],
    index=0 if st.session_state.lang == 'ko' else 1, key='language_selector'
)
st.session_state.lang = 'ko' if selected_lang_display == '한국어' else 'en'

# --- 3.1. Core Strategic Choices ---
st.sidebar.header(t('section_1_header'))

use_carbon_free_mix = st.sidebar.toggle(t('power_mix_label'), value=True, help=t('power_mix_help'))
high_perf_hw_ratio = st.sidebar.slider(t('hw_ratio_label'), 0, 100, 100, 5, help=t('hw_ratio_help'))
apply_advanced_arch = st.sidebar.toggle(t('arch_toggle_label'), value=False, help=t('arch_toggle_help'))

# --- 3.2. Market and Economic Assumptions ---
st.sidebar.header(t('section_2_header'))
market_keys = list(config.get('market_scenarios', {}).keys())
market_display_names = t('market_names')
formatted_options = [market_display_names.get(key, key) for key in market_keys]
display_name_to_key_map = {name: key for name, key in zip(formatted_options, market_keys)}
selected_display_name = st.sidebar.selectbox(t('market_label'), options=formatted_options)
selected_scenario_key = display_name_to_key_map[selected_display_name]
discount_rate = st.sidebar.slider(t('discount_rate_label'), 3.0, 15.0, 8.0, 0.1)

# --- 3.3. Business Goals ---
st.sidebar.header(t('section_3_header'))
target_irr = st.sidebar.slider(t('target_irr_label'), 5.0, 20.0, 8.0, 0.5)

# --- 4. Main Page ---
st.title(t('app_title'))
st.markdown(t('app_subtitle'))

if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    with st.spinner(t('spinner_text')):
        user_inputs = {
            'demand_profile': demand_profile,
            'use_carbon_free_mix': use_carbon_free_mix,
            'apply_advanced_arch': apply_advanced_arch,
            'high_perf_hw_ratio': high_perf_hw_ratio,
            'scenario_params': config['market_scenarios'][selected_scenario_key],
            'econ_assumptions': {'discount_rate': discount_rate / 100.0, 'target_irr': target_irr / 100.0}
        }
        summary = calculate_integrated_tco(config, user_inputs)

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(t('results_header'))

    st.subheader(t('user_scenario_header'))
    col1, col2 = st.columns(2)
    col1.metric(t('tco_metric_label'), f"${summary.get('final_integrated_tco_5yr', 0):,.0f}")
    col2.metric(t('investment_metric_label'), f"${summary.get('investment_per_mw', 0):,.2f} M / MW")

    st.subheader(t('viability_header'))
    viability_data = summary.get('viability', {})
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    col_v1.metric(t('annual_revenue_label'), f"${viability_data.get('required_annual_revenue', 0):,.0f}")
    col_v2.metric(t('token_price_label'), f"${viability_data.get('price_per_million_tokens', 0):.4f}")
    col_v3.metric(t('user_fee_label'), f"${viability_data.get('monthly_fee_per_user', 0):.2f}")
    col_v4.metric(t('serviceable_users_label'), f"{viability_data.get('total_serviceable_users', 0):,.0f}")

    # --- 4.2. Display Narrative Interpretation ---
    with st.expander(t('narrative_expander_title'), expanded=True):
        if not apply_advanced_arch:
            power_mix_text = t('power_mix_carbon_free') if use_carbon_free_mix else t('power_mix_standard')
            hw_strategy = t('hw_strategy_high') if high_perf_hw_ratio > 80 else t('hw_strategy_low') if high_perf_hw_ratio < 20 else t('hw_strategy_hybrid')
            st.markdown(f"#### {t('narrative_no_arch_header')}")
            st.markdown(t('narrative_no_arch_text').format(
                power_mix_text=power_mix_text,
                hw_strategy=hw_strategy,
                tco=summary.get('final_integrated_tco_5yr', 0),
                investment_per_mw=f"${summary.get('investment_per_mw', 0):,.2f} M",
                target_irr=target_irr,
                annual_revenue=viability_data.get('required_annual_revenue', 0)
            ))
        else:
            reduction_pct = (1 - config.get('advanced_architecture_assumptions', {}).get('workload_efficiency_factor', 1)) * 100
            st.markdown(f"#### {t('narrative_arch_header')}")
            st.markdown(t('narrative_arch_text').format(
                reduction_pct=f"{reduction_pct:.1f}",
                tco=summary.get('final_integrated_tco_5yr', 0),
                serviceable_users=viability_data.get('total_serviceable_users', 0),
                user_fee=viability_data.get('monthly_fee_per_user', 0)
            ))
        
        if apply_advanced_arch:
            st.markdown("---")
            st.info(f"{t('footnote_text')}", icon="ℹ️")

else:
    st.info("사이드바에서 전략을 구성한 후 '분석 실행' 버튼을 클릭하세요. / Configure your strategy in the sidebar and click 'Run Analysis'.")

st.markdown("---")
st.caption(t('footer_text'))
