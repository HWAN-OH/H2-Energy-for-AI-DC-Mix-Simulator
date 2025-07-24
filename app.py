import streamlit as st
import pandas as pd
from calculator import calculate_business_case
from localization import t

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Datacenter Business Simulator",
    page_icon="💡",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    /* Sidebar styling */
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1rem;
    }
    /* Title styling */
    h1 {
        color: #0c4a6e; /* Tailwind sky-900 */
        font-weight: 700;
    }
    /* Subtitle styling */
    .st-emotion-cache-16idsys p {
        font-size: 1.1rem;
        color: #4b5563; /* Tailwind gray-600 */
    }
    /* Footer styling */
    footer {
        visibility: hidden;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f9fafb; /* Tailwind gray-50 */
        color: #6b7280; /* Tailwind gray-500 */
        text-align: center;
        padding: 10px;
        font-size: 0.9rem;
        border-top: 1px solid #e5e7eb; /* Tailwind gray-200 */
    }
    /* Table styling */
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
    }
    /* Center align text, left align numbers in tables */
    .dataframe th {
        text-align: center !important;
    }
    .dataframe td:nth-child(1) { /* Text column */
        text-align: center !important;
    }
    .dataframe td:nth-child(2) { /* Number column */
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Language State Management ---
if 'lang' not in st.session_state:
    st.session_state.lang = "ko"

# --- Sidebar ---
with st.sidebar:
    # 1. Language Selector
    selected_lang_display = st.radio(
        label="Language / 언어",
        options=["한국어", "English"],
        index=0 if st.session_state.lang == "ko" else 1,
        horizontal=True
    )
    st.session_state.lang = "ko" if selected_lang_display == "한국어" else "en"
    
    st.markdown("---")

    # 3. Simulator Guide
    st.subheader(t("sidebar_guide_title", st.session_state.lang))
    st.markdown(t("sidebar_guide_text", st.session_state.lang))
    
    st.markdown("---")

    # Input variables
    dc_size_mw = st.slider(t("dc_capacity", st.session_state.lang), 10, 300, 100)
    power_option = st.selectbox(
        t("power_type", st.session_state.lang), 
        ["Conventional", "Renewable"]
    )
    use_clean_power = "Renewable" if power_option == "Renewable" else "Conventional"
    
    target_irr = st.slider(t("target_irr", st.session_state.lang), 2.0, 20.0, 8.0, disabled=True) # Disabled as per logic evolution
    apply_mirrormind = st.checkbox(t("apply_mirrormind", st.session_state.lang), value=True)


# --- Main Page ---
# 2. Title and Subtitle
st.title(t("app_title", st.session_state.lang))
st.markdown(f"<div class='st-emotion-cache-16idsys'><p>{t('app_subtitle', st.session_state.lang)}</p></div>", unsafe_allow_html=True)


# 5. Run button to trigger analysis
if st.button(t("run_button", st.session_state.lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        result = calculate_business_case(
            dc_size_mw=dc_size_mw,
            use_clean_power=use_clean_power,
            target_irr=target_irr,
            apply_mirrormind=apply_mirrormind,
            lang=st.session_state.lang
        )

    st.header(t("results_header", st.session_state.lang))
    
    # --- P&L Tables ---
    col1, col2 = st.columns(2)

    with col1:
        # 6. Annual P&L with clarification
        st.subheader(t("pnl_annual_title", st.session_state.lang, dc_size=result['dc_size']))
        pnl_df = result["pnl_df"]
        # 7. Formatting numbers with commas
        pnl_df['Amount ($)'] = pnl_df['Amount ($)'].apply(lambda x: f"{x:,.0f}")
        st.dataframe(pnl_df, hide_index=True, use_container_width=True)

    with col2:
        # 8. Per-User Annual P&L
        st.subheader(t("pnl_per_user_title", st.session_state.lang))
        per_user_pnl_df = result["per_user_pnl_df"]
        if per_user_pnl_df is not None:
            per_user_pnl_df['Amount ($)'] = per_user_pnl_df['Amount ($)'].apply(lambda x: f"{x:,.2f}")
            st.dataframe(per_user_pnl_df, hide_index=True, use_container_width=True)
        else:
            st.warning("Not enough capacity to support users.")


    # --- Break-Even and Recommendations ---
    st.subheader(t("breakeven_title", st.session_state.lang))
    breakeven_users = result["break_even_users"]
    if breakeven_users == float('inf'):
        st.metric(label=t("breakeven_users", st.session_state.lang), value="달성 불가 (Unachievable)")
    else:
        st.metric(label=t("breakeven_users", st.session_state.lang), value=f"{breakeven_users:,.0f} 명")

    st.subheader(t("recommendations_title", st.session_state.lang))
    st.info(result["recommendations"])

else:
    st.info(t("initial_prompt", st.session_state.lang))


# 4. Footer with Copyright
st.markdown(
    f"""
    <div class="footer">
        <p>{t('copyright_text', st.session_state.lang)} | {t('contact_text', st.session_state.lang)}</p>
    </div>
    """,
    unsafe_allow_html=True
)

