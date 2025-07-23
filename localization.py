# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v2.5 - 각주 추가)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 데이터센터 통합 TCO & 사업 타당성 시뮬레이터 (v2.5)",
        # ... (이전 버전과 대부분 동일) ...
        'narrative_expander_title': "결과 해설 및 전략적 제언",
        'footnote_title': "※ 'MirrorMind 적용' 효과에 대한 중요 참고사항",
        'footnote_text': """
        본 시뮬레이션에서 'MirrorMind 적용' 시 나타나는 비용 절감 효과(필요 연산량 83.3% 감소)는 '미러마인드 도입 사업 제안서'에 제시된 **가설**에 기반합니다.

        **핵심 논리:** 모든 AI 작업에 거대 단일 모델을 사용하는 대신, 작업의 종류(예: 단순 요약 vs 복잡한 분석)에 따라 최적화된 경량 모델을 지능적으로 선택하여 사용하는 '워크로드 최적화'를 통해 불필요한 컴퓨팅 자원 낭비를 제거하는 것입니다.

        이 가설은 제안서의 전력 소비 비교('기존 1,200 kWh' vs '미러마인드 200 kWh')를 정량화한 것이며, 본 시뮬레이터는 이 가설이 실현될 경우의 **잠재적 경제성**을 분석하기 위한 도구입니다. 실제 절감 효과는 파일럿 프로젝트를 통한 실증이 필요합니다.
        """,
        # ... (나머지 텍스트는 이전과 동일)
        'app_subtitle': "IT 하드웨어, 아키텍처, 건설 및 에너지 비용을 통합하여 최적의 데이터센터 투자 전략을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 구성",
        'lang_selector_label': "언어 (Language)",
        'section_1_header': "1. 핵심 전략 선택",
        'mirrormind_toggle_label': "**MirrorMind 아키텍처 적용**",
        'mirrormind_toggle_help': """
        **적용 시:** AI 워크로드 효율화(필요 연산량 83.3% 감소) 및 에너지 믹스 최적화.
        **미적용 시:** 표준 워크로드 및 에너지 믹스.
        (참고: 효율화 효과는 '미러마인드 도입 제안서'의 가설에 기반합니다.)
        """,
        'hw_ratio_label': "**고성능 하드웨어(H100) 비중 (%)**",
        'hw_ratio_help': """
        전체 AI 워크로드 중 고성능 칩으로 처리해야 하는 비율.
        0%는 모든 작업을 저비용 칩으로 처리, 100%는 모든 작업을 고성능 칩으로 처리함을 의미합니다.
        """,
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
        'run_button_label': "🚀 TCO 분석 실행",
        'spinner_text': "TCO 분석 중...",
        'results_header': "📊 분석 결과",
        'user_scenario_header': "나의 시나리오 결과",
        'tco_metric_label': "5년 최종 통합 TCO",
        'investment_metric_label': "단위 MW당 최종 투자 비용",
        'viability_header': "사업 타당성 분석 (목표 IRR 달성 기준)",
        'annual_revenue_label': "필요 연간 매출",
        'token_price_label': "필요 서비스 단가 (백만 토큰 당)",
        'user_fee_label': "필요 사용자당 월 요금",
        'comparison_header': "4대 핵심 전략 옵션 비교 기준점",
        'strategy_col_1': "전략 옵션",
        'strategy_col_2': "핵심 전략",
        'strategy_col_3': "단위 MW당 투자 비용",
        'option_1_name': "옵션 1: 현상 유지",
        'option_2_name': "옵션 2: 잘못된 경제학",
        'option_3_name': "옵션 3: 최적 경로",
        'option_4_name': "옵션 4: 실행 가능한 대안",
        'strategy_1_desc': "고성능 (미적용)",
        'strategy_2_desc': "저비용 (미적용)",
        'strategy_3_desc': "고성능 (적용)",
        'strategy_4_desc': "저비용 (적용)",
        'footer_text': "© 2025, OH SEONG-HWAN. 본 시뮬레이터는 전략적 의사결정을 위한 개념적 도구입니다.",
        'narrative_title': "AI 전략 분석 리포트",
        'your_choice_title': "선택한 전략",
        'your_choice_text': "당신은 **{apply_mm_text}** 상태에서 **{hw_strategy} 전략**을 선택했으며, 그 결과 **단위 MW당 {investment_per_mw}**의 투자비가 산출되었습니다.",
        'applied': "미러마인드 적용",
        'not_applied': "미러마인드 미적용",
        'hw_strategy_high': "고성능 하드웨어 중심",
        'hw_strategy_low': "저비용 하드웨어 중심",
        'hw_strategy_hybrid': "하이브리드 하드웨어",
        'key_driver_title': "비용의 핵심 동인 분석",
        'driver_mm_on_title': "아키텍처 효율성",
        'driver_mm_on_text': "미러마인드 적용으로 AI 워크로드가 효율화되어, IT 하드웨어와 에너지 인프라 양쪽에서 근본적인 비용 절감이 발생했습니다.",
        'driver_mm_on_subtext': "그 결과, 당신의 시나리오는 가장 이상적인 '최적 경로'({option_3_cost})에 근접한 높은 효율성을 보여줍니다.",
        'driver_mm_off_title': "높은 에너지 및 인프라 비용",
        'driver_mm_off_text': "미러마인드 미적용으로 인해, AI 워크로드를 감당하기 위한 막대한 양의 에너지와 이를 뒷받침하는 거대한 물리적 인프라(건설, IT)가 전체 비용의 대부분을 차지하고 있습니다.",
        'driver_mm_off_subtext': "이는 '현상 유지' 전략({option_1_cost})과 유사한 고비용 구조입니다.",
        'viability_title': "사업 타당성 평가",
        'viability_text': "선택하신 인프라 투자({investment_per_mw} / MW)를 정당화하고 목표 IRR {target_irr}%를 달성하기 위해서는, 연간 약 **${annual_revenue:,.0f}**의 매출이 필요합니다. 이는 서비스 단가로는 **백만 토큰당 ${token_price:.4f}**, 혹은 **사용자당 월 ${user_fee:.2f}**의 요금 수준에 해당합니다.",
        'recommendation_title': "전략적 제언",
        'rec_mm_high_title': "최적 경로입니다.",
        'rec_mm_high_text': "고성능 하드웨어의 물리적 효율성과 미러마인드의 아키텍처 효율성을 결합하여, 가장 낮은 TCO를 달성하는 이상적인 전략입니다.",
        'rec_mm_low_title': "가장 현실적인 대안입니다.",
        'rec_mm_low_text': "초기 IT 투자 비용을 최소화하면서도 미러마인드를 통해 전체 시스템 효율을 극대화하는, 매우 현명하고 실행 가능한 전략입니다.",
        'rec_mm_hybrid_title': "균형 잡힌 포트폴리오입니다.",
        'rec_mm_hybrid_text': "반드시 고성능이 필요한 일부 워크로드와 비용 효율적인 일반 워크로드를 모두 고려한, 현실적인 하이브리드 전략입니다. 하드웨어 비중을 조절하며 최적의 균형점을 찾아보세요.",
        'rec_no_mm_title': "아키텍처 도입을 최우선으로 고려하십시오.",
        'rec_no_mm_text': "현재 전략은 높은 잠재적 비용을 안고 있습니다. 하드웨어 종류와 무관하게, 미러마인드 아키텍처를 도입하는 것만으로 TCO를 70% 이상 절감할 수 있는 기회가 있습니다.",
        'viability_recommendation': "이 가격 지표를 현재 시장의 경쟁 환경 및 가격 정책과 비교하여, 당신의 비즈니스 모델이 현실적으로 생존 가능한지, 혹은 가격 경쟁력을 갖추기 위해 TCO를 더 절감해야 하는지 판단하는 핵심 기준으로 삼으십시오."
    },
    'en': {
        'app_title': "💡 AI DC Integrated TCO & Business Viability Simulator (v2.5)",
        # ... (이전 버전과 대부분 동일) ...
        'narrative_expander_title': "Interpretation & Strategic Recommendation",
        'footnote_title': "※ Important Note on the 'Apply MirrorMind' Effect",
        'footnote_text': """
        The cost reduction effect (83.3% reduction in required computation) shown when 'Apply MirrorMind' is enabled is based on a **hypothesis** presented in the 'MirrorMind Adoption Proposal' document.

        **Core Logic:** The principle is 'workload optimization'—eliminating unnecessary waste of computing resources by intelligently selecting optimized, lightweight models based on the task type (e.g., simple summarization vs. complex analysis), instead of using a single, large model for everything.

        This hypothesis quantifies the power consumption comparison from the proposal ('Standard 1,200 kWh' vs. 'MirrorMind 200 kWh'). This simulator is a tool to analyze the **potential economic impact** if this hypothesis is realized. Actual savings require validation through a real-world pilot project.
        """,
        # ... (나머지 텍스트는 이전과 동일)
        'app_subtitle': "Analyze the optimal data center investment strategy by integrating IT hardware, architecture, construction, and energy costs.",
        'sidebar_title': "⚙️ Scenario Configuration",
        'lang_selector_label': "Language",
        'section_1_header': "1. Core Strategic Choices",
        'mirrormind_toggle_label': "**Apply MirrorMind Architecture**",
        'mirrormind_toggle_help': """
        **On:** Enables AI workload efficiency (83.3% reduction in required computation) and optimizes the energy mix.
        **Off:** Uses standard workload and energy mix.
        (Note: The efficiency effect is based on the hypothesis in the 'MirrorMind Adoption Proposal'.)
        """,
        'hw_ratio_label': "**High-Performance HW (H100) Ratio (%)**",
        'hw_ratio_help': """
        The percentage of the total AI workload that must be processed by high-performance chips.
        0% means all tasks are handled by low-cost chips; 100% means all tasks are handled by high-performance chips.
        """,
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
        'run_button_label': "🚀 Run TCO Analysis",
        'spinner_text': "Analyzing TCO...",
        'results_header': "📊 Analysis Results",
        'user_scenario_header': "My Scenario's Result",
        'tco_metric_label': "5-Year Final Integrated TCO",
        'investment_metric_label': "Final Investment per MW",
        'viability_header': "Business Viability Analysis (to achieve Target IRR)",
        'annual_revenue_label': "Required Annual Revenue",
        'token_price_label': "Required Service Price (per 1M tokens)",
        'user_fee_label': "Required Monthly Fee per User",
        'comparison_header': "Benchmark: 4 Key Strategic Options",
        'strategy_col_1': "Strategic Option",
        'strategy_col_2': "Core Strategy",
        'strategy_col_3': "Investment per MW",
        'option_1_name': "Option 1: The Incumbent",
        'option_2_name': "Option 2: The False Economy",
        'option_3_name': "Option 3: The Optimal Path",
        'option_4_name': "Option 4: The Viable Alternative",
        'strategy_1_desc': "High-Perf (No MM)",
        'strategy_2_desc': "Low-Cost (No MM)",
        'strategy_3_desc': "High-Perf (w/ MM)",
        'strategy_4_desc': "Low-Cost (w/ MM)",
        'footer_text': "© 2025, OH SEONG-HWAN. This is a conceptual simulator for strategic decision-making.",
        'narrative_title': "AI Strategy Analysis Report",
        'your_choice_title': "Your Chosen Strategy",
        'your_choice_text': "You have selected a **{hw_strategy} strategy** **{apply_mm_text}**, resulting in a final investment cost of **{investment_per_mw} per MW**.",
        'applied': "with MirrorMind applied",
        'not_applied': "without MirrorMind",
        'hw_strategy_high': "High-Performance Hardware-centric",
        'hw_strategy_low': "Low-Cost Hardware-centric",
        'hw_strategy_hybrid': "Hybrid Hardware",
        'key_driver_title': "Key Cost Drivers",
        'driver_mm_on_title': "Architectural Efficiency",
        'driver_mm_on_text': "By applying MirrorMind, the AI workload was made more efficient, leading to fundamental cost savings in both IT hardware and energy infrastructure.",
        'driver_mm_on_subtext': "As a result, your scenario shows high efficiency, approaching the ideal 'Optimal Path' ({option_3_cost}).",
        'driver_mm_off_title': "High Energy & Infrastructure Costs",
        'driver_mm_off_text': "Without MirrorMind, a massive amount of energy and the large-scale physical infrastructure (construction, IT) required to support the AI workload account for the majority of the total cost.",
        'driver_mm_off_subtext': "This is a high-cost structure similar to the 'Incumbent' strategy ({option_1_cost}).",
        'viability_title': "Business Viability Assessment",
        'viability_text': "To justify your infrastructure investment of **{investment_per_mw} per MW** and achieve a **{target_irr}% Target IRR**, your business needs to generate approximately **${annual_revenue:,.0f} in annual revenue**. This translates to a service price point of **${token_price:.4f} per million tokens**, or a **monthly fee of ${user_fee:.2f} per user**.",
        'recommendation_title': "Strategic Recommendation",
        'rec_mm_high_title': "This is the Optimal Path.",
        'rec_mm_high_text': "This is the ideal strategy that achieves the lowest TCO by combining the physical efficiency of high-performance hardware with the architectural efficiency of MirrorMind.",
        'rec_mm_low_title': "This is the most Viable Alternative.",
        'rec_mm_low_text': "This is a very wise and executable strategy that minimizes initial IT investment while maximizing overall system efficiency through MirrorMind.",
        'rec_mm_hybrid_title': "This is a Balanced Portfolio.",
        'rec_mm_hybrid_text': "This is a realistic hybrid strategy that considers both workloads that absolutely require high performance and cost-effective general workloads. Try adjusting the hardware ratio to find the optimal balance.",
        'rec_no_mm_title': "Prioritize adopting a better architecture.",
        'rec_no_mm_text': "The current strategy carries high potential costs. Regardless of the hardware type, there is an opportunity to reduce TCO by over 70% simply by introducing the MirrorMind architecture.",
        'viability_recommendation': "Use this pricing benchmark as a critical standard to assess your business model's viability against the current competitive market landscape. It will help you determine if your pricing is realistic or if you need to further reduce TCO to gain a competitive edge."
    }
}
