import streamlit as st
import pandas as pd
import plotly.express as px
from config_loader import load_config
from calculator import calculate_5yr_tco

# --- Page Configuration ---
st.set_page_config(
    page_title="AI 데이터센터 에너지 전략 시뮬레이터",
    page_icon="💡",
    layout="wide"
)

# --- Load Data and Config ---
@st.cache_data
def load_data():
    """
    Loads demand profile and configuration files.
    수요 프로필과 설정 파일을 로드합니다.
    """
    demand_df = pd.read_csv('demand_profile (2).csv')
    config = load_config('config (2).yml')
    return demand_df, config

demand_profile, config = load_data()

if config is None:
    st.stop()

# --- UI ---
st.title("💡 AI 데이터센터 에너지 전략 시뮬레이터")
st.markdown("향후 5년간의 다양한 변수를 고려하여, 데이터센터에 가장 효율적인 에너지 포트폴리오를 설계하고 총소유비용(TCO)을 분석합니다.")

# --- Sidebar for User Inputs ---
st.sidebar.title("📊 시나리오 설정")

st.sidebar.header("1. 에너지 믹스 설계 (%)")
st.sidebar.info("각 발전원의 비중을 조절하세요. 총합은 100%가 되어야 합니다.")

# Energy Mix Sliders
grid_mix = st.sidebar.slider("Grid (전력망)", 0, 100, 60)
solar_mix = st.sidebar.slider("Solar (태양광)", 0, 100, 20)
wind_mix = st.sidebar.slider("Wind (풍력)", 0, 100, 0)
h2_sofc_mix = st.sidebar.slider("H2 Fuel Cell (수소 연료전지)", 0, 100, 20)

# Validate total mix is 100%
total_mix = grid_mix + solar_mix + wind_mix + h2_sofc_mix
if total_mix != 100:
    st.sidebar.error(f"에너지 믹스의 총합이 100%가 되어야 합니다. (현재: {total_mix}%)")
    st.stop()

energy_mix = {
    'grid': grid_mix,
    'solar': solar_mix,
    'wind': wind_mix,
    'hydrogen_SOFC': h2_sofc_mix
}

st.sidebar.header("2. 경제성 변수 설정")
discount_rate = st.sidebar.slider("할인율 (Discount Rate, %)", 3.0, 15.0, 8.0, 0.1) / 100
grid_escalation = st.sidebar.slider("연간 그리드 요금 상승률 (%)", 0.0, 10.0, 3.0, 0.1) / 100
h2_fuel_cost = st.sidebar.number_input("초기 수소 연료비 ($/kWh)", 0.05, 0.30, 0.12, 0.01)
fuel_escalation = st.sidebar.slider("연간 연료비 상승률 (%)", -5.0, 10.0, 0.0, 0.5) / 100

st.sidebar.header("3. 탄소세 시나리오")
carbon_tax_year = st.sidebar.select_slider(
    "탄소세 도입 연도",
    options=[None, 2, 3, 4, 5],
    value=3,
    format_func=lambda x: "미도입" if x is None else f"{x}년차"
)
carbon_tax_price = st.sidebar.number_input("탄소세 가격 ($/ton)", 0, 200, 50, 5)


# --- Calculation ---
user_inputs = {
    'demand_profile': demand_profile,
    'energy_mix': energy_mix,
    'econ_assumptions': {
        'discount_rate': discount_rate,
        'grid_escalation': grid_escalation,
        'h2_fuel_cost': h2_fuel_cost,
        'fuel_escalation': fuel_escalation,
        'carbon_tax_year': carbon_tax_year,
        'carbon_tax_price': carbon_tax_price
    }
}

df_results, summary = calculate_5yr_tco(config, user_inputs)


# --- Display Results ---
st.markdown("---")
st.header("종합 분석 결과 (5-Year TCO Analysis)")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("5년 총소유비용 (TCO)", f"${summary['5_Year_TCO']:,.0f}")
col2.metric("5년 평균 LCOE", f"${summary['LCOE_Avg_5yr']:.2f} / MWh")
col3.metric("총 CAPEX (현재가치)", f"${summary['Total_CAPEX_PV']:,.0f}")


# Tabs for detailed analysis
tab1, tab2, tab3 = st.tabs(["📈 비용 추이 분석", "💰 비용 상세 내역", "📄 원본 데이터"])

with tab1:
    st.subheader("연도별 비용 구성 (현재가치 기준)")
    
    # Stacked Bar Chart for costs
    fig = px.bar(df_results, x='Year', y=['CAPEX (PV)', 'OPEX (PV)'],
                 title="연간 비용 추이 (CAPEX vs OPEX)",
                 labels={'value': '비용 (USD)', 'variable': '비용 종류'},
                 template='plotly_white')
    fig.update_layout(barmode='stack', yaxis_title='비용 (USD)', xaxis_title='연도')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("5년간 상세 비용 내역 (단위: USD)")
    st.dataframe(df_results.style.format({
        "Annual CAPEX": "{:,.0f}",
        "Annual OPEX": "{:,.0f}",
        "Total Annual Cost": "{:,.0f}",
        "CAPEX (PV)": "{:,.0f}",
        "OPEX (PV)": "{:,.0f}",
        "Total Cost (PV)": "{:,.0f}",
        "LCOE ($/MWh)": "{:,.2f}"
    }), use_container_width=True)

with tab3:
    st.subheader("입력 데이터")
    st.markdown("`demand_profile (2).csv`")
    st.dataframe(demand_profile, use_container_width=True)
    st.markdown("`config (2).yml`")
    st.json(config)
