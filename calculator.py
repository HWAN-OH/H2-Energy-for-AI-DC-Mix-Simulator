import yaml

def calculate_business_case(
    dc_size_mw,
    use_clean_power,
    apply_mirrormind,
    high_perf_gpu_ratio,
    utilization_rate,
    market_price_per_m_tokens,
    lang
):
    # [1] config 로딩
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    dc_conf = config["dc_defaults"]
    token_conf = config["token_processing"]
    tiers_conf = config["tiers"]
    users_total = config["assumptions"]["users_total"]
    HOURS_PER_YEAR = 8760

    # [2] 토큰/효율/전력 파라미터
    EFFICIENCY = token_conf["mirrormind_efficiency"] if apply_mirrormind else 1.0
    TOKENS_PER_KWH = token_conf.get("tokens_per_kwh", 50000)
    power_cost_kwh = dc_conf["power_cost_kwh"][use_clean_power]

    # [3] GPU mix (high_perf_gpu_ratio) 적용
    high_perf_ratio = high_perf_gpu_ratio
    standard_ratio = 1 - high_perf_ratio
    n_gpu = int(dc_size_mw * 30)  # 임의: MW 1당 30대
    n_high = int(n_gpu * high_perf_ratio)
    n_std = n_gpu - n_high

    # [4] 전체 연간 토큰 처리량 계산 (고성능/표준 구분)
    tokens_per_high = token_conf.get("tokens_per_gpu_high_perf", 1_200_000_000)
    tokens_per_std = token_conf.get("tokens_per_gpu_standard", 500_000_000)
    total_token_capacity = (
        n_high * tokens_per_high +
        n_std * tokens_per_std
    ) * utilization_rate * EFFICIENCY

    # [5] 고객군별 연간 토큰 수요 계산
    tiers = ["free", "standard", "premium"]
    group_stats = []
    token_demand_total = 0
    for t in tiers:
        ratio = tiers_conf[t]["ratio"]
        month_token = tiers_conf[t]["monthly_token_usage"]
        group_tokens = ratio * users_total * month_token * 12
        token_demand_total += group_tokens
        group_stats.append({
            "tier": t,
            "ratio": ratio,
            "users": int(users_total * ratio),
            "annual_tokens": group_tokens
        })

    # [6] 실사용자 scaling (처리 한계 초과시 축소)
    scale = min(1.0, total_token_capacity / token_demand_total) if token_demand_total > 0 else 0
    for g in group_stats:
        g["users"] = int(g["users"] * scale)
        g["annual_tokens"] = g["annual_tokens"] * scale

    # [7] 매출, 전력비, 이익 (고객군별/전체)
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

    # [8] 연간 OPEX/CAPEX/감가상각 등 (DC config)
    opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw
    capex = dc_conf["capex_per_mw"] * dc_size_mw / dc_conf["amortization_years"]
    # (필요시 SG&A, 감가상각 등도 config에서 추가 가능)

    # [9] 연간 손익
    total_cost = power_cost_total + opex + capex
    profit = revenue_total - total_cost
    summary = f"총 매출: ${revenue_total:,.0f}, 총 비용: ${total_cost:,.0f}, 손익: ${profit:,.0f}"

    # [10] 손익분기점
    unit_rev = revenue_total / (sum(g["users"] for g in group_stats) or 1)
    be_users = int(total_cost / (unit_rev or 1))

    # [11] 전략 제언
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
