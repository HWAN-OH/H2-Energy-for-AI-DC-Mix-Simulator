import streamlit as st
import pandas as pd
from calculator import calculate_business_case
from localization import t

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Datacenter Business Simulator", page_icon="💡", layout="wide")

# --- 2. Custom CSS ---
st.markdown("""
<style>
    .main .block-container { padding: 2rem 5rem; }
    h1, h2, h3 { font-weight: 700; color: #111827; }
    h2 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-top: 2rem;}
    .stMetric { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: #6b7280; text-align: center; padding: 12px; font-size: 0.85rem; border-top: 1px solid #e5e7eb; }
    .pnl-table { margin-top: 1rem; }
    .pnl-table .row { display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid #f3f4f6; }
    .pnl-table .row.total { font-weight: 700; border-top: 2px solid #d1d5db; }
    .pnl-table .label { text-align: left; }
    .pnl-table .value { text-align: right; font-family: 'Roboto Mono', monospace; }
    .narrative-block { background-color: #f9fafb; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; }
    .narrative-block h3 { margin-top: 0; }
    .recommendation-block { background-color: #eef2ff; border: 1px solid #c7d2fe; border-radius: 0.5rem; padding: 1.5rem; margin-top: 2rem; }
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
    utilization_rate = st.slider(t("utilization_rate", st.session_state.lang), 40, 100, 60, 5)
    power_option = st.selectbox(t("power_type", st.session_state.lang), [t("power_conventional", st.session_state.lang), t("power_renewable", st.session_state.lang)])
    use_clean_power = "Renewable" if power_option == t("power_renewable", st.session_state.lang) else "Conventional"
    apply_mirrormind = st.checkbox(t("apply_mirrormind", st.session_state.lang), value=False)
    
    st.markdown("---")
    market_price_per_m_tokens = st.slider(t("market_price", st.session_state.lang), 0.5, 5.0, 1.5, 0.1)

    st.markdown("---")
    st.subheader(t("sidebar_pricing_title", st.session_state.lang))
    standard_fee = st.number_input(t("pricing_standard_fee", st.session_state.lang), min_value=0.0, value=20.0, step=1.0)
    premium_fee = st.number_input(t("pricing_premium_fee", st.session_state.lang), min_value=0.0, value=100.0, step=5.0)


lang = st.session_state.lang

# --- 5. Main Page ---
st.title(t("app_title", lang))
st.markdown(f"<p style='font-size: 1.15rem; color: #4b5563;'>{t('app_subtitle', lang)}</p>", unsafe_allow_html=True)

if st.button(t("run_button", lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        st.session_state.results = calculate_business_case(
            dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio, utilization_rate, market_price_per_m_tokens,
            standard_fee, premium_fee,
            lang
        )

if st.session_state.results:
    res = st.session_state.results
    pnl = res['pnl_annual']
    
    st.header(t("section_1_title", lang))
    st.subheader(t("assumptions_title", lang))
    
    st.html(f"""
        <div class="pnl-table">
            <div class="row"><div class="label">{t('pnl_revenue', lang)}</div><div class="value">${pnl['revenue']:,.0f}</div></div>
            <div class="row"><div class="label">{t('pnl_cost_of_revenue', lang)}</div><div class="value">(${pnl['cost_of_revenue']:,.0f})</div></div>
            <div class="row total"><div class="label">{t('pnl_gross_profit', lang)}</div><div class="value">${pnl['gross_profit']:,.0f}</div></div>
            <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_sg_and_a', lang)}</div><div class="value">(${pnl['sg_and_a']:,.0f})</div></div>
            <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_d_and_a', lang)}</div><div class="value">(${pnl['d_and_a']:,.0f})</div></div>
            <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_rd_amortization', lang)}</div><div class="value">(${pnl['rd_amortization']:,.0f})</div></div>
            <div class="row total"><div class="label">{t('pnl_operating_profit', lang)}</div><div class="value">${pnl['operating_profit']:,.0f}</div></div>
        </div>
    """)
    
    st.header(t("section_2_title", lang))
    if 'segment_narratives' in res:
        for segment in res['segment_narratives']:
            st.markdown(f"""
            <div class="narrative-block">
                <h3>{t(segment['tier_name_key'], lang)}</h3>
                <ul>
                    <li><b>{t('narrative_users', lang)}:</b> {segment['num_users']:,.0f}</li>
                    <li><b>{t('narrative_revenue_per_user', lang)}:</b> ${segment['revenue_per_user']:,.2f}</li>
                    <li><b>{t('narrative_cost_per_user', lang)}:</b> ${segment['cost_per_user']:,.2f}</li>
                    <li><b>{t('narrative_profit_per_user', lang)}:</b> ${segment['profit_per_user']:,.2f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    st.header(t("section_3_title", lang))
    if 'segment_narratives' in res:
        for segment in res['segment_narratives']:
            if segment['tier_name_key'] in ['tier_standard', 'tier_premium']:
                profit_color = "red" if segment['new_profit_per_user'] < 0 else "green"
                
                st.markdown(f"""
                <div class="narrative-block">
                    <h3>{t('narrative_pricing_title', lang)}: {t(segment['tier_name_key'], lang)}</h3>
                    <ul>
                        <li><b>{t('narrative_fixed_fee_revenue', lang)}:</b> ${segment['fixed_fee']:,.2f}</li>
                        <li><b>{t('narrative_opportunity_cost', lang)}:</b> ${segment['opportunity_cost']:,.2f}</li>
                        <li style="color:{profit_color};"><b>{t('narrative_new_profit_per_user', lang)}:</b> ${segment['new_profit_per_user']:,.2f}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # [NEW] Section 4: Final Recommendation
    st.header(t("section_4_title", lang))
    if 'recommendation' in res:
        reco = res['recommendation']
        st.markdown(f'<div class="recommendation-block">', unsafe_allow_html=True)
        if reco['is_achievable']:
            st.write(t('recommendation_intro', lang))
            r_cols = st.columns(2)
            r_cols[0].metric(label=t('recommended_standard_fee', lang), value=f"${reco['standard_fee']:.2f}")
            r_cols[1].metric(label=t('recommended_premium_fee', lang), value=f"${reco['premium_fee']:.2f}")
        else:
            st.warning(t('recommendation_unachievable', lang))
        st.markdown(f'</div>', unsafe_allow_html=True)


else:
    st.info(t("initial_prompt", lang))

# --- Footer ---
st.markdown(f'<div class="footer"><p>{t("copyright_text", lang)} | {t("contact_text", lang)}</p></div>', unsafe_allow_html=True)
