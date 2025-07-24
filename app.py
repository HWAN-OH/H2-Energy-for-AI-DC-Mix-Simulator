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
        background-color: #f9fafb; /* Tailwind gray-50 */
    }
    /* Title styling */
    h1 {
        color: #1e3a8a; /* Tailwind indigo-900 */
        font-weight: 700;
        font-size: 2.5rem;
    }
    /* Subtitle styling */
    .st-emotion-cache-16idsys p {
        font-size: 1.15rem;
        color: #4b5563; /* Tailwind gray-600 */
    }
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #6b7280; /* Tailwind gray-500 */
        text-align: center;
        padding: 12px;
        font-size: 0.85rem;
        border-top: 1px solid #e5e7eb; /* Tailwind gray-200 */
    }
    /* Table styling */
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        overflow: hidden; /* Ensures border-radius is applied to the table */
    }
    .dataframe th {
        background-color: #f3f4f6; /* Tailwind gray-100 */
        text-align: center !important;
        font-weight: 600;
        color: #1f2937; /* Tailwind gray-800 */
        border-bottom: 2px solid #d1d5db; /* Tailwind gray-300 */
    }
    .dataframe td {
        border-bottom: 1px solid #f3f4f6; /* Lighter border for rows */
    }
    .dataframe td:first-child { /* Text column */
        text-align: center !important;
        font-weight: 500;
    }
    .dataframe td:last-child { /* Number column */
        text-align: left !important;
        font-family: 'Roboto Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)


# --- 3. Language State Management ---
if 'lang' not in st.session_state:
    st.session_state.lang = "ko"

# --- 4. Sidebar ---
with st.sidebar:
    # Language Selector
    selected_lang_display = st.radio(
        label="Language / 언어",
        options=["한국어", "English"],
        index=0 if st.session_state.lang == "ko" else 1,
        horizontal=True
    )
    st.session_state.lang = "ko" if selected_lang_display == "한국어" else "en"
    
    st.markdown("---")

    # Simulator Guide
    with st.expander(t("sidebar_guide_title", st.session_state.lang), expanded=True):
        st.markdown(t("sidebar_guide_text", st.session_state.lang))
    
    st.markdown("---")

    # Input variables
    dc_size_mw = st.slider(t("dc_capacity", st.session_state.lang), 10, 300, 100)
    power_option = st.selectbox(
        t("power_type", st.session_state.lang), 
        [t("power_conventional", st.session_state.lang), t("power_renewable", st.session_state.lang)]
    )
    use_clean_power = "Renewable" if power_option == t("power_renewable", st.session_state.lang) else "Conventional"
    
    target_irr = st.slider(t("target_irr", st.session_state.lang), 2.0, 20.0, 8.0, disabled=True)
    apply_mirrormind = st.checkbox(t("apply_mirrormind", st.session_state.lang), value=True)


# --- 5. Main Page ---
# Title and Subtitle
st.title(t("app_title", st.session_state.lang))
st.markdown(f"<div class='st-emotion-cache-16idsys'><p>{t('app_subtitle', st.session_state.lang)}</p></div>", unsafe_allow_html=True)

# Session state to hold results
if 'results' not in st.session_state:
    st.session_state.results = None

# Run button to trigger analysis
if st.button(t("run_button", st.session_state.lang), use_container_width=True, type="primary"):
    with st.spinner('Analyzing...'):
        st.session_state.results = calculate_business_case(
            dc_size_mw=dc_size_mw,
            use_clean_power=use_clean_power,
            target_irr=target_irr,
            apply_mirrormind=apply_mirrormind,
            lang=st.session_state.lang
        )

# Display results if they exist
if st.session_state.results:
    st.header(t("results_header", st.session_state.lang))
    
    # P&L Tables
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("pnl_annual_title", st.session_state.lang, dc_size=st.session_state.results['dc_size']))
        pnl_df = st.session_state.results["pnl_df"]
        pnl_df.iloc[:, 1] = pnl_df.iloc[:, 1].apply(lambda x: f"{x:,.0f}")
        st.dataframe(pnl_df, hide_index=True, use_container_width=True)

    with col2:
        st.subheader(t("pnl_per_user_title", st.session_state.lang))
        per_user_pnl_df = st.session_state.results["per_user_pnl_df"]
        if per_user_pnl_df is not None:
            per_user_pnl_df.iloc[:, 1] = per_user_pnl_df.iloc[:, 1].apply(lambda x: f"{x:,.2f}")
            st.dataframe(per_user_pnl_df, hide_index=True, use_container_width=True)
        else:
            st.warning("Not enough capacity to support users.")

    # Break-Even and Recommendations
    st.subheader(t("breakeven_title", st.session_state.lang))
    breakeven_users = st.session_state.results["break_even_users"]
    if breakeven_users == float('inf'):
        st.metric(label=t("breakeven_users", st.session_state.lang), value=t("unachievable", st.session_state.lang))
    else:
        st.metric(label=t("breakeven_users", st.session_state.lang), value=f"{breakeven_users:,.0f}")

    st.subheader(t("recommendations_title", st.session_state.lang))
    st.info(st.session_state.results["recommendations"])
else:
    st.info(t("initial_prompt", st.session_state.lang))

# --- 6. Footer with Copyright ---
st.markdown(
    f"""
    <div class="footer">
        <p>{t('copyright_text', st.session_state.lang)} | {t('contact_text', st.session_state.lang)}</p>
    </div>
    """,
    unsafe_allow_html=True
)
