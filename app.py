import streamlit as st
import pandas as pd
from calculator import calculate_business_case
from localization import t

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AI Datacenter Business Simulator",
    page_icon="💡",
    layout="wide"
)

# --- 2. Custom CSS for Polished Design ---
st.markdown("""
<style>
    .main .block-container { padding: 2rem 5rem; }
    .st-emotion-cache-16txtl3 { background-color: #f9fafb; } /* Sidebar BG */
    h1 { color: #1e3a8a; font-weight: 700; }
    h2 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; color: #111827; }
    .stMetric { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: #6b7280; text-align: center; padding: 12px; font-size: 0.85rem; border-top: 1px solid #e5e7eb; }
    /* Table Styling */
    .dataframe th { text-align: center !important; background-color: #f3f4f6; font-weight: 600; color: #1f2937; }
    .dataframe td:first-child { text-align: center !important; font-weight: 500; }
    .dataframe td:not(:first-child) { text-align: left !important; font-family: 'Roboto Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# --- 3. Language & Session State ---
if 'lang' not in st.session_state:
    st.session_state.lang = "ko"
if 'results' not in st.session_state:
    st.session_state.results = None

# --- 4. Sidebar ---
with st.sidebar:
    selected_lang = st.radio("Language / 언어", ["한국어", "English"], index=0 if st.session_state.lang == "ko" else 1, horizontal=True)
    st.session_state.lang = "ko" if selected_lang == "한국어" else "en"
    st.markdown("---")
    
    with st.expander(t("sidebar_guide_title", st.session_state.lang), expanded=True):
        st.markdown(t("sidebar_guide_text", st.session_state.lang))
    st.markdown("---")

    dc_size_mw = st.slider(t("dc_capacity", st.session_state.lang), 10, 300, 100)
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
            dc_size_mw, use_clean_power, apply_mirrormind, paid_tier_fee, premium_tier_multiplier, st.session_state.lang
        )

if st.session_state.results:
    res = st.session_state.results
    
    # --- Section 1: Overall P&L ---
    st.header(t("section_1_title", st.session_state.lang))
    st.subheader(t("assumptions_title", st.session_state.lang))
    cols1 = st.columns(4)
    cols1[0].metric(t("assump_gpu_mix", st.session_state.lang), res["assumptions"]["gpu_mix"])
    cols1[1].metric(t("assump_users", st.session_state.lang), f"{res['assumptions']['supported_users']:,.0f}")
    cols1[2].metric(t("assump_tokens", st.session_state.lang), f"{res['assumptions']['serviced_tokens_t']:,.2f} T")
    cols1[3].metric(t("assump_power", st.session_state.lang), f"{res['assumptions']['consumed_kwh_gwh']:,.1f} GWh")

    st.subheader(t("pnl_table_title", st.session_state.lang))
    pnl_df = pd.DataFrame({
        t("pnl_item", st.session_state.lang): [t("pnl_revenue", st.session_state.lang), t("pnl_cost", st.session_state.lang), t("pnl_profit", st.session_state.lang)],
        t("pnl_amount", st.session_state.lang): [f"{res['pnl_annual']['revenue']:,.0f}", f"{res['pnl_annual']['cost']:,.0f}", f"{res['pnl_annual']['profit']:,.0f}"]
    })
    st.dataframe(pnl_df, hide_index=True, use_container_width=True)

    # --- Section 2: Per-User P&L ---
    st.header(t("section_2_title", st.session_state.lang))
    
    # Create a single detailed DataFrame
    segment_data = []
    for tier in ["free", "standard", "premium"]:
        data = res["pnl_segments"][tier]
        tier_name_map = {"free": t("tier_free", st.session_state.lang), "standard": t("tier_standard", st.session_state.lang), "premium": t("tier_premium", st.session_state.lang)}
        segment_data.append({
            "고객 그룹": tier_name_map[tier],
            "그룹 전체 매출": f"${data['total_revenue']:,.0f}",
            "그룹 전체 비용": f"${data['total_cost']:,.0f}",
            "그룹 전체 손익": f"${data['total_profit']:,.0f}",
            "1인당 매출": f"${data['per_user_revenue']:,.2f}",
            "1인당 비용": f"${data['per_user_cost']:,.2f}",
            "1인당 손익": f"${data['per_user_profit']:,.2f}"
        })
    segment_df = pd.DataFrame(segment_data)
    st.dataframe(segment_df, hide_index=True, use_container_width=True)

    st.subheader(t("payback_title", st.session_state.lang))
    payback = res["payback_years"]
    payback_display = f"{payback:.1f} {t('years_suffix', st.session_state.lang)}" if payback != float('inf') else t("unrecoverable", st.session_state.lang)
    st.metric(label=t("payback_years", st.session_state.lang), value=payback_display)

else:
    st.info(t("initial_prompt", st.session_state.lang))

# --- Footer ---
st.markdown(f'<div class="footer"><p>{t("copyright_text", st.session_state.lang)} | {t("contact_text", st.session_state.lang)}</p></div>', unsafe_allow_html=True)
