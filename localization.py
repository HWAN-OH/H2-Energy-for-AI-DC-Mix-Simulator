# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소

loc_strings = {
    'ko': {
        'app_title': "💡 AI 데이터센터 통합 TCO & 전략 시뮬레이터 (v2.1)",
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
        'discount_rate_label': "할인율 (%)",
        'run_button_label': "🚀 TCO 분석 실행",
        'spinner_text': "TCO 분석 중...",
        'results_header': "📊 분석 결과",
        'user_scenario_header': "나의 시나리오 결과",
        'tco_metric_label': "5년 최종 통합 TCO",
        'investment_metric_label': "단위 MW당 최종 투자 비용",
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
        'footer_text': "© 2025, OH SEONG-HWAN. 본 시뮬레이터는 전략적 의사결정을 위한 개념적 도구입니다."
    },
    'en': {
        'app_title': "💡 AI DC Integrated TCO & Strategy Simulator (v2.1)",
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
        'discount_rate_label': "Discount Rate (%)",
        'run_button_label': "🚀 Run TCO Analysis",
        'spinner_text': "Analyzing TCO...",
        'results_header': "📊 Analysis Results",
        'user_scenario_header': "My Scenario's Result",
        'tco_metric_label': "5-Year Final Integrated TCO",
        'investment_metric_label': "Final Investment per MW",
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
        'footer_text': "© 2025, OH SEONG-HWAN. This is a conceptual simulator for strategic decision-making."
    }
}
