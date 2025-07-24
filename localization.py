# localization.py (v14.0)

loc_strings = {
    "en": {
        "app_title": "AI Datacenter Business Simulator",
        "app_subtitle": "A strategic tool to analyze the profitability of AI services based on infrastructure and business models.",
        "sidebar_guide_title": "📖 How to Use",
        "sidebar_guide_text": """
        1.  **Set Key Variables**: Adjust the sliders and options below to define your business scenario.
        2.  **Run Analysis**: Click the 'Run Analysis' button.
        3.  **Review Results**: Analyze the P&L statements for strategic insights.
        """,
        "copyright_text": "© 2025, Oh Sunghwan. All rights reserved.",
        "contact_text": "Contact: hawn21@gmail.com",
        
        "lang_selector": "Language",
        "dc_capacity": "Data Center Size (MW)",
        "high_perf_gpu_ratio": "High-Performance GPU Budget Ratio (%)",
        "power_type": "Power Source",
        "apply_mirrormind": "Apply Intelligent Architecture",
        "paid_tier_fee": "Paid Tier Monthly Fee ($)",
        "premium_tier_multiplier": "Premium Tier Price Multiplier (vs Paid)",

        "run_button": "🚀 Run Analysis",
        "results_header": "Analysis Results",
        "initial_prompt": "Set your scenario variables in the sidebar and click 'Run Analysis'.",

        "section_1_title": "1. Overall Business P&L (Annual)",
        "assumptions_title": "Key Assumptions & Capacity",
        "assump_gpu_mix": "GPU Configuration",
        "assump_users": "Supported Users",
        "assump_tokens": "Tokens Serviced",
        "assump_power": "Power Consumed",
        "pnl_table_title": "Annual P&L",
        "pnl_item": "Item",
        "pnl_amount": "Amount ($)",
        "pnl_revenue": "Revenue",
        "pnl_cost": "Cost",
        "pnl_profit": "Profit",

        "section_2_title": "2. Per-User P&L and Cost Structure",
        "tier_free": "Free Users",
        "tier_standard": "Paid Users",
        "tier_premium": "Premium Users",
        "segment_pnl_header": "P&L by Customer Segment",
        "col_segment": "Customer Segment",
        "col_total_revenue": "Total Revenue",
        "col_total_cost": "Total Cost",
        "col_total_profit": "Total Profit",
        "col_per_user_revenue": "Revenue/User",
        "col_per_user_cost": "Cost/User",
        "col_per_user_profit": "Profit/User",
        
        "payback_title": "Investment Payback Period",
        "payback_years": "Estimated Payback Years",
        "unrecoverable": "Unrecoverable",

        "power_conventional": "Conventional",
        "power_renewable": "Renewable",
    },
    "ko": {
        "app_title": "AI 데이터센터 사업성 시뮬레이터",
        "app_subtitle": "인프라와 비즈니스 모델에 따른 AI 서비스의 수익성을 분석하는 전략 도구입니다.",
        "sidebar_guide_title": "📖 사용 방법",
        "sidebar_guide_text": """
        1.  **핵심 변수 설정**: 아래의 슬라이더와 옵션을 조절하여 비즈니스 시나리오를 정의합니다.
        2.  **분석 실행**: '분석 실행' 버튼을 클릭합니다.
        3.  **결과 검토**: 손익계산서를 분석하여 전략적 인사이트를 얻으세요.
        """,
        "copyright_text": "© 2025, Oh Sunghwan. All rights reserved.",
        "contact_text": "문의: hawn21@gmail.com",
        "lang_selector": "언어",
        "dc_capacity": "데이터센터 용량 (MW)",
        "high_perf_gpu_ratio": "고성능 GPU 예산 비중 (%)",
        "power_type": "전력 종류",
        "apply_mirrormind": "지능형 아키텍처 적용",
        "paid_tier_fee": "유료 사용자 월 요금 ($)",
        "premium_tier_multiplier": "프리미엄 요금 배수 (유료 대비)",

        "run_button": "🚀 분석 실행",
        "results_header": "분석 결과",
        "initial_prompt": "사이드바에서 시나리오 변수를 설정한 후 '분석 실행' 버튼을 눌러 결과를 확인하세요.",

        "section_1_title": "1. 전체 사업 손익 (연간 기준)",
        "assumptions_title": "주요 가정 및 생산량",
        "assump_gpu_mix": "그래픽카드 구성",
        "assump_users": "서비스 가능 고객",
        "assump_tokens": "처리 토큰 총량",
        "assump_power": "소비 전력 총량",
        "pnl_table_title": "연간 손익계산서",
        "pnl_item": "항목",
        "pnl_amount": "금액 ($)",
        "pnl_revenue": "매출",
        "pnl_cost": "비용",
        "pnl_profit": "이익",

        "section_2_title": "2. 인당 손익 및 원가 구조",
        "tier_free": "무료 사용자",
        "tier_standard": "유료 사용자",
        "tier_premium": "프리미엄 사용자",
        "segment_pnl_header": "고객 그룹별 손익 분석",
        "col_segment": "고객 그룹",
        "col_total_revenue": "그룹 전체 매출",
        "col_total_cost": "그룹 전체 비용",
        "col_total_profit": "그룹 전체 손익",
        "col_per_user_revenue": "인당 매출",
        "col_per_user_cost": "인당 비용",
        "col_per_user_profit": "인당 손익",
        
        "payback_title": "투자금 회수 기간",
        "payback_years": "예상 회수 기간 (년)",
        "unrecoverable": "회수 불가",

        "power_conventional": "일반 전력망",
        "power_renewable": "재생에너지",
    }
}

def t(key, lang="ko", **kwargs):
    return loc_strings.get(lang, {}).get(key, key).format(**kwargs)
