# calculator.py (패치버전)

import yaml

def calculate_business_case(dc_size_mw, power_type, target_irr, apply_mirrormind, lang_code):
    # config 로딩
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    # [1] 기본 파라미터
    dc_conf = config["dc_defaults"]
    token_conf = config["token_processing"]
    tiers_conf = config["tiers"]
    users_total = config["assumptions"]["users_total"]
    HOURS_PER_YEAR = 8760

    # [2] 토큰/효율/전력 파라미터
    EFFICIENCY = token_conf["mirrormind_efficiency"] if apply_mirrormind else 1.0
    TOKENS_PER_KWH = token_conf.get("tokens_per_kwh", 50000)
    power_cost_kwh = dc_conf["power_cost_kwh"][power_type]

    # [3] 전체 토큰처리량(캐파) & 연간 전력량
    total_power_kwh = dc_size_mw * 1000 * HOURS_PER_YEAR
    total_token_capacity = total_power_kwh * TOKENS_PER_KWH * EFFICIENCY

    # [4] 연간 고객군별 토큰 수요 계산
    tiers = ["free", "standard", "premium"]
    group_stats = []
    token_demand_total = 0
    for t in tiers:
        ratio = tiers_conf[t]["ratio"]
        month_token = tiers_conf[t]["monthly_token_usage"]
        group_tokens = ratio * users_total * month_token * 12  # 1년간
        token_demand_total += group_tokens
        group_stats.append({
            "tier": t,
            "ratio": ratio,
            "users": int(users_total * ratio),
            "annual_tokens": group_tokens
        })

    # [5] 실사용자 scaling (처리 한계 이상이면 자동 축소)
    scale = min(1.0, total_token_capacity / token_demand_total) if token_demand_total > 0 else 0
    for g in group_stats:
        g["users"] = int(g["users"] * scale)
        g["annual_tokens"] = g["annual_tokens"] * scale

    # [6] 매출, 비용, 이익 (고객군별/전체)
    revenue_total = 0
    power_cost_total = 0
    per_group_table = []
    for g in group_stats:
        tier = g["tier"]
        price_per_mtoken = tiers_conf[tier]["price_per_million_token"]
        annual_revenue = (g["annual_tokens"] / 1_000_000) * price_per_mtoken
        annual_power_kwh = g["annual_tokens"] / TOKENS_PER_KWH
        group_power_cost = annual_power_kwh * power_cost_kwh
        margin = annual_revenue - group_power_cost

        per_group_table.append({
            "Tier": tier.title(),
            "Users": g["users"],
            "Annual_Tokens": int(g["annual_tokens"]),
            "Revenue($)": round(annual_revenue, 2),
            "PowerCost($)": round(group_power_cost, 2),
            "Margin($)": round(margin, 2),
            "UnitCost($/Mtoken)": round(group_power_cost / (g["annual_tokens"] / 1_000_000), 4) if g["annual_tokens"] > 0 else 0,
            "UnitPrice($/Mtoken)": price_per_mtoken
        })
        revenue_total += annual_revenue
        power_cost_total += group_power_cost

    # [7] 연간 CAPEX/OPEX/감가상각 등
    opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw
    capex = dc_conf["capex_per_mw"] * dc_size_mw / dc_conf["amortization_years"]

    # [8] 요약 손익
    total_cost = power_cost_total + opex + capex
    profit = revenue_total - total_cost
    summary = f"총 매출: ${revenue_total:,.0f}, 총 비용: ${total_cost:,.0f}, 손익: ${profit:,.0f}"

    # [9] 손익분기점 (연간 기준)
    unit_rev = revenue_total / (sum(g["users"] for g in group_stats) or 1)
    be_users = int(total_cost / (unit_rev or 1))

    # [10] 전략 제언
    recommendations = ""
    if profit < 0:
        recommendations += "비용구조 개선, 단가 조정, 프리미엄 비중 확대 필요"
    else:
        recommendations += "현 구조에서 수익성 확보, 추가 효율화 여지 검토"

    return {
        "summary": summary,
        "per_group_table": per_group_table,
        "break_even_msg": f"손익분기점 연간 사용자: {be_users:,}명",
        "recommendations": recommendations
    }
