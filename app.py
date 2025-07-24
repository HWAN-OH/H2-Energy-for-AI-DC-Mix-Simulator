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
    .st-emotion-cache-16txtl3 { background-color: #f9fafb; }
    h1, h2, h3 { font-weight: 700; color: #111827; }
    h2 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; margin-top: 2rem;}
    .stMetric { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: #6b7280; text-align: center; padding: 12px; font-size: 0.85rem; border-top: 1px solid #e5e7eb; }
    .pnl-table { margin-top: 1rem; }
    .pnl-table .row { display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid #f3f4f6; }
    .pnl-table .row.total { font-weight: 700; border-top: 2px solid #d1d5db; }
    .pnl-table .label { text-align: left; }
    .pnl-table .value { text-align: right; font-family: 'Roboto Mono', monospace; }
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

# --- 5. Main Page ---
st.title(t("app_title", st.session_state.lang))
st.markdown(f"<p style='font-size: 1.15rem; color: #4b5563;'>{t('app_subtitle', st.session_state.lang)}</p>", unsafe_allow_html=True)

if st.button(t("run_button", st.session_state.lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        st.session_state.results = calculate_business_case(
            dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio, utilization_rate, market_price_per_m_tokens, st.session_state.lang
        )

if st.session_state.results:
    res = st.session_state.results
    lang = st.session_state.lang
    pnl = res['pnl_annual']
    
    st.header(t("section_1_title", lang))
    
    st.subheader(t("assumptions_title", lang))
    cols1 = st.columns(3)
    cols1[0].metric(t("assump_gpu_mix", lang), res["assumptions"]["gpu_mix_string"])
    cols1[1].metric(t("assump_utilization", lang), f"{res['assumptions']['utilization_rate']}%")
    cols1[2].metric(t("assump_tokens", lang), f"{res['assumptions']['serviced_tokens_t']:,.2f}")
    
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
    
    # --- START: ROBUST DATAFRAME DISPLAY LOGIC ---
    if res.get('pnl_by_segment') and len(res['pnl_by_segment']) > 0:
        # 1. Create DataFrame with original English keys from calculator.py
        segment_df = pd.DataFrame(res['pnl_by_segment'])

        # 2. Map the English segment names to translated names for display
        tier_map = {
            'Free': t('tier_free', lang),
            'Standard': t('tier_standard', lang),
            'Premium': t('tier_premium', lang)
        }
        segment_df['segment'] = segment_df['segment'].str.title().map(tier_map)

        # 3. Define column configurations: Use original English keys and set translated 'label' for display
        column_config = {
            "segment": st.column_config.TextColumn(
                label=t('col_segment', lang),
            ),
            "total_revenue": st.column_config.NumberColumn(
                label=t('col_total_revenue', lang),
                format="$ {:,.0f}"
            ),
            "total_cost": st.column_config.NumberColumn(
                label=t('col_total_cost', lang),
                format="$ {:,.0f}"
            ),
            "total_profit": st.column_config.NumberColumn(
                label=t('col_total_profit', lang),
                format="$ {:,.0f}"
            )
        }

        # 4. Display the DataFrame using the robust configuration
        st.dataframe(
            segment_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )
    else:
        st.warning("고객 그룹별 손익 데이터를 계산할 수 없습니다.") # Could not calculate P&L data by customer segment.
    # --- END: ROBUST DATAFRAME DISPLAY LOGIC ---

    # 투자금 회수 기간 계산 및 표시
    st.subheader(t('payback_title', lang))
    operating_profit = res['pnl_annual']['operating_profit']
    if operating_profit > 0:
        payback_period = res['total_investment'] / operating_profit
        payback_text = f"{payback_period:.2f}"
    else:
        payback_text = t('unrecoverable', lang)
    st.metric(label=t('payback_years', lang), value=payback_text)

else:
    st.info(t("initial_prompt", st.session_state.lang))

# --- Footer ---
st.markdown(f'<div class="footer"><p>{t("copyright_text", lang)} | {t("contact_text", lang)}</p></div>', unsafe_allow_html=True)

