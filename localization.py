# localization.py

loc_strings = {
    "en": {
        "dc_capacity": "Data Center Size (MW)",
        "power_type": "Power Source",
        "target_irr": "Target IRR (%)",
        "apply_mirrormind": "Apply MirrorMind Architecture",
        "summary_title": "Business Summary",
        "per_user_analysis": "Per-User Profitability Analysis",
        "break_even_analysis": "Break-even User Estimate",
        "recommendations": "Strategic Recommendations"
    },
    "ko": {
        "dc_capacity": "데이터센터 용량 (MW)",
        "power_type": "전력 종류",
        "target_irr": "목표 IRR (%)",
        "apply_mirrormind": "미러마인드 적용 여부",
        "summary_title": "사업 요약",
        "per_user_analysis": "사용자별 수익성 분석",
        "break_even_analysis": "손익분기점 사용자 수",
        "recommendations": "전략적 제언"
    }
}

# 문자열 조회 함수 추가
def translate(key, lang="en"):
    return loc_strings.get(lang, {}).get(key, key)
