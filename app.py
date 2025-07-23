import streamlit as st
import yaml
from calculator import calculate_profitability
from localization import loc_strings

# --- 1. Page Configuration and Data Loading ---
st.set_page_config(page_title="AI Service Profitability Simulator", page_icon="💡", layout="wide")

@st.cache_data
def load_config():
    try:
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading 'config.yml': {e}")
        return None
    return config

config = load_config()
if config is None:
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

# --- 3.1. Core Strategic Choice ---
st.sidebar.header(t('section_1_header'))

infra_mode_display = st.sidebar.selectbox(
    t('infra_mode_label'),
    [t('infra_mode_cloud'), t('infra_mode_on_premise')]
)
infra_mode = 'cloud' if infra_mode_display == t('infra_mode_cloud') else 'on_premise'

# --- 3.2. Display Assumptions ---
with st.sidebar.expander(t('expander_assumptions_title')):
    st.markdown(f"**{t('assumptions_financial')}**")
    st.text(f"- {t('assumptions_analysis_years')}: {config['business_assumptions']['analysis_years']} years")
    st.text(f"- {t('assumptions_target_irr')}: {config['business_assumptions']['target_irr']*100}%")
    
    st.markdown(f"**{t('assumptions_model')}**")
    st.text(f"- {t('assumptions_training_cost')}: ${config['model_assumptions']['training_cost']:,}")

    st.markdown(f"**{t('assumptions_user')}**")
    st.text(f"- {t('assumptions_total_users')}: {config['user_assumptions']['total_users']:,}")
    st.text(f"- {t('assumptions_user_dist')}: {config['user_assumptions']['free_user_pct']*100}% / {config['user_assumptions']['low_tier_user_pct']*100}% / {config['user_assumptions']['high_tier_user_pct']*100}%")
    st.text(f"- {t('assumptions_pricing_ratio')}: {config['user_assumptions']['high_to_low_pricing_ratio']}:1")

# --- 4. Main Page ---
st.title(t('app_title'))
st.markdown(t('app_subtitle'))

if st.button(t('run_button_label'), use_container_width=True, type="primary"):
    with st.spinner(t('spinner_text')):
        summary = calculate_profitability(config, infra_mode)

    # --- 4.1. Display Results ---
    st.markdown("---")
    st.header(f"{t('results_header')} - {t('results_for_model').format(model_name=infra_mode_display)}")

    col1, col2 = st.columns(2)
    col1.metric(t('tco_metric_label'), f"${summary.get('total_cash_outflow_pv', 0):,.0f}")
    col2.metric(t('revenue_metric_label'), f"${summary.get('required_monthly_revenue', 0):,.0f}")

    st.markdown("---")
    
    col3, col4 = st.columns(2)
    col3.metric(t('low_tier_fee_label'), f"${summary.get('low_tier_fee', 0):,.2f}")
    col4.metric(t('high_tier_fee_label'), f"${summary.get('high_tier_fee', 0):,.2f}")

    # --- 4.2. Display Methodology Note ---
    st.info(f"**{t('methodology_title')}**\n\n{t('methodology_text')}", icon="ℹ️")

else:
    st.info("사이드바에서 운영 모델을 선택한 후 '수익성 분석 실행' 버튼을 클릭하세요. / Select an operation model in the sidebar and click 'Run Profitability Analysis'.")
