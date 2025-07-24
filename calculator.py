import yaml
import pandas as pd

def calculate_business_case(dc_size_mw, use_clean_power, apply_mirrormind, high_perf_gpu_ratio, utilization_rate, market_price_per_m_tokens, lang):
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # --- 1. Unpack Config ---
    inv_conf = config["investment"]
    hw_conf = config["hardware"]
    op_conf = config["operating_expenses"]
    rd_conf = config["research_and_development"]
    model_conf = config["model_and_market"]
    tiers_conf = model_conf["tiers"]

    # --- 2. Calculate Hardware Mix & Max Capacity ---
    it_budget = inv_conf["it_budget_per_mw"] * dc_size_mw
    high_perf_budget = it_budget * (high_perf_gpu_ratio / 100.0)
    standard_budget = it_budget * (1 - high_perf_gpu_ratio / 100.0)

    h_gpu = hw_conf["high_perf_gpu"]
    s_gpu = hw_conf["standard_gpu"]
    num_high_perf_gpus = high_perf_budget / h_gpu["cost"] if h_gpu["cost"] > 0 else 0
    num_standard_gpus = standard_budget / s_gpu["cost"] if s_gpu["cost"] > 0 else 0
    
    max_token_capacity_m = ((num_high_perf_gpus * h_gpu["m_tokens_per_hour"]) + \
                            (num_standard_gpus * s_gpu["m_tokens_per_hour"])) * 8760
    
    # --- 3. Apply Real-World Constraints ---
    util_rate = utilization_rate / 100.0
    EFFICIENCY = model_conf["intelligent_arch_efficiency"] if apply_mirrormind else 1.0
    effective_tokens_serviced_m = max_token_capacity_m * util_rate * EFFICIENCY

    # --- 4. Build Complete P&L ---
    pnl = {}
    pnl['revenue'] = effective_tokens_serviced_m * market_price_per_m_tokens

    power_consumed_kwh = (effective_tokens_serviced_m / EFFICIENCY) * 1000000 / 2000 
    power_cost_kwh = 0.18 if use_clean_power == "Renewable" else 0.12
    annual_power_cost = power_consumed_kwh * power_cost_kwh
    annual_maintenance_cost = op_conf["maintenance_and_cooling_per_mw"] * dc_size_mw
    annual_personnel_cost = op_conf["personnel_and_other_per_mw"] * dc_size_mw
    pnl['cost_of_revenue'] = annual_power_cost + annual_maintenance_cost + annual_personnel_cost
    pnl['gross_profit'] = pnl['revenue'] - pnl['cost_of_revenue']

    dc_capex = inv_conf["dc_capex_per_mw"] * dc_size_mw
    pnl['dc_depreciation'] = dc_capex / inv_conf["amortization_years"]["datacenter"]
    pnl['it_depreciation'] = it_budget / inv_conf["amortization_years"]["it_hardware"]
    pnl['rd_amortization'] = (rd_conf["total_model_development_cost"] / rd_conf["global_datacenter_count_for_cost_allocation"]) / inv_conf["amortization_years"]["research_and_development"]
    pnl['sg_and_a'] = pnl['revenue'] * (op_conf["sgna_as_percent_of_revenue"] / 100.0)
    pnl['operating_expenses'] = pnl['dc_depreciation'] + pnl['it_depreciation'] + pnl['rd_amortization'] + pnl['sg_and_a']
    pnl['operating_profit'] = pnl['gross_profit'] - pnl['operating_expenses']
    
    total_annual_cost = pnl['cost_of_revenue'] + pnl['operating_expenses']

    # --- 5. Per-User Segment P&L (NEWLY ADDED) ---
    pnl_segments = {}
    total_token_usage_by_users = 0
    # First, find the total token usage based on the user mix
    for tier, tier_conf in tiers_conf.items():
        total_token_usage_by_users += tier_conf['monthly_token_usage_m'] * 12 * tier_conf['ratio']

    # Scale factor to match serviced tokens to user demand profile
    scaling_factor = effective_tokens_serviced_m / total_token_usage_by_users if total_token_usage_by_users > 0 else 0

    for tier, tier_conf in tiers_conf.items():
        # This tier's share of total token consumption
        token_share_ratio = (tier_conf['monthly_token_usage_m'] * tier_conf['ratio']) / (total_token_usage_by_users / 12) if total_token_usage_by_users > 0 else 0
        
        # Calculate revenue and cost based on this share
        revenue_segment = pnl['revenue'] * token_share_ratio
        cost_segment = total_annual_cost * token_share_ratio
        profit_segment = revenue_segment - cost_segment
        
        pnl_segments[tier] = {
            "total_revenue": revenue_segment,
            "total_cost": cost_segment,
            "total_profit": profit_segment
        }

    # --- 6. Payback Period ---
    total_investment = dc_capex + it_budget
    annual_cash_flow = pnl['operating_profit'] + pnl['dc_depreciation'] + pnl['it_depreciation'] + pnl['rd_amortization']
    payback_years = total_investment / annual_cash_flow if annual_cash_flow > 0 else float('inf')

    return {
        "assumptions": {
            "dc_size": dc_size_mw,
            "utilization_rate": utilization_rate,
            "gpu_mix_string": f"{int(num_high_perf_gpus):,} H / {int(num_standard_gpus):,} S",
            "serviced_tokens_t": effective_tokens_serviced_m / 1_000_000,
        },
        "pnl_annual": pnl,
        "pnl_segments": pnl_segments,
        "payback_years": payback_years
    }
