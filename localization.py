# localization.py (v12.0)

loc_strings = {
    "en": {
        "app_title": "AI Datacenter Business Simulator",
        "app_subtitle": "A strategic tool to analyze the profitability of AI services based on infrastructure and business models.",
        
        "sidebar_guide_title": "📖 How to Use",
        "sidebar_guide_text": """
        1.  **Set Key Variables**: Adjust the sliders and options on the left to define your business scenario.
        2.  **Run Analysis**: Click the 'Run Analysis' button on the main screen.
        3.  **Review Results**: Analyze the comprehensive P&L statements for both the entire business and individual users to gain strategic insights.
        """,
        
        "copyright_text": "© 2025, Oh Sunghwan. All rights reserved.",
        "contact_text": "Contact: hawn21@gmail.com",
        
        "lang_selector": "Language",
        "dc_capacity": "Data Center Size (MW)",
        "power_type": "Power Source",
        "target_irr": "Target IRR (%)",
        "apply_mirrormind": "Apply Intelligent Architecture",
        "run_button": "🚀 Run Analysis",
        
        "results_header": "Analysis Results",
        "initial_prompt": "Set your scenario variables in the sidebar and click 'Run Analysis' to see the results.",

        "pnl_annual_title": "Annual P&L (based on {dc_size}MW DC)",
        "pnl_per_user_title": "Per-User Annual P&L",
        
        "pnl_item": "Item",
        "pnl_total_amount": "Total Amount ($)",
        "pnl_per_user_amount": "Amount per User ($)",
        
        "pnl_revenue": "Revenue",
        "pnl_cost": "Cost",
        "pnl_profit": "Profit",
        
        "breakeven_title": "Break-Even Analysis",
        "breakeven_users": "Break-Even Point (Users)",
        
        "recommendations_title": "Strategic Recommendations",
    },
    "ko": {
        "app_title": "AI 데이터센터 사업성 시뮬레이터",
        "app_subtitle": "인프라와 비즈니스 모델에 따른 AI 서비스의 수익성을 분석하는 전략 도구입니다.",

        "sidebar_guide_title": "📖 사용 방법",
        "sidebar_guide_text": """
        1.  **핵심 변수 설정**: 왼쪽 사이드바의 슬라이더와 옵션을 조절하여 비즈니스 시나리오를 정의합니다.
        2.  **분석 실행**: 메인 화면의 '분석 실행' 버튼을 클릭합니다.
        3.  **결과 검토**: 전체 사업 및 개별 사용자 단위의 종합 손익계산서를 분석하여 전략적 인사이트를 얻으세요.
        """,

        "copyright_text": "© 2025, Oh Sunghwan. All rights reserved.",
        "contact_text": "문의: hawn21@gmail.com",

        "lang_selector": "언어",
        "dc_capacity": "데이터센터 용량 (MW)",
        "power_type": "전력 종류",
        "target_irr": "목표 IRR (%)",
        "apply_mirrormind": "지능형 아키텍처 적용",
        "run_button": "🚀 분석 실행",
        
        "results_header": "분석 결과",
        "initial_prompt": "사이드바에서 시나리오 변수를 설정한 후 '분석 실행' 버튼을 눌러 결과를 확인하세요.",

        "pnl_annual_title": "연간 손익계산서 ({dc_size}MW 데이터센터 기준)",
        "pnl_per_user_title": "사용자 1인당 연간 손익계산서",

        "pnl_item": "항목",
        "pnl_total_amount": "총 금액 ($)",
        "pnl_per_user_amount": "사용자당 금액 ($)",

        "pnl_revenue": "매출",
        "pnl_cost": "비용",
        "pnl_profit": "이익",
        
        "breakeven_title": "손익분기점 분석",
        "breakeven_users": "손익분기점 (사용자 수)",
        
        "recommendations_title": "전략적 제언",
    }
}

def t(key, lang="ko", **kwargs):
    """Translates a key for a given language and formats it."""
    return loc_strings.get(lang, {}).get(key, key).format(**kwargs)
