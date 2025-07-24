import streamlit as st
import pandas as pd
from calculator import calculate_business_case
from localization import t

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Datacenter Business Simulator", page_icon="💡", layout="wide")

# --- 2. Custom CSS for Polished Design ---
st.markdown("""
<style>
    .main .block-container { padding: 2rem 5rem; }
    .st-emotion-cache-16txtl3 { background-color: #f9fafb; }
    h1 { color: #1e3a8a; font-weight: 700; }
    h2 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; color: #111827; margin-top: 2rem;}
    h3 { color: #1f2937; }
    .stMetric { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: #6b7280; text-align: center; padding: 12px; font-size: 0.85rem; border-top: 1px solid #e5e7eb; }
    .dataframe th { text-align: center !important; background-color: #f3f4f6; font-weight: 600; color: #1f2937; }
    .dataframe td:first-child { text-align: center !important; font-weight: 500; }
    .dataframe td:not(:first-child) { text-align: left !important; font-family: 'Roboto Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# --- 3. Language & Session State ---
if 'lang' not in st.session_state: st.session_state.lang = "ko"
if 'results' not in st.session_state: st.session_state.results = None

# --- 4. Sidebar ---
with st.sidebar:
    selected_lang = st.radio("Language / 언어", ["한국어", "English"], index=0 if st.session_state.lang == "ko" else 1, horizontal=True)
    st.session_state.lang = "ko" if selected_lang == "한국어" else "en"
    st.markdown("---")
    
    with st.expander(t("sidebar_guide_title", st.session_state.lang), expanded=True):
        st.markdown(t("sidebar_guide_text", st.session_state.lang))
    st.markdown("---")

    dc_size_mw = st.slider(t("dc_capacity", st.session_state.lang), 10, 300, 100)
    high_perf_gpu_ratio = st.slider(t("high_perf_gpu_ratio", st.session_state.lang), 0, 100, 50, 5)
    power_option = st.selectbox(t("power_type", st.session_state.lang), [t("power_conventional", st.session_state.lang), t("power_renewable", st.session_state.lang)])
    use_clean_power = "Renewable" if power_option == t("power_renewable", st.session_state.lang) else "Conventional"
    apply_mirrormind = st.checkbox(t("apply_mirrormind", st.session_state.lang), value=True)
    
    st.markdown("---")
    paid_tier_fee = st.slider(t("paid_tier_fee", st.session_state.lang), 5.0, 50.0, 20.0, 1.0)
    premium_tier_multiplier = st.slider(t("premium_tier_multiplier", st.session_state.lang), 2.0, 20.0, 10.0, 0.5)

# --- 5. Main Page ---
st.title(t("app_title", st.session_state.lang))
st.markdown(f"<p style='font-size: 1.15rem; color: #4b5563;'>{t('app_subtitle', st.session_state.lang)}</p>", unsafe_allow_html=True)

if st.button(t("run_button", st.session_state.lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        st.session_state.results = calculate_business_case(
            dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio, paid_tier_fee, premium_tier_multiplier, st.session_state.lang
        )

if st.session_state.results:
    res = st.session_state.results
    lang = st.session_state.lang
    
    # --- Section 1: Overall P&L ---
    st.header(t("section_1_title", lang))
    st.subheader(t("assumptions_title", lang))
    cols1 = st.columns(4)
    cols1[0].metric(t("assump_gpu_mix", lang), res["assumptions"]["gpu_mix_string"])
    cols1[1].metric(t("assump_users", lang), f"{res['assumptions']['supported_users']:,.0f}")
    cols1[2].metric(t("assump_tokens", lang), f"{res['assumptions']['serviced_tokens_t']:,.2f} T")
    cols1[3].metric(t("assump_power", lang), f"{res['assumptions']['consumed_power_gwh']:,.1f} GWh")

    st.subheader(t("pnl_table_title", lang))
    pnl_df = pd.DataFrame({
        t("pnl_item", lang): [t("pnl_revenue", lang), t("pnl_cost", lang), t("pnl_profit", lang)],
        t("pnl_amount", lang): [f"{res['pnl_annual']['revenue']:,.0f}", f"{res['pnl_annual']['cost']:,.0f}", f"{res['pnl_annual']['profit']:,.0f}"]
    })
    st.dataframe(pnl_df, hide_index=True, use_container_width=True)

    # --- Section 2: Per-User P&L ---
    st.header(t("section_2_title", lang))
    
    segment_data = []
    tier_name_map = {"free": t("tier_free", lang), "standard": t("tier_standard", lang), "premium": t("tier_premium", lang)}
    for tier in ["free", "standard", "premium"]:
        data = res["pnl_segments"][tier]
        segment_data.append({
            t("col_segment", lang): tier_name_map[tier],
            t("col_total_revenue", lang): f"{data['total_revenue']:,.0f}",
            t("col_total_cost", lang): f"{data['total_cost']:,.0f}",
            t("col_total_profit", lang): f"{data['total_profit']:,.0f}",
            t("col_per_user_revenue", lang): f"{data['per_user_revenue']:,.2f}",
            t("col_per_user_cost", lang): f"{data['per_user_cost']:,.2f}",
            t("col_per_user_profit", lang): f"{data['per_user_profit']:,.2f}"
        })
    segment_df = pd.DataFrame(segment_data)
    st.dataframe(segment_df, hide_index=True, use_container_width=True)

    st.subheader(t("payback_title", lang))
    payback = res["payback_years"]
    payback_display = f"{payback:.1f} {t('years_suffix', lang)}" if payback != float('inf') else t("unrecoverable", lang)
    st.metric(label=t("payback_years", lang), value=payback_display)

else:
    st.info(t("initial_prompt", st.session_state.lang))

# --- Footer ---
st.markdown(f'<div class="footer"><p>{t("copyright_text", lang)} | {t("contact_text", lang)}</p></div>', unsafe_allow_html=True)
