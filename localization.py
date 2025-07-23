# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v5.5)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 사업성 시뮬레이터 (v5.5)",
        'app_subtitle': "기술 및 가격 전략을 조절하여, 사용자 그룹별 수익성과 전체 사업의 타당성을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 입력 변수",
        'lang_selector_label': "언어 (Language)",

        'section_1_header': "1. 재무 목표",
        'target_irr_label': "목표 내부수익률 (IRR, %)",
        'target_irr_help': "이 투자를 통해 달성하고자 하는 최소 연평균 수익률입니다. 모든 비용 계산의 기준이 됩니다.",

        'section_2_header': "2. 기술 및 인프라 전략",
        'hw_ratio_label': "하드웨어 포트폴리오 (고사양 GPU 비중)",
        'hw_ratio_help': "고성능 칩은 단위 효율이 높지만 비쌉니다. 저비용 칩은 그 반대입니다. 워크로드에 맞는 최적의 조합을 선택하세요.",
        'electricity_label': "전력 가격 시나리오",
        'electricity_help': "'표준 전력망'은 일반적인 산업용 요금을, '넷제로'는 100% 재생에너지 사용을 위한 더 비싼 장기계약(PPA) 요금을 가정합니다.",
        'standard_grid': "표준 전력망",
        'net_zero_ppa': "넷제로 (탄소중립)",
        'arch_toggle_label': "고급 아키텍처 적용 (선택)",
        'arch_toggle_help': "AI 워크로드를 최적화하는 지능형 아키텍처 도입을 가정합니다. 총 필요 연산량을 줄여 동일 하드웨어로 더 높은 효율을 달성하는 효과를 분석할 수 있습니다.",

        'section_3_header': "3. 서비스 가격 전략",
        'paid_tier_fee_label': "유료 사용자 월 요금 ($)",
        'paid_tier_fee_help': "표준 유료 사용자에게 청구할 월 요금을 설정합니다.",
        'premium_tier_fee_label': "프리미엄 사용자 월 요금 ($)",
        'premium_tier_fee_help': "고사용량 프리미엄 사용자에게 청구할 월 요금을 설정합니다.",

        'run_button_label': "🚀 분석 실행",
        'results_header': "📊 시나리오 분석 결과",
        'spinner_text': "시나리오 분석 중입니다...",
        'initial_prompt': "사이드바에서 변수를 조정한 후 '분석 실행' 버튼을 클릭하세요.",

        'output_section_A_title': "A. 비용 구조 분석 (Cost Basis)",
        'annual_revenue_label': "손익분기 연간 매출 (IRR 기준)",
        'token_price_label': "토큰당 원가 ($ / 1M tokens)",

        'output_section_B_title': "B. 사용자 그룹별 수익성 분석 (가격 모델 검증)",
        'user_tier_header': "사용자 그룹",
        'free_tier': "무료 사용자",
        'paid_tier': "유료 사용자",
        'premium_tier': "프리미엄 사용자",
        'monthly_usage_label': "월간 사용량",
        'monthly_cost_label': "월간 비용",
        'monthly_revenue_label': "월간 수익",
        'monthly_profit_label': "월간 손익",
        'profit_status_profit': "수익",
        'profit_status_loss': "손실",

        'paradox_explanation_title': "💡 분석: 왜 사용자별 수익과 전체 수익이 다른가요?",
        'paradox_explanation_text': """
        **개별 사용자는 수익성이 높은데 전체 사업은 '회수 불가'인 것은, 시뮬레이터가 비즈니스의 중요한 딜레마를 정확히 보여주기 때문입니다.**

        - **B 분석 (가격 모델):** 이 분석은 "만약 사업이 성공한다면, 우리 요금제는 원가 대비 수익성이 있는가?"를 답합니다. 현재 유료 고객들은 사용하는 서비스 원가보다 훨씬 많은 돈을 내므로 **가격 정책은 성공적**입니다.

        - **C 분석 (사업 모델):** 이 분석은 "소수 유료 고객의 총수익이, 다수 무료 고객의 손실과 막대한 초기 투자금을 모두 감당할 수 있는가?"를 답합니다. 현재는 유료 고객 비중이 낮아 전체 비용 구조를 감당할 수 없으므로, **현재의 사업 모델은 실패할 가능성이 높음**을 의미합니다.
        """,

        'output_section_C_title': "C. 최종 사업 타당성 (초기 투자금 포함)",
        'payback_period_label': "전체 투자 회수 기간",
        'payback_inf': "회수 불가",
        'years_suffix': "년",
        'years_suffix_projected': "년 (추정)",

        'footnote_title': "※ '고급 아키텍처 적용' 효과에 대한 참고사항",
        'footnote_text': """
        * **가설 기반:** '고급 아키텍처' 효과는 '작업 종류에 따라 최적화된 경량 모델을 지능적으로 선택하여 자원 낭비를 제거한다'는 가설에 기반합니다.
        * **근거 자료:** 이 가설의 수학적 증명은 [관련 논문](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf)에서 확인하실 수 있습니다.
        """
    },
    'en': {
        'app_title': "💡 AI Service Business Case Simulator (v5.5)",
        'app_subtitle': "Analyze the profitability of user segments and overall business viability by adjusting tech and pricing strategies.",
        'sidebar_title': "⚙️ Scenario Input Variables",
        'lang_selector_label': "Language",

        'section_1_header': "1. Financial Goals",
        'target_irr_label': "Target IRR (%)",
        'target_irr_help': "The minimum annual rate of return you want to achieve. This sets the basis for all cost calculations.",

        'section_2_header': "2. Tech & Infrastructure Strategy",
        'hw_ratio_label': "Hardware Portfolio (High-Perf GPU %)",
        'hw_ratio_help': "High-performance chips are more efficient but more expensive. Low-cost chips are the opposite. Choose the optimal mix for your workload.",
        'electricity_label': "Electricity Pricing Scenario",
        'electricity_help': "'Standard Grid' assumes typical industrial rates. 'Net-Zero PPA' assumes a more expensive Power Purchase Agreement for 100% renewable energy.",
        'standard_grid': "Standard Grid",
        'net_zero_ppa': "Net-Zero (Carbon Free)",
        'arch_toggle_label': "Apply Advanced Architecture (Optional)",
        'arch_toggle_help': "Assumes an intelligent architecture that optimizes AI workloads, reducing the total computation required and thus increasing efficiency with the same hardware.",

        'section_3_header': "3. Service Pricing Strategy",
        'paid_tier_fee_label': "Paid Tier Monthly Fee ($)",
        'paid_tier_fee_help': "Set the monthly fee for standard paid users.",
        'premium_tier_fee_label': "Premium Tier Monthly Fee ($)",
        'premium_tier_fee_help': "Set the monthly fee for high-usage premium users.",

        'run_button_label': "🚀 Run Analysis",
        'results_header': "📊 Scenario Analysis Results",
        'spinner_text': "Running analysis...",
        'initial_prompt': "Adjust variables in the sidebar and click 'Run Analysis'.",

        'output_section_A_title': "A. Cost Basis Analysis",
        'annual_revenue_label': "Break-Even Annual Revenue (for IRR)",
        'token_price_label': "Cost per Token ($ / 1M tokens)",

        'output_section_B_title': "B. Per-User Profitability Analysis (Pricing Model Check)",
        'user_tier_header': "User Tier",
        'free_tier': "Free Users",
        'paid_tier': "Paid Users",
        'premium_tier': "Premium Users",
        'monthly_usage_label': "Monthly Usage",
        'monthly_cost_label': "Monthly Cost",
        'monthly_revenue_label': "Monthly Revenue",
        'monthly_profit_label': "Monthly Profit/Loss",
        'profit_status_profit': "Profit",
        'profit_status_loss': "Loss",

        'paradox_explanation_title': "💡 Analysis: Why is Per-User Profit High but Overall Payback Negative?",
        'paradox_explanation_text': """
        **The fact that individual users are profitable while the overall business is not recoverable is not a bug; it's the simulator accurately highlighting a critical business dilemma.**

        - **Analysis B (Pricing Model):** This section answers, "If our business were to succeed (covering all costs), is our pricing for each user profitable against its marginal cost?" The answer is yes. Your paying customers are charged much more than they cost to serve, meaning your **pricing policy is sound.**

        - **Analysis C (Business Model):** This section answers, "Can the total revenue from our few paying customers cover the losses from many free users AND the massive initial investment?" The answer is no. The percentage of paying users is too low to cover the enormous total costs, meaning your **overall business model is likely to fail.**
        """,

        'output_section_C_title': "C. Final Business Viability (incl. Initial Investment)",
        'payback_period_label': "Overall Investment Payback Period",
        'payback_inf': "Not Recoverable",
        'years_suffix': "Years",
        'years_suffix_projected': "Years (Projected)",

        'footnote_title': "※ Note on the 'Advanced Architecture' Effect",
        'footnote_text': """
        * **Hypothesis-Based:** The effect of the 'Advanced Architecture' is based on the hypothesis of eliminating resource waste by intelligently selecting optimized models for specific tasks.
        * **Source:** The mathematical proof for this hypothesis can be found in the [accompanying paper](https://github.com/HWAN-OH/AI-DC-TCO-Strategy-Simulator/blob/main/paper/A%20Mathematical%20Proof%20of%20the%20Computational%20and%20Energy%20Efficiency%20of%20the%20MirrorMind%20Architecture.pdf).
        """
    }
}
