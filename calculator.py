# calculator_v12.py

def calculate_business_case(dc_size_mw, use_clean_power, target_irr, apply_mirrormind, lang):
    """
    Calculate AI DC business performance based on key variables.
    """
    # Constants (placeholder - later from config)
    HOURS_PER_YEAR = 8760
    TOKEN_PER_KWH = 2000  # 예시: 1kWh당 처리 가능한 토큰 수
    POWER_COST_PER_KWH = 0.12 if use_clean_power == "Conventional" else 0.18
    CAPEX_PER_MW = 1000000  # USD
    OPEX_PER_MW = 150000  # USD/year
    AMORT_YEARS = 5

    # Usage assumptions
    token_usage_per_user = {
        "free": 1000 * 30,    # 월 1천 토큰 x 30일
        "standard": 10000 * 30,
        "premium": 100000 * 30
    }
    user_ratio = {"free": 0.6, "standard": 0.3, "premium": 0.1}
    total_users = 1000000  # 기본 시나리오

    # Efficiency factor
    efficiency = 1.0
    if apply_mirrormind:
        efficiency *= 1.25

    # Power and token capacity
    total_power_kwh = dc_size_mw * 1000 * HOURS_PER_YEAR
    total_token_capacity = total_power_kwh * TOKEN_PER_KWH * efficiency

    # Token demand
    token_demand = sum([
        token_usage_per_user[tier] * user_ratio[tier] * total_users
        for tier in user_ratio
    ])

    # Scale factor (수용가능한 사용자 수)
    scale_ratio = min(1.0, total_token_capacity / token_demand)
    actual_users = int(total_users * scale_ratio)

    # 단가 가정 (후에 역산으로 변경 가능)
    price_per_million_tokens = {
        "free": 0,
        "standard": 0.8,
        "premium": 5.0
    }

    # 매출 계산
    revenue = 0
    user_level_table = []
    for tier in ["free", "standard", "premium"]:
        users = int(actual_users * user_ratio[tier])
        usage = token_usage_per_user[tier] * users
        unit_price = price_per_million_tokens[tier] / 1e6
        tier_revenue = usage * unit_price
        revenue += tier_revenue

        cost = (usage / TOKEN_PER_KWH) * POWER_COST_PER_KWH
        margin = tier_revenue - cost

        user_level_table.append({
            "Tier": tier.title(),
            "Users": users,
            "Monthly_Tokens": token_usage_per_user[tier],
            "Revenue": round(tier_revenue, 2),
            "Cost": round(cost, 2),
            "Margin": round(margin, 2)
        })

    # 비용
    annual_opex = OPEX_PER_MW * dc_size_mw
    annual_capex = CAPEX_PER_MW * dc_size_mw / AMORT_YEARS
    total_cost = annual_opex + annual_capex

    profit = revenue - total_cost

    # 손익분기점 사용자 계산
    avg_rev_per_user = revenue / actual_users if actual_users else 0.01
    break_even_users = int(total_cost / avg_rev_per_user) if avg_rev_per_user else 0

    # 제언
    recommendations = f"* 요금 인상 또는 프리미엄 사용자 비율 확대 고려\n"
    if apply_mirrormind:
        recommendations += "* 미러마인드 적용으로 토큰 효율 개선 효과 반영됨\n"
    else:
        recommendations += "* 미러마인드 미적용: 효율 개선 여지 있음\n"

    return {
        "summary": f"총 매출: ${revenue:,.0f}, 총 비용: ${total_cost:,.0f}, 손익: ${profit:,.0f}",
        "user_level_table": user_level_table,
        "break_even_msg": f"손익분기점 사용자 수: {break_even_users:,}명",
        "recommendations": recommendations
    }
