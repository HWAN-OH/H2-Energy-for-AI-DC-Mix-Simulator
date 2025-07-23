# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v7.0)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 사업성 시뮬레이터 (v7.0)",
        'app_subtitle': "기술/가격 전략에 따른 전체 사업 및 개별 사용자 단위의 손익(P&L)을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 입력 변수",
        'lang_selector_label': "언어 (Language)",

        'section_2_header': "1. 기술 및 인프라 전략",
        'hw_ratio_label': "하드웨어 포트폴리오 (고사양 GPU 비중)",
        'hw_ratio_help': "고성능 칩은 단위 효율이 높지만 비쌉니다. 저비용 칩은 그 반대입니다. 워크로드에 맞는 최적의 조합을 선택하세요.",
        'electricity_label': "전력 가격 시나리오",
        'electricity_help': "'표준 전력망'은 일반적인 산업용 요금을, '넷제로'는 100% 재생에너지 사용을 위한 더 비싼 장기계약(PPA) 요금을 가정합니다.",
        'standard_grid': "표준 전력망",
        'net_zero_ppa': "넷제로 (탄소중립)",
        'arch_toggle_label': "고급 아키텍처 적용 (선택)",
        'arch_toggle_help': "AI 워크로드를 최적화하는 지능형 아키텍처 도입을 가정합니다. 총 필요 연산량을 줄여 동일 하드웨어로 더 높은 효율을 달성하는 효과를 분석할 수 있습니다.",

        'section_3_header': "2. 서비스 가격 전략",
        'paid_tier_fee_label': "유료 사용자 월 요금 ($)",
        'paid_tier_fee_help': "표준 유료 사용자에게 청구할 월 요금을 설정합니다.",
        'premium_tier_fee_label': "프리미엄 사용자 월 요금 ($)",
        'premium_tier_fee_help': "고사용량 프리미엄 사용자에게 청구할 월 요금을 설정합니다.",

        'run_button_label': "🚀 분석 실행",
        'results_header': "📊 시나리오 분석 결과",
        'spinner_text': "시나리오 분석 중입니다...",
        'initial_prompt': "사이드바에서 변수를 조정한 후 '분석 실행' 버튼을 클릭하세요.",

        'output_section_A_title': "A. 연간 손익계산서 (P&L, 5년차 기준)",
        'pnl_revenue': "매출",
        'pnl_cost_of_revenue': "매출원가 (운영비)",
        'pnl_gross_profit': "매출총이익",
        'pnl_operating_expenses': "영업비용 (상각비)",
        'pnl_operating_profit': "영업이익",

        'output_section_B_title': "B. 개별 사용자 월간 손익 (P&L)",
        'free_tier': "무료 사용자",
        'paid_tier': "유료 사용자",
        'premium_tier': "프리미엄 사용자",
        'pnl_user_revenue': "월 매출",
        'pnl_user_cost': "월 총원가",
        'pnl_user_profit': "월 영업이익",
    },
    'en': {
        'app_title': "💡 AI Service Business Case Simulator (v7.0)",
        'app_subtitle': "Analyze the full business and per-user Profit & Loss (P&L) based on your tech and pricing strategies.",
        'sidebar_title': "⚙️ Scenario Input Variables",
        'lang_selector_label': "Language",

        'section_2_header': "1. Tech & Infrastructure Strategy",
        'hw_ratio_label': "Hardware Portfolio (High-Perf GPU %)",
        'hw_ratio_help': "High-performance chips are more efficient but more expensive. Low-cost chips are the opposite. Choose the optimal mix for your workload.",
        'electricity_label': "Electricity Pricing Scenario",
        'electricity_help': "'Standard Grid' assumes typical industrial rates. 'Net-Zero PPA' assumes a more expensive Power Purchase Agreement for 100% renewable energy.",
        'standard_grid': "Standard Grid",
        'net_zero_ppa': "Net-Zero (Carbon Free)",
        'arch_toggle_label': "Apply Advanced Architecture (Optional)",
        'arch_toggle_help': "Assumes an intelligent architecture that optimizes AI workloads, reducing the total computation required and thus increasing efficiency with the same hardware.",

        'section_3_header': "2. Service Pricing Strategy",
        'paid_tier_fee_label': "Paid Tier Monthly Fee ($)",
        'paid_tier_fee_help': "Set the monthly fee for standard paid users.",
        'premium_tier_fee_label': "Premium Tier Monthly Fee ($)",
        'premium_tier_fee_help': "Set the monthly fee for high-usage premium users.",

        'run_button_label': "🚀 Run Analysis",
        'results_header': "📊 Scenario Analysis Results",
        'spinner_text': "Running analysis...",
        'initial_prompt': "Adjust variables in the sidebar and click 'Run Analysis'.",

        'output_section_A_title': "A. Annual Profit & Loss Statement (P&L, based on Year 5)",
        'pnl_revenue': "Revenue",
        'pnl_cost_of_revenue': "Cost of Revenue (Operating Costs)",
        'pnl_gross_profit': "Gross Profit",
        'pnl_operating_expenses': "Operating Expenses (D&A)",
        'pnl_operating_profit': "Operating Profit",

        'output_section_B_title': "B. Per-User Monthly P&L",
        'free_tier': "Free Users",
        'paid_tier': "Paid Users",
        'premium_tier': "Premium Users",
        'pnl_user_revenue': "Monthly Revenue",
        'pnl_user_cost': "Monthly Full Cost",
        'pnl_user_profit': "Monthly Operating Profit",
    }
}
