# localization.py
# UI 텍스트를 위한 한/영 문자열 저장소 (AI 수익성 모델)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 서비스 수익성 시뮬레이터",
        'app_subtitle': "클라우드 및 온프레미스 운영 모델에 따른 AI 서비스의 목표 수익률(IRR) 달성을 위한 필요 요금 수준을 분석합니다.",
        'sidebar_title': "⚙️ 시나리오 구성",
        'lang_selector_label': "언어 (Language)",
        'section_1_header': "1. 인프라 운영 모델 선택",
        'infra_mode_label': "운영 모델",
        'infra_mode_cloud': "클라우드 기반",
        'infra_mode_on_premise': "온프레미스 (자체 구축)",
        
        'expander_assumptions_title': "핵심 가정 보기",
        'assumptions_financial': "재무 가정",
        'assumptions_analysis_years': "분석 기간",
        'assumptions_target_irr': "목표 IRR",
        'assumptions_model': "모델 가정",
        'assumptions_training_cost': "훈련 비용",
        'assumptions_user': "사용자 가정",
        'assumptions_total_users': "총 사용자 수",
        'assumptions_user_dist': "사용자 비중 (무료/저사용/고사용)",
        'assumptions_pricing_ratio': "요금 비율 (고사용자:저사용자)",
        
        'run_button_label': "🚀 수익성 분석 실행",
        'spinner_text': "수익성 분석 중...",
        
        'results_header': "📊 분석 결과",
        'results_for_model': "{model_name} 모델",
        'tco_metric_label': "총 투자비의 현재가치 (PV)",
        'revenue_metric_label': "목표 IRR 달성 위한 월 필요매출",
        'low_tier_fee_label': "저사용자 월 요금",
        'high_tier_fee_label': "고사용자 월 요금",
        
        'methodology_title': "※ 분석 방법론에 대한 참고",
        'methodology_text': """
        본 시뮬레이터는 투자 결정의 표준 방식인 **현금흐름할인(DCF) 모델**을 사용합니다. 이는 미래에 발생할 비용과 수익의 가치를 현재 시점으로 할인하여 '돈의 시간 가치'를 반영하는 방식입니다. 따라서 모든 비용(초기 투자, 운영비 등)의 현재가치(PV) 합계를 계산한 후, 이 총 투자 가치를 회수하고 목표 IRR을 달성하기 위해 필요한 미래 매출을 역산합니다. 이는 회계적 비용(감가상각 등)을 사용한 단순 합산보다 더 정확한 사업성 분석을 제공합니다.
        """
    },
    'en': {
        'app_title': "💡 AI Service Profitability Simulator",
        'app_subtitle': "Analyze the required pricing levels to achieve a target IRR for AI services under Cloud and On-Premise operation models.",
        'sidebar_title': "⚙️ Configure Scenario",
        'lang_selector_label': "Language",
        'section_1_header': "1. Select Infrastructure Model",
        'infra_mode_label': "Operation Model",
        'infra_mode_cloud': "Cloud-Based",
        'infra_mode_on_premise': "On-Premise",
        
        'expander_assumptions_title': "View Key Assumptions",
        'assumptions_financial': "Financial Assumptions",
        'assumptions_analysis_years': "Analysis Period",
        'assumptions_target_irr': "Target IRR",
        'assumptions_model': "Model Assumptions",
        'assumptions_training_cost': "Training Cost",
        'assumptions_user': "User Assumptions",
        'assumptions_total_users': "Total Users",
        'assumptions_user_dist': "User Distribution (Free/Low/High)",
        'assumptions_pricing_ratio': "Pricing Ratio (High:Low Tier)",
        
        'run_button_label': "🚀 Run Profitability Analysis",
        'spinner_text': "Analyzing profitability...",
        
        'results_header': "📊 Analysis Results",
        'results_for_model': "for {model_name} Model",
        'tco_metric_label': "Present Value (PV) of Total Investment",
        'revenue_metric_label': "Required Monthly Revenue for Target IRR",
        'low_tier_fee_label': "Low-Tier Monthly Fee",
        'high_tier_fee_label': "High-Tier Monthly Fee",
        
        'methodology_title': "※ Note on Analysis Methodology",
        'methodology_text': """
        This simulator uses the standard **Discounted Cash Flow (DCF) model** for investment analysis. This method reflects the 'time value of money' by discounting future costs and revenues to their present value. We first calculate the total present value (PV) of all costs (initial investment, operating expenses, etc.). Then, we determine the future revenue required to recover this total investment value and achieve the target IRR. This provides a more accurate business viability analysis than a simple summation of accounting costs (like depreciation).
        """
    }
}
