# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v10.0)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 경영 대시보드 (v10.0)",
        'app_subtitle': "핵심 전략 변수를 조절하여, AI 서비스의 전체 손익과 사업 타당성을 분석합니다.",
        'sidebar_title': "⚙️ 핵심 전략 변수",
        
        'section_tech_strategy': "1. 기술 전략",
        'hw_ratio_label': "고사양 GPU 예산 비중 (%)",
        'hw_ratio_help': "전체 IT 예산 중, 고성능 GPU에 투자할 비중을 결정합니다. 이는 데이터센터의 총 연산 성능과 직결됩니다.",
        'arch_toggle_label': "지능형 아키텍처 적용",
        'arch_toggle_help': "AI 워크로드를 최적화하여, 동일 성능으로 더 많은 사용자를 지원하거나 비용을 절감하는 효과를 시뮬레이션합니다.",

        'section_financial_strategy': "2. 재무 및 운영",
        'target_irr_label': "목표 내부수익률 (IRR, %)",
        'target_irr_help': "이 프로젝트를 통해 달성하고자 하는 최소 연평균 수익률입니다. 현재 버전에서는 직접적인 계산보다 전략적 목표로 사용됩니다.",
        'electricity_label': "전력 시나리오",
        'electricity_help': "'표준 전력망'은 일반 산업용 요금을, '탄소중립'은 재생에너지 사용을 위한 프리미엄 요금을 가정합니다.",
        'standard_grid': "표준 전력망",
        'net_zero_ppa': "탄소중립 (Net-Zero)",

        'run_button_label': "🚀 대시보드 생성",
        'results_header': "📊 경영 대시보드",
        'initial_prompt': "좌측 사이드바에서 핵심 전략 변수를 조정한 후 '대시보드 생성' 버튼을 클릭하세요.",

        'section_A_title': "A. 전체 사업 손익 (연간 P&L)",
        'pnl_revenue': "총 매출",
        'pnl_cost': "총 비용 (운영비+상각비)",
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
        'breakeven_users': "손익분기 사용자 수",
        'payback_inf': "회수 불가",
        'users_inf': "달성 불가",
        'years_suffix': "년",

        'section_D_title': "D. AI 기반 전략 제언",
        'reco_cost_title': "비용 절감 방안",
        'reco_revenue_title': "매출 증대 방안",
        'reco_arch_on': "✅ 지능형 아키텍처를 적용하여 비용 효율성을 극대화하세요. 동일 하드웨어로 더 많은 사용자를 지원할 수 있습니다.",
        'reco_arch_off': "⚠️ 지능형 아키텍처 미적용은 가장 큰 비용 절감 기회를 놓치는 것일 수 있습니다. 적용 시의 효과를 비교해보세요.",
        'reco_hw_balance': "💡 하드웨어 포트폴리오 최적화: 현재 고사양 GPU 비중이 높습니다. 워크로드에 따라 저비용 GPU를 혼합하여 전체 TCO를 절감할 수 있는지 검토하세요.",
        'reco_price_increase': "📈 요금 인상 고려: 현재의 비용 구조를 감당하기 위해 유료/프리미엄 사용자 요금 인상을 검토할 수 있습니다.",
        'reco_all_good': "👍 현재 전략은 모든 면에서 균형 잡혀 있습니다. 시장 상황 변화에 지속적으로 주의를 기울이세요."
    },
    'en': {
        'app_title': "💡 AI Service Executive Dashboard (v10.0)",
        'app_subtitle': "Analyze the overall P&L and business viability of your AI service by adjusting key strategic variables.",
        'sidebar_title': "⚙️ Key Strategic Variables",
        
        'section_tech_strategy': "1. Technology Strategy",
        'hw_ratio_label': "High-Performance GPU Budget Ratio (%)",
        'hw_ratio_help': "Determines the investment allocation for high-performance GPUs, directly impacting the datacenter's total computational power.",
        'arch_toggle_label': "Apply Intelligent Architecture",
        'arch_toggle_help': "Simulates the effect of optimizing AI workloads to support more users or reduce costs with the same hardware.",

        'section_financial_strategy': "2. Finance & Operations",
        'target_irr_label': "Target IRR (%)",
        'target_irr_help': "The minimum annual rate of return for this project. Used as a strategic target in this version.",
        'electricity_label': "Electricity Scenario",
        'electricity_help': "'Standard Grid' assumes typical industrial rates. 'Net-Zero' assumes premium rates for renewable energy.",
        'standard_grid': "Standard Grid",
        'net_zero_ppa': "Net-Zero",

        'run_button_label': "🚀 Generate Dashboard",
        'results_header': "📊 Executive Dashboard",
        'initial_prompt': "Adjust the strategic variables in the sidebar, then click 'Generate Dashboard'.",

        'section_A_title': "A. Overall Business P&L (Annual)",
        'pnl_revenue': "Total Revenue",
        'pnl_cost': "Total Cost (OpEx + D&A)",
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
        'breakeven_users': "Break-Even Users",
        'payback_inf': "Not Recoverable",
        'users_inf': "Unachievable",
        'years_suffix': "Years",

        'section_D_title': "D. AI-Powered Strategic Recommendations",
        'reco_cost_title': "Cost Reduction",
        'reco_revenue_title': "Revenue Enhancement",
        'reco_arch_on': "✅ Apply Intelligent Architecture to maximize cost efficiency. It allows supporting more users with the same hardware.",
        'reco_arch_off': "⚠️ Not applying Intelligent Architecture could be a missed opportunity for significant cost savings. Compare the effect of applying it.",
        'reco_hw_balance': "💡 Optimize Hardware Portfolio: The current high-perf GPU ratio is high. Consider a hybrid model with low-cost GPUs to potentially lower TCO depending on the workload.",
        'reco_price_increase': "📈 Consider Price Increase: To cover the current cost structure, a review of the paid/premium tier pricing may be necessary.",
        'reco_all_good': "👍 The current strategy appears well-balanced. Continue to monitor market conditions."
    }
}
