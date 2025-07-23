# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v4.0 - 최종 완성본)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 사업성 시뮬레이터 (v4.0)",
        'app_subtitle': "핵심 입력 변수를 조절하여 AI 서비스의 수익성과 투자 회수 기간을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 입력 변수",
        'lang_selector_label': "언어 (Language)",
        
        'section_1_header': "1. 재무 목표",
        'target_irr_label': "목표 내부수익률 (IRR, %)",
        'target_irr_help': "이 투자를 통해 달성하고자 하는 최소 연평균 수익률입니다. 이 수익률을 기준으로 '필요 서비스 단가'가 역산됩니다.",

        'section_2_header': "2. 기술 및 인프라 전략",
        'hw_ratio_label': "하드웨어 포트폴리오 (고사양 GPU 비중)",
        'hw_ratio_help': "고성능 칩은 단위 효율이 높지만 비쌉니다. 저비용 칩은 그 반대입니다. 워크로드에 맞는 최적의 조합을 선택하세요.",
        'electricity_label': "전력 가격 시나리오",
        'electricity_help': "'표준 전력망'은 일반적인 산업용 요금을, '넷제로'는 100% 재생에너지 사용을 위한 더 비싼 장기계약(PPA) 요금을 가정합니다.",
        'arch_toggle_label': "고급 아키텍처 적용 (선택)",
        'arch_toggle_help': "AI 워크로드를 최적화하는 지능형 아키텍처 도입을 가정합니다. 총 필요 연산량을 줄여 동일 하드웨어로 더 높은 효율을 달성하는 효과를 분석할 수 있습니다.",

        'section_3_header': "3. 비즈니스 모델 가정",
        'assumed_fee_label': "가정된 사용자 월 요금 ($)",
        'assumed_fee_help': "현재 시장 상황을 고려하여, 저사용자에게 청구할 월 요금을 가정하여 입력합니다. 이 요금을 기준으로 '투자 회수 기간'이 계산됩니다.",

        'run_button_label': "🚀 분석 실행",
        'results_header': "📊 시나리오 분석 결과",
        
        'output_section_A_title': "A. 목표 IRR 달성을 위한 필요 서비스 단가",
        'annual_revenue_label': "필요 연간 매출",
        'token_price_label': "토큰당 단가 ($ / 1M tokens)",
        
        'output_section_B_title': "B. 가정된 요금 기준 투자 회수 기간",
        'payback_period_label': "투자금 회수 기간 (년)",
        'payback_inf': "> 10 년",
        
        'footnote_title': "※ '고급 아키텍처 적용' 효과에 대한 참고사항",
        'footnote_text': """
        * **가설 기반:** '고급 아키텍처' 효과는 '작업 종류에 따라 최적화된 경량 모델을 지능적으로 선택하여 자원 낭비를 제거한다'는 가설에 기반합니다.
        * **근거 자료:** 이 가설의 수학적 증명은 [관련 논문](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf)에서 확인하실 수 있습니다.
        """
    },
    'en': {
        'app_title': "💡 AI Service Business Case Simulator (v4.0)",
        'app_subtitle': "Analyze the profitability and payback period of your AI service by adjusting key input variables.",
        'sidebar_title': "⚙️ Scenario Input Variables",
        'lang_selector_label': "Language",
        
        'section_1_header': "1. Financial Goals",
        'target_irr_label': "Target IRR (%)",
        'target_irr_help': "The minimum annual rate of return you want to achieve from this investment. The 'Required Service Price' is calculated based on this target.",

        'section_2_header': "2. Tech & Infrastructure Strategy",
        'hw_ratio_label': "Hardware Portfolio (High-Perf GPU %)",
        'hw_ratio_help': "High-performance chips are more efficient but more expensive. Low-cost chips are the opposite. Choose the optimal mix for your workload.",
        'electricity_label': "Electricity Pricing Scenario",
        'electricity_help': "'Standard Grid' assumes typical industrial rates. 'Net-Zero PPA' assumes a more expensive Power Purchase Agreement for 100% renewable energy.",
        'arch_toggle_label': "Apply Advanced Architecture (Optional)",
        'arch_toggle_help': "Assumes an intelligent architecture that optimizes AI workloads, reducing the total computation required and thus increasing efficiency with the same hardware.",

        'section_3_header': "3. Business Model Assumptions",
        'assumed_fee_label': "Assumed Monthly Fee per User ($)",
        'assumed_fee_help': "Enter an assumed monthly fee for low-tier users based on market conditions. The 'Payback Period' will be calculated based on this fee.",

        'run_button_label': "🚀 Run Analysis",
        'results_header': "📊 Scenario Analysis Results",
        
        'output_section_A_title': "A. Required Service Price to Achieve Target IRR",
        'annual_revenue_label': "Required Annual Revenue",
        'token_price_label': "Price per Token ($ / 1M tokens)",
        
        'output_section_B_title': "B. Payback Period Based on Assumed Fee",
        'payback_period_label': "Payback Period (Years)",
        'payback_inf': "> 10 Years",
        
        'footnote_title': "※ Note on the 'Advanced Architecture' Effect",
        'footnote_text': """
        * **Hypothesis-Based:** The effect of the 'Advanced Architecture' is based on the hypothesis of eliminating resource waste by intelligently selecting optimized models for specific tasks.
        * **Source:** The mathematical proof for this hypothesis can be found in the [accompanying paper](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf).
        """
    }
}

