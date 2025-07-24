# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v11.0)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 경영 대시보드 (v11.0)",
        'app_subtitle': "핵심 전략 변수를 조절하여, AI 서비스의 전체 손익과 사업 타당성을 분석합니다.",
        'sidebar_title': "⚙️ 핵심 전략 변수",
        
        'section_tech_strategy': "1. 기술 전략",
        'hw_ratio_label': "고사양 GPU 예산 비중 (%)",
        'hw_ratio_help': "전체 IT 예산 중, 고성능 GPU에 투자할 비중을 결정합니다. 이는 데이터센터의 총 연산 성능과 직결됩니다.",
        'arch_toggle_label': "지능형 아키텍처 적용",
        'arch_toggle_help': "AI 워크로드를 최적화하여, 동일 성능으로 더 많은 사용자를 지원하거나 비용을 절감하는 효과를 시뮬레이션합니다.",

        'section_financial_strategy': "2. 재무 및 운영",
        'electricity_label': "전력 시나리오",
        'electricity_help': "'표준 전력망'은 일반 산업용 요금을, '탄소중립'은 재생에너지 사용을 위한 프리미엄 요금을 가정합니다.",
        'standard_grid': "표준 전력망",
        'net_zero_ppa': "탄소중립 (Net-Zero)",

        'run_button_label': "🚀 대시보드 생성",
        'results_header': "📊 경영 대시보드",
        'initial_prompt': "좌측 사이드바에서 핵심 전략 변수를 조정한 후 '대시보드 생성' 버튼을 클릭하세요.",

        'section_A_title': "A. 전체 사업 손익 (연간 P&L)",
        'pnl_revenue': "매출",
        'pnl_gross_profit': "매출총이익",
        'pnl_opex': "영업비용 (판관비+상각비)",
        'pnl_profit': "영업이익",

        'section_B_title': "B. 고객 그룹별 손익 (인당 월간 P&L)",
        'free_tier': "무료 사용자",
        'paid_tier': "유료 사용자",
        'premium_tier': "프리미엄 사용자",
        'user_pnl_usage': "월 사용량",
        'user_pnl_cost': "총원가",
        'user_pnl_revenue': "매출",
        'user_pnl_profit': "손익",

        'section_C_title': "C. 손익분기점 분석",
        'breakeven_payback': "투자 회수 기간",
        'payback_inf': "회수 불가",
        'years_suffix': "년",

        'section_D_title': "D. AI 기반 전략 제언",
        'reco_profit_positive': "👍 현재 전략은 수익성이 있습니다. 가동률을 높이거나, 저비용 GPU 비중을 조절하여 수익을 극대화하는 방안을 검토하세요.",
        'reco_profit_negative': "🔥 현재 전략은 적자입니다. 아래의 제언을 검토하여 수익성을 개선해야 합니다.",
        'reco_arch_off': "⚠️ [비용] 지능형 아키텍처를 적용하여 총 필요 연산량을 줄이는 것이 가장 효과적인 비용 절감 수단입니다.",
        'reco_util_low': "📈 [매출] 데이터센터 가동률을 높여 유휴 자원을 최소화하고 매출을 증대시켜야 합니다.",
        'reco_price_increase': "💰 [매출] 현재의 비용 구조를 감당하기 위해 유료/프리미엄 사용자 요금 인상을 검토할 수 있습니다."
    },
    'en': {
        'app_title': "💡 AI Service Executive Dashboard (v11.0)",
        'app_subtitle': "Analyze the overall P&L and business viability of your AI service by adjusting key strategic variables.",
        'sidebar_title': "⚙️ Key Strategic Variables",
        
        'section_tech_strategy': "1. Technology Strategy",
        'hw_ratio_label': "High-Performance GPU Budget Ratio (%)",
        'hw_ratio_help': "Determines the investment allocation for high-performance GPUs, directly impacting the datacenter's total computational power.",
        'arch_toggle_label': "Apply Intelligent Architecture",
        'arch_toggle_help': "Simulates the effect of optimizing AI workloads to support more users or reduce costs with the same hardware.",

        'section_financial_strategy': "2. Finance & Operations",
        'electricity_label': "Electricity Scenario",
        'electricity_help': "'Standard Grid' assumes typical industrial rates. 'Net-Zero' assumes premium rates for renewable energy.",
        'standard_grid': "Standard Grid",
        'net_zero_ppa': "Net-Zero",

        'run_button_label': "🚀 Generate Dashboard",
        'results_header': "📊 Executive Dashboard",
        'initial_prompt': "Adjust the strategic variables in the sidebar, then click 'Generate Dashboard'.",

        'section_A_title': "A. Overall Business P&L (Annual)",
        'pnl_revenue': "Revenue",
        'pnl_gross_profit': "Gross Profit",
        'pnl_opex': "Operating Expenses (SG&A + D&A)",
        'pnl_profit': "Operating Profit",

        'section_B_title': "B. Per-User Segment P&L (Monthly)",
        'free_tier': "Free Users",
        'paid_tier': "Paid Users",
        'premium_tier': "Premium Users",
        'user_pnl_usage': "Usage",
        'user_pnl_cost': "Fully-Loaded Cost",
        'user_pnl_revenue': "Revenue",
        'user_pnl_profit': "Profit/Loss",

        'section_C_title': "C. Break-Even Analysis",
        'breakeven_payback': "Payback Period",
        'payback_inf': "Not Recoverable",
        'years_suffix': "Years",

        'section_D_title': "D. AI-Powered Strategic Recommendations",
        'reco_profit_positive': "👍 The current strategy is profitable. Consider increasing utilization or optimizing the low-cost GPU ratio to maximize profit.",
        'reco_profit_negative': "🔥 The current strategy is unprofitable. Review the recommendations below to improve profitability.",
        'reco_arch_off': "⚠️ [Cost] Applying intelligent architecture is the most effective way to reduce costs by lowering total computational demand.",
        'reco_util_low': "📈 [Revenue] Increase datacenter utilization to minimize idle resources and boost revenue.",
        'reco_price_increase': "💰 [Revenue] Consider increasing paid/premium tier prices to cover the current cost structure."
    }
}
