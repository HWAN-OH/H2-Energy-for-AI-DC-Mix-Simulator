import streamlit as st
import pandas as pd
# Import both calculators
from calculator import calculate_core_business_case
from what_if_calculator import analyze_fixed_fee_scenario
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
    .recommendation-block { background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 0.5rem; padding: 1.5rem; margin-top: 2rem; }
    .clarification-box { background-color: #fffbeb; color: #92400e; border: 1px solid #fde68a; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; }
    .explanation-box { background-color: #f3f4f6; border-left: 5px solid #6b7280; padding: 1rem 1.5rem; margin-top: 3rem; }
    /* [NEW] Style for what-if sections */
    .what-if-section { border: 1px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; margin-top: 1rem; }
    .what-if-section h4 { margin-top: 0; color: #4b5563; }
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
    
    apply_mirrormind = st.checkbox(
        label=t("apply_mirrormind_label", st.session_state.lang), 
        value=False, 
        help=t("apply_mirrormind_help", st.session_state.lang)
    )
    
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
st.markdown(f"<div class='clarification-box'>{t('model_clarification', lang)}</div>", unsafe_allow_html=True)

if st.button(t("run_button", lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        core_results = calculate_core_business_case(
            dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio,
            utilization_rate, market_price_per_m_tokens
        )
        
        what_if_narratives, pnl_what_if = analyze_fixed_fee_scenario(
            core_results,
            standard_fee,
            premium_fee
        )
        
        core_results['segment_narratives'] = what_if_narratives
        core_results['pnl_what_if'] = pnl_what_if
        st.session_state.results = core_results

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
                profit_color = "red" if segment['final_profit_per_user'] < 0 else "green"
                
                st.markdown(f"""
                <div class="narrative-block">
                    <h3>{t(segment['tier_name_key'], lang)}</h3>
                    
                    <div class="what-if-section">
                        <h4>{t('what_if_subtitle_potential', lang)}</h4>
                        <ul>
                            <li>{t('what_if_potential_revenue', lang)}: ${segment['revenue_per_user']:,.2f}</li>
                            <li>{t('what_if_potential_cost', lang)}: ${segment['cost_per_user']:,.2f}</li>
                            <li>{t('what_if_potential_profit', lang)}: ${segment['profit_per_user']:,.2f}</li>
                        </ul>
                    </div>

                    <div class="what-if-section">
                        <h4>{t('what_if_subtitle_scenario', lang)}</h4>
                        <ul>
                            <li>{t('what_if_set_fee', lang)}: ${segment['fixed_fee']:,.2f}</li>
                            <li style="font-weight: bold; color:{profit_color};">{t('what_if_final_profit', lang)}: ${segment['final_profit_per_user']:,.2f}</li>
                        </ul>
                    </div>

                    <div class="what-if-section">
                        <h4>{t('what_if_subtitle_implication', lang)}</h4>
                        <ul>
                            <li>{t('what_if_opportunity_cost', lang)}: ${segment['opportunity_cost']:,.2f}</li>
                        </ul>
                        <small>{t('what_if_interpretation', lang, opportunity_cost=segment['opportunity_cost'])}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if 'pnl_what_if' in res:
            pnl_wi = res['pnl_what_if']
            st.subheader(t('what_if_pnl_title', lang))
            st.html(f"""
                <div class="pnl-table">
                    <div class="row"><div class="label">{t('pnl_revenue', lang)}</div><div class="value">${pnl_wi['revenue']:,.0f}</div></div>
                    <div class="row"><div class="label">{t('pnl_cost_of_revenue', lang)}</div><div class="value">(${pnl_wi['cost_of_revenue']:,.0f})</div></div>
                    <div class="row total"><div class="label">{t('pnl_gross_profit', lang)}</div><div class="value">${pnl_wi['gross_profit']:,.0f}</div></div>
                    <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_sg_and_a', lang)}</div><div class="value">(${pnl_wi['sg_and_a']:,.0f})</div></div>
                    <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_d_and_a', lang)}</div><div class="value">(${pnl_wi['d_and_a']:,.0f})</div></div>
                    <div class="row"><div class="label" style="padding-left: 1rem;">{t('pnl_rd_amortization', lang)}</div><div class="value">(${pnl_wi['rd_amortization']:,.0f})</div></div>
                    <div class="row total"><div class="label">{t('pnl_operating_profit', lang)}</div><div class="value">${pnl_wi['operating_profit']:,.0f}</div></div>
                </div>
            """)

    st.header(t("section_4_title", lang))
    if 'recommendation' in res:
        st.markdown(f'<div class="recommendation-block">', unsafe_allow_html=True)
        st.write(t('payback_analysis_intro', lang))
        cash_flow = pnl.get('annual_cash_flow', 0)
        payback_period = res['total_investment'] / cash_flow if cash_flow > 0 else 0
        p_cols = st.columns(2)
        p_cols[0].metric(label=t('annual_cash_flow', lang), value=f"${cash_flow:,.0f}")
        p_cols[1].metric(label=t('calculated_payback_period', lang), value=f"{payback_period:.2f}" if payback_period > 0 else t('unrecoverable', lang))
        st.markdown("---")
        st.write(f"**{t('recommendation_title', lang)}**")
        reco = res['recommendation']
        if reco['is_achievable']:
            st.write(t('recommendation_intro', lang))
            r_cols = st.columns(2)
            r_cols[0].metric(label=t('recommended_standard_fee', lang), value=f"${reco['standard_fee']:.2f}")
            r_cols[1].metric(label=t('recommended_premium_fee', lang), value=f"${reco['premium_fee']:.2f}")
        else:
            st.warning(t('recommendation_unachievable', lang))
        st.markdown(f'</div>', unsafe_allow_html=True)
        
    st.markdown(f"""
    <div class="explanation-box">
        <h4>{t('arch_explanation_title', lang)}</h4>
        <p>{t('arch_explanation_text', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info(t("initial_prompt", lang))

st.markdown('<div style="height: 5rem;"></div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer"><p>{t("copyright_text", lang)} | {t("contact_text", lang)}</p></div>', unsafe_allow_html=True)
