# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v3.1 - 중립적 UI 및 금융 모델)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 데이터센터 전략 시뮬레이터 (v3.1)",
        'app_subtitle': "전원, 하드웨어, 아키텍처 등 핵심 전략 변수에 따른 5년 TCO와 10년 사업성을 분석합니다.",
        'sidebar_title': "⚙️ 전략 시나리오 구성",
        'lang_selector_label': "언어 (Language)",
        'section_1_header': "1. 핵심 전략 선택",
        
        'power_mix_label': "전원 구성 전략",
        'power_mix_help': "무탄소 전원(태양광 등) 비중을 높여 ESG 목표를 달성하고 장기적인 에너지 비용 변동성을 줄일 수 있으나, 초기 투자비(CAPEX)가 증가할 수 있습니다. (On: 무탄소 중심, Off: 표준)",
        
        'hw_ratio_label': "하드웨어 포트폴리오",
        'hw_ratio_help': "고성능 칩은 단위 연산 당 전력 효율과 공간 효율이 높지만 초기 구매 비용이 비쌉니다. 저비용 칩은 그 반대의 특성을 가집니다. 워크로드에 맞는 최적의 조합을 선택하세요.",
        
        'arch_toggle_label': "고급 아키텍처 적용 (선택)",
        'arch_toggle_help': "AI 워크로드를 최적화하는 지능형 아키텍처 도입을 가정합니다. 이를 통해 총 필요 연산량을 줄여 동일 하드웨어로 더 높은 효율을 달성하는 효과를 분석할 수 있습니다.",
        
        'section_2_header': "2. 시장 및 경제 가정",
        'market_label': "시장 / 지역",
        'market_names': {
            'USA_California_HighCost': "미국 (캘리포니아) - 고비용",
            'USA_Virginia_AvgCost': "미국 (버지니아) - 평균비용",
            'USA_Washington_LowCost': "미국 (워싱턴) - 저비용",
            'South_Korea_Industrial': "대한민국 (산업용)",
            'EU_Germany_Frankfurt': "유럽 (독일 프랑크푸르트)",
            'EU_Nordics_Favorable': "유럽 (북유럽) - 저비용"
        },
        'discount_rate_label': "할인율 (%)",
        'section_3_header': "3. 사업 목표 설정",
        'target_irr_label': "목표 내부수익률 (IRR, %)",
        'run_button_label': "🚀 분석 실행",
        
        'results_header': "📊 시나리오 분석 결과",
        'user_scenario_header': "나의 시나리오 분석 (5년 TCO 기준)",
        'tco_metric_label': "5년 총소유비용 (TCO)",
        'investment_metric_label': "단위 MW당 5년 투자비",
        
        'viability_header': "사업 타당성 분석 (10년 기준)",
        'annual_revenue_label': "필요 연간 매출",
        'token_price_label': "서비스 단가 (백만 토큰 당)",
        'user_fee_label': "사용자당 월 요금",
        'serviceable_users_label': "총 서비스 가능 인원",
        
        'narrative_expander_title': "결과 해설",
        'narrative_title': "시나리오 분석 리포트",
        'narrative_no_arch_header': "선택한 시나리오 요약:",
        'narrative_no_arch_text': "선택하신 **{power_mix_text}**과 **{hw_strategy}** 조합의 5년 TCO는 약 **${tco:,.0f}**이며, 이는 **MW당 {investment_per_mw}**의 투자비에 해당합니다. 이 비용 구조 하에서 10년간 목표 IRR {target_irr}%를 달성하려면, 연간 약 **${annual_revenue:,.0f}**의 매출이 필요합니다.",
        'narrative_arch_header': "고급 아키텍처 적용 시 잠재적 효과:",
        'narrative_arch_text': "워크로드 최적화 아키텍처를 적용할 경우, 가설에 따라 총 필요 연산량이 **{reduction_pct}% 감소**하여 5년 TCO가 **${tco:,.0f}**로 낮아질 **가능성**이 있습니다. 이는 동일한 물리적 인프라로 **약 {serviceable_users:,.0f}명**의 사용자에게 서비스를 제공할 수 있음을 의미하며, 10년간 목표 IRR 달성에 필요한 사용자당 월 요금을 **${user_fee:.2f}** 수준으로 낮출 수 있습니다.",
        'power_mix_carbon_free': "무탄소 전원 중심",
        'power_mix_standard': "표준 전원",
        'hw_strategy_high': "고성능 하드웨어 중심",
        'hw_strategy_low': "저비용 하드웨어 중심",
        'hw_strategy_hybrid': "하이브리드 하드웨어",
        
        'footnote_title': "※ '고급 아키텍처 적용' 효과에 대한 중요 참고사항",
        'footnote_text': """
        * **가설 기반:** 본 시뮬레이션의 '고급 아키텍처' 효과는 '모든 AI 작업에 거대 단일 모델을 사용하는 대신, 작업 종류에 따라 최적화된 경량 모델을 지능적으로 선택하여 불필요한 자원 낭비를 제거한다'는 가설에 기반합니다.
        * **근거 자료:** 이 가설의 수학적 증명은 [관련 논문](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf)에서 확인하실 수 있습니다.
        * **목적:** 본 시뮬레이터는 이 가설이 실현될 경우의 잠재적 경제성을 분석하기 위한 도구이며, 실제 효과는 실증이 필요합니다.
        """,
        'footer_text': "© 2025, OH SEONG-HWAN. 본 시뮬레이터는 전략적 의사결정을 위한 개념적 도구입니다."
    },
    'en': {
        'app_title': "💡 AI Data Center Strategy Simulator (v3.1)",
        'app_subtitle': "Analyze 5-year TCO and 10-year business viability based on key strategic variables like power, hardware, and architecture.",
        'sidebar_title': "⚙️ Configure Strategy Scenario",
        'lang_selector_label': "Language",
        'section_1_header': "1. Core Strategic Choices",
        'power_mix_label': "Power Mix Strategy",
        'power_mix_help': "A carbon-free mix (On) can help achieve ESG goals and reduce long-term energy cost volatility, but may increase initial CAPEX vs. a Standard mix (Off).",
        'hw_ratio_label': "Hardware Portfolio",
        'hw_ratio_help': "High-performance chips offer better power and space efficiency per computation but have a higher upfront cost. Low-cost chips have the opposite profile. Choose the optimal mix for your workload.",
        'arch_toggle_label': "Apply Advanced Architecture (Optional)",
        'arch_toggle_help': "Assumes the adoption of an intelligent architecture that optimizes AI workloads. This allows you to analyze the effect of achieving higher efficiency with the same hardware by reducing the total required computation.",
        'section_2_header': "2. Market & Economic Assumptions",
        'market_label': "Market / Region",
        'market_names': {
            'USA_California_HighCost': "USA (California) - High Cost",
            'USA_Virginia_AvgCost': "USA (Virginia) - Avg. Cost",
            'USA_Washington_LowCost': "USA (Washington) - Low Cost",
            'South_Korea_Industrial': "South Korea (Industrial)",
            'EU_Germany_Frankfurt': "EU (Germany, Frankfurt)",
            'EU_Nordics_Favorable': "EU (Nordics) - Low Cost"
        },
        'discount_rate_label': "Discount Rate (%)",
        'section_3_header': "3. Business Goals",
        'target_irr_label': "Target IRR (%)",
        'run_button_label': "🚀 Run Analysis",
        'results_header': "📊 Scenario Analysis Results",
        'user_scenario_header': "My Scenario Analysis (5-Year TCO)",
        'tco_metric_label': "5-Year Total Cost of Ownership (TCO)",
        'investment_metric_label': "5-Year Investment per MW",
        'viability_header': "Business Viability Analysis (10-Year Horizon)",
        'annual_revenue_label': "Required Annual Revenue",
        'token_price_label': "Service Price (per 1M tokens)",
        'user_fee_label': "Monthly Fee per User",
        'serviceable_users_label': "Total Serviceable Users",
        'narrative_expander_title': "Results Interpretation",
        'narrative_title': "Scenario Analysis Report",
        'narrative_no_arch_header': "Summary of Your Chosen Scenario:",
        'narrative_no_arch_text': "The 5-year TCO for your selected combination of **{power_mix_text}** and a **{hw_strategy}** is approximately **${tco:,.0f}**, which corresponds to a 5-year investment of **{investment_per_mw} per MW**. To achieve your 10-year target IRR of {target_irr}%, you would need to generate about **${annual_revenue:,.0f}** in annual revenue.",
        'narrative_arch_header': "Potential Effect of Applying Advanced Architecture:",
        'narrative_arch_text': "By applying the workload optimization architecture, the total required computation could be reduced by **{reduction_pct}%** based on the hypothesis, potentially lowering the 5-year TCO to **${tco:,.0f}**. This means the same physical infrastructure could serve approximately **{serviceable_users:,.0f} users**, and the required monthly fee per user to achieve the 10-year target IRR could be reduced to **${user_fee:.2f}**.",
        'power_mix_carbon_free': "a Carbon-Free Power mix",
        'power_mix_standard': "a Standard Power mix",
        'hw_strategy_high': "a High-Performance Hardware focus",
        'hw_strategy_low': "a Low-Cost Hardware focus",
        'hw_strategy_hybrid': "a Hybrid Hardware portfolio",
        'footnote_title': "※ Important Note on the 'Advanced Architecture' Effect",
        'footnote_text': """
        * **Hypothesis-Based:** The effect of the 'Advanced Architecture' in this simulation is based on the hypothesis that 'intelligently selecting optimized, lightweight models for specific tasks eliminates resource waste compared to using a single large model for everything.'
        * **Source:** The mathematical proof for this hypothesis can be found in the [accompanying paper](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf).
        * **Purpose:** This simulator is a tool to analyze the potential economic impact if this hypothesis is realized. Actual effects require real-world validation.
        """,
        'footer_text': "© 2025, OH SEONG-HWAN. This is a conceptual simulator for strategic decision-making."
    }
}
