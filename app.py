import streamlit as st
import pandas as pd
import yaml
import plotly.express as px
from calculator import calculate_integrated_tco

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

# --- 2. UI: Title and Sidebar ---
st.title("💡 AI Data Center TCO & Strategy Simulator (v2.0)")
st.markdown("IT 하드웨어, 아키텍처, 건설 및 에너지 비용을 통합하여 최적의 데이터센터 투자 전략을 분석합니다.")

st.sidebar.title("⚙️ Scenario Configuration")

# --- 2.1. Core Strategic Choices ---
st.sidebar.header("1. Core Strategic Choices")
apply_mirrormind = st.sidebar.toggle(
    "**MirrorMind 아키텍처 적용**", 
    value=True,
    help="""
    **적용 시:** AI 워크로드 효율화(필요 연산량 83.3% 감소) 및 에너지 믹스 최적화.
    **미적용 시:** 표준 워크로드 및 에너지 믹스.
    (Note: 효율화 효과는 '미러마인드 도입 제안서'의 가설에 기반합니다.)
    """
)

high_perf_hw_ratio = st.sidebar.slider(
    "**고성능 하드웨어(H100) 비중 (%)**", 
    min_value=0, max_value=100, value=100, step=5,
    help="""
    전체 AI 워크로드 중 고성능 칩으로 처리해야 하는 비율.
    0%는 모든 작업을 저비용 칩으로 처리, 100%는 모든 작업을 고성능 칩으로 처리함을 의미합니다.
    """
)

# --- 2.2. Market and Economic Assumptions ---
st.sidebar.header("2. Market & Economic Assumptions")
selected_scenario = st.sidebar.selectbox(
    "Market / Region", 
    options=list(config.get('market_scenarios', {}).keys())
)

discount_rate = st.sidebar.slider("Discount Rate (%)", 3.0, 15.0, 8.0, 0.1)

# --- 3. Main Page Logic ---
if st.button("🚀 Run TCO Analysis", use_container_width=True, type="primary"):
    
    # --- 3.1. Prepare and Run Calculation ---
    user_inputs = {
        'demand_profile': demand_profile,
        'apply_mirrormind': apply_mirrormind,
        'high_perf_hw_ratio': high_perf_hw_ratio,
        'scenario_params': config['market_scenarios'][selected_scenario],
        'econ_assumptions': {
            'discount_rate': discount_rate / 100.0
        }
    }
    
    with st.spinner("Analyzing TCO..."):
        summary = calculate_integrated_tco(config, user_inputs)

    # --- 3.2. Display Results ---
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Display key metrics
    col1, col2 = st.columns(2)
    col1.metric(
        "5-Year Final Integrated TCO", 
        f"${summary.get('final_integrated_tco_5yr', 0):,.0f}"
    )
    col2.metric(
        "Final Investment per MW", 
        f"${summary.get('investment_per_mw', 0):,.2f} M / MW"
    )
    
    # Display cost breakdown chart
    st.subheader("5-Year TCO Composition")
    breakdown_data = summary.get('breakdown', {})
    if breakdown_data:
        breakdown_df = pd.DataFrame.from_dict(breakdown_data, orient='index', columns=['Cost (USD)'])
        breakdown_df.index.name = 'Cost Component'
        breakdown_df = breakdown_df.reset_index()
        
        # Clean up index names for better display
        breakdown_df['Cost Component'] = breakdown_df['Cost Component'].str.replace('_', ' ').str.title()
        
        fig = px.pie(
            breakdown_df, 
            values='Cost (USD)', 
            names='Cost Component', 
            title='Total 5-Year Cost Breakdown',
            hole=0.3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Display strategic context
    with st.expander("💡 Strategic Interpretation & Next Steps"):
        st.markdown(f"""
        #### **현재 시나리오 분석**
        - **MirrorMind 아키텍처:** `{'적용됨' if apply_mirrormind else '미적용'}`
        - **고성능 하드웨어 비중:** `{high_perf_hw_ratio}%`
        - **시장:** `{selected_scenario}`
        - **산출된 단위 투자비:** **${summary.get('investment_per_mw', 0):,.2f} M / MW**

        #### **결과 해석**
        이 결과는 귀사의 특정 전략 선택에 따른 5년간의 총 투자 비용을 의미합니다. 
        사이드바의 '고성능 하드웨어 비중'을 조절하며 비용 변화를 관찰함으로써, 귀사의 워크로드 환경에 가장 적합한 최적의 하드웨어 포트폴리오를 설계할 수 있습니다.

        #### **다음 단계 제안**
        1.  **민감도 분석:** '고성능 하드웨어 비중'을 0%, 25%, 50%, 75%, 100%로 변경하며 각 시나리오의 TCO를 비교하여 최적의 균형점을 탐색하십시오.
        2.  **경쟁 전략 비교:** 'MirrorMind 아키텍처 적용' 토글을 끄고 동일한 분석을 실행하여, 아키텍처 도입이 가져오는 경제적 가치를 정량적으로 확인하십시오.
        """)
else:
    st.info("사이드바에서 시나리오를 구성한 후 'Run TCO Analysis' 버튼을 클릭하세요.")

st.markdown("---")
st.caption("© 2025, OH SEONG-HWAN. This is a conceptual simulator for strategic decision-making.")
