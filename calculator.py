import yaml
import pandas as pd

def calculate_business_case(dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio, paid_tier_fee, premium_tier_multiplier, lang):
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # --- 1. Unpack Config & Constants ---
    HOURS_PER_YEAR = 8760
    hw_conf = config["hardware"]
    dc_conf = config["datacenter"]
    biz_conf = config["model_and_business"]
    tiers_conf = biz_conf["tiers"]
    rd_conf = biz_conf["research_and_development"]

    # --- 2. Calculate Hardware Mix, Capacity & Power Consumption ---
    it_budget = hw_conf["it_budget_per_mw"] * dc_size_mw
    high_perf_budget = it_budget * (high_perf_gpu_ratio / 100.0)
    standard_budget = it_budget * (1 - high_perf_gpu_ratio / 100.0)

    h_gpu = hw_conf["high_perf_gpu"]
    s_gpu = hw_conf["standard_gpu"]

    num_high_perf_gpus = high_perf_budget / h_gpu["cost"] if h_gpu["cost"] > 0 else 0
    num_standard_gpus = standard_budget / s_gpu["cost"] if s_gpu["cost"] > 0 else 0
    
    total_token_capacity_m = ((num_high_perf_gpus * h_gpu["m_tokens_per_hour"]) + \
                              (num_standard_gpus * s_gpu["m_tokens_per_hour"])) * HOURS_PER_YEAR
    
    total_it_power_kw = (num_high_perf_gpus * 0.7 + num_standard_gpus * 0.4)
    total_dc_power_kw = total_it_power_kw * dc_conf["total_watts_per_it_watt"]
    total_power_kwh_consumed = total_dc_power_kw * HOURS_PER_YEAR

    # --- 3. Calculate Demand & Revenue ---
    EFFICIENCY = biz_conf["intelligent_arch_efficiency"] if apply_mirrormind else 1.0
    effective_token_capacity_m = total_token_capacity_m * EFFICIENCY

    token_demand_per_user_set = sum(
        tier_conf["monthly_token_usage_m"] * 12 * tier_conf["ratio"]
        for tier, tier_conf in tiers_conf.items()
    )
    
    num_user_sets_supported = effective_token_capacity_m / token_demand_per_user_set if token_demand_per_user_set > 0 else 0
    actual_users_total = int(num_user_sets_supported * sum(tier['ratio'] for tier in tiers_conf.values()))

    pricing = {"free": 0, "standard": paid_tier_fee, "premium": paid_tier_fee * premium_tier_multiplier}
    
    total_revenue = 0
    segment_pnl = {}
    for tier, tier_conf in tiers_conf.items():
        users_in_tier = int(actual_users_total * tier_conf["ratio"])
        revenue_tier = pricing[tier] * 12 * users_in_tier if tier != "free" else 0
        total_revenue += revenue_tier
        segment_pnl[tier] = {"users": users_in_tier, "total_revenue": revenue_tier}

    # --- 4. Build Complete P&L ---
    pnl = {}
    pnl['revenue'] = total_revenue
    
    power_cost_kwh = dc_conf["power_cost_kwh"][use_clean_power]
    annual_power_cost = total_power_kwh_consumed * power_cost_kwh
    annual_opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw
    pnl['cost_of_revenue'] = annual_power_cost + annual_opex
    pnl['gross_profit'] = pnl['revenue'] - pnl['cost_of_revenue']

    annual_capex_dc = (dc_conf["capex_per_mw"] * dc_size_mw)
    annual_capex_it = it_budget
    pnl['d_and_a'] = (annual_capex_dc / dc_conf["amortization_years"]) + (annual_capex_it / dc_conf["amortization_years"])
    
    pnl['rd_amortization'] = (rd_conf["total_model_development_cost"] / rd_conf["global_datacenter_count_for_cost_allocation"]) / rd_conf["model_amortization_years"]
    
    pnl['sg_and_a'] = pnl['revenue'] * (biz_conf["sgna_as_percent_of_revenue"] / 100.0)
    
    pnl['operating_expenses'] = pnl['d_and_a'] + pnl['rd_amortization'] + pnl['sg_and_a']
    pnl['operating_profit'] = pnl['gross_profit'] - pnl['operating_expenses']

    # --- 5. Per-User P&L Calculation ---
    total_cost = pnl['cost_of_revenue'] + pnl['operating_expenses']
    for tier in segment_pnl:
        data = segment_pnl[tier]
        users_in_tier = data['users']
        user_ratio = (users_in_tier / actual_users_total) if actual_users_total > 0 else 0
        cost_share = total_cost * user_ratio
        
        data['total_cost'] = cost_share
        data['total_profit'] = data['total_revenue'] - cost_share

    # --- 6. Payback Period ---
    annual_cash_flow = pnl['operating_profit'] + pnl['d_and_a'] + pnl['rd_amortization']
    total_investment = annual_capex_dc + annual_capex_it
    payback_years = total_investment / annual_cash_flow if annual_cash_flow > 0 else float('inf')

    return {
        "assumptions": {
            "dc_size": dc_size_mw,
            "gpu_mix_string": f"{int(num_high_perf_gpus):,} H / {int(num_standard_gpus):,} S",
            "supported_users": actual_users_total,
            "serviced_tokens_t": total_token_capacity_m / 1_000_000,
            "consumed_power_gwh": total_power_kwh_consumed / 1_000_000
        },
        "pnl_annual": pnl,
        "pnl_segments": segment_pnl,
        "payback_years": payback_years
    }
