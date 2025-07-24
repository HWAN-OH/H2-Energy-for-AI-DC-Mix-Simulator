# calculator_v12.py (with config loading)

import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

def calculate_business_case(dc_size_mw, use_clean_power, target_irr, apply_mirrormind, lang):
    """
    Calculate AI DC business performance based on config values and user inputs.
    """
    HOURS_PER_YEAR = 8760

    dc_conf = config["dc_defaults"]
    token_conf = config["token_processing"]
    tiers_conf = config["tiers"]
    assumptions = config["assumptions"]

    TOKEN_PER_KWH = token_conf["token_per_kwh"]
    EFFICIENCY = token_conf["mirrormind_efficiency"] if apply_mirrormind else 1.0

    power_cost = dc_conf["power_cost_kwh"][use_clean_power]
    capex = dc_conf["capex_per_mw"] * dc_size_mw / dc_conf["amortization_years"]
    opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw

    total_power_kwh = dc_size_mw * 1000 * HOURS_PER_YEAR
    total_token_capacity = total_power_kwh * TOKEN_PER_KWH * EFFICIENCY

    token_demand = 0
    for tier in tiers_conf:
        tier_conf = tiers_conf[tier]
        token_demand += tier_conf["monthly_token_usage"] * 12 * tier_conf["ratio"] * assumptions["users_total"]

    scale_ratio = min(1.0, total_token_capacity / token_demand)
    actual_users = int(assumptions["users_total"] * scale_ratio)

    revenue = 0
    user_level_table = []

    for tier in ["free", "standard", "premium"]:
        tier_conf = tiers_conf[tier]
        users = int(actual_users * tier_conf["ratio"])
        usage = tier_conf["monthly_token_usage"] * 12 * users
        unit_price = tier_conf["price_per_million_token"] / 1e6
        tier_revenue = usage * unit_price
        revenue += tier_revenue

        cost = (usage / TOKEN_PER_KWH) * power_cost
        margin = tier_revenue - cost

        user_level_table.append({
            "Tier": tier.title(),
            "Users": users,
            "Monthly_Tokens": tier_conf["monthly_token_usage"],
            "Revenue": round(tier_revenue, 2),
            "Cost": round(cost, 2),
            "Margin": round(margin, 2)
        })

    total_cost = capex + opex
    profit = revenue - total_cost

    avg_rev_per_user = revenue / actual_users if actual_users else 0.01
    break_even_users = int(total_cost / avg_rev_per_user) if avg_rev_per_user else 0

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
