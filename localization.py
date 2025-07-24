# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (v8.0)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 데이터센터 사업성 시뮬레이터 (v8.0)",
        'app_subtitle': "하드웨어 포트폴리오 전략이 성능, 단위 원가, 그리고 최종 수익성에 미치는 영향을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 입력 변수",
        'lang_selector_label': "언어 (Language)",

        'section_hw_header': "하드웨어 포트폴리오 전략",
        'hw_ratio_label': "고사양 GPU 예산 비중 (%)",
        'hw_ratio_help': "전체 IT 하드웨어 예산 중, 고성능 GPU에 얼마를 투자할지 결정합니다. 이는 데이터센터의 총 연산 성능을 좌우합니다.",
        
        'run_button_label': "🚀 분석 실행",
        'results_header': "📊 시나리오 분석 결과",
        'spinner_text': "시나리오 분석 중입니다...",
        'initial_prompt': "좌측 사이드바에서 하드웨어 예산 비중을 조정한 후 '분석 실행' 버튼을 클릭하세요.",

        'section_A_title': "A. 하드웨어 투자 및 성능 분석",
        'metric_hw_investment': "총 IT 하드웨어 예산",
        'metric_performance_score': "총 연산 성능 점수",
        'metric_token_capacity': "연간 총 토큰 처리 용량",
        
        'section_B_title': "B. 비용 구조 및 단위 원가 분석",
        'metric_annual_cost': "총 연간 비용",
        'metric_cost_per_token': "토큰당 총원가 ($ / 1M)",
        
        'section_C_title': "C. 최종 수익성 분석 (P&L)",
        'metric_users_supported': "최대 지원 가능 사용자",
        'metric_annual_revenue': "예상 연간 매출",
        'metric_operating_profit': "예상 연간 영업이익",
    },
    'en': {
        'app_title': "💡 AI Datacenter Business Case Simulator (v8.0)",
        'app_subtitle': "Analyze how hardware portfolio strategy impacts performance, unit cost, and final profitability.",
        'sidebar_title': "⚙️ Scenario Input Variables",
        'lang_selector_label': "Language",

        'section_hw_header': "Hardware Portfolio Strategy",
        'hw_ratio_label': "High-Performance GPU Budget Ratio (%)",
        'hw_ratio_help': "Determines how much of the total IT hardware budget is allocated to high-performance GPUs. This dictates the total computational performance of the datacenter.",

        'run_button_label': "🚀 Run Analysis",
        'results_header': "📊 Scenario Analysis Results",
        'spinner_text': "Running analysis...",
        'initial_prompt': "Adjust the hardware budget ratio in the sidebar, then click 'Run Analysis'.",

        'section_A_title': "A. Hardware Investment & Performance Analysis",
        'metric_hw_investment': "Total IT Hardware Budget",
        'metric_performance_score': "Total Performance Score",
        'metric_token_capacity': "Annual Token Throughput Capacity",

        'section_B_title': "B. Cost Structure & Unit Cost Analysis",
        'metric_annual_cost': "Total Annual Cost",
        'metric_cost_per_token': "Fully Loaded Cost per 1M Tokens",

        'section_C_title': "C. Final Profitability Analysis (P&L)",
        'metric_users_supported': "Max Users Supported",
        'metric_annual_revenue': "Projected Annual Revenue",
        'metric_operating_profit': "Projected Annual Operating Profit",
    }
}
