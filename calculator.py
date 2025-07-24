import yaml
import pandas as pd
from localization import t

def calculate_business_case(dc_size_mw, use_clean_power, apply_mirrormind, paid_tier_fee, premium_tier_multiplier, lang):
    """
    Calculates detailed P&L for the entire business and per user segment.
    """
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # --- 1. Unpack Config & Constants ---
    HOURS_PER_YEAR = 8760
    dc_conf = config["dc_defaults"]
    token_conf = config["token_processing"]
    tiers_conf = config["tiers"]
    assumptions = config["assumptions"]

    # --- 2. Calculate Capacity & Core Costs ---
    TOKEN_PER_KWH = token_conf["token_per_kwh"]
    EFFICIENCY = token_conf["mirrormind_efficiency"] if apply_mirrormind else 1.0
    power_cost_kwh = dc_conf["power_cost_kwh"][use_clean_power]
    annual_capex = (dc_conf["capex_per_mw"] * dc_size_mw) / dc_conf["amortization_years"]
    annual_opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw
    fixed_costs = annual_capex + annual_opex

    total_power_kwh_capacity = dc_size_mw * 1000 * HOURS_PER_YEAR
    total_token_capacity = total_power_kwh_capacity * TOKEN_PER_KWH * EFFICIENCY

    # --- 3. Calculate Demand & Actual User Scale ---
    token_demand_per_user_set = sum(
        tier_conf["monthly_token_usage"] * 12 * tier_conf["ratio"]
        for tier, tier_conf in tiers_conf.items()
    )
    num_user_sets_capacity = total_token_capacity / token_demand_per_user_set if token_demand_per_user_set > 0 else 0
    actual_users_total = int(num_user_sets_capacity * sum(tier['ratio'] for tier in tiers_conf.values()))

    # --- 4. Calculate P&L per Segment ---
    segment_pnl = {}
    total_revenue = 0
    total_variable_cost = 0
    total_token_usage = 0

    pricing = {
        "free": 0,
        "standard": paid_tier_fee,
        "premium": paid_tier_fee * premium_tier_multiplier
    }

    for tier, tier_conf in tiers_conf.items():
        users_in_tier = int(actual_users_total * tier_conf["ratio"])
        token_usage_tier = tier_conf["monthly_token_usage"] * 12 * users_in_tier
        
        revenue_tier = pricing[tier] * 12 * users_in_tier if tier != "free" else 0
        
        # Variable cost is power cost
        power_consumed_kwh_tier = (token_usage_tier / EFFICIENCY) / TOKEN_PER_KWH if TOKEN_PER_KWH > 0 else 0
        cost_tier_variable = power_consumed_kwh_tier * power_cost_kwh
        
        total_revenue += revenue_tier
        total_variable_cost += cost_tier_variable
        total_token_usage += token_usage_tier

        segment_pnl[tier] = {
            "users": users_in_tier,
            "total_revenue": revenue_tier,
            "total_cost": cost_tier_variable, # Will add fixed cost portion later
            "total_profit": revenue_tier - cost_tier_variable,
            "per_user_revenue": pricing[tier] * 12 if tier != "free" else 0,
            "per_user_cost": (cost_tier_variable / users_in_tier) if users_in_tier > 0 else 0,
            "per_user_profit": (pricing[tier] * 12 - (cost_tier_variable / users_in_tier)) if users_in_tier > 0 and tier != "free" else -(cost_tier_variable / users_in_tier) if users_in_tier > 0 else 0
        }

    # --- 5. Final P&L and Break-Even ---
    total_cost = fixed_costs + total_variable_cost
    total_profit = total_revenue - total_cost
    
    # Distribute fixed costs for accurate segment P&L
    for tier in segment_pnl:
        user_ratio = segment_pnl[tier]['users'] / actual_users_total if actual_users_total > 0 else 0
        fixed_cost_share = fixed_costs * user_ratio
        segment_pnl[tier]['total_cost'] += fixed_cost_share
        segment_pnl[tier]['total_profit'] -= fixed_cost_share
        segment_pnl[tier]['per_user_cost'] += (fixed_cost_share / segment_pnl[tier]['users']) if segment_pnl[tier]['users'] > 0 else 0
        segment_pnl[tier]['per_user_profit'] -= (fixed_cost_share / segment_pnl[tier]['users']) if segment_pnl[tier]['users'] > 0 else 0


    # Payback Period
    annual_cash_flow = total_profit + annual_capex # Simplified: Profit + Depreciation
    payback_years = (dc_conf["capex_per_mw"] * dc_size_mw) / annual_cash_flow if annual_cash_flow > 0 else float('inf')


    return {
        "assumptions": {
            "dc_size": dc_size_mw,
            "gpu_mix": "N/A in this version", # Placeholder
            "supported_users": actual_users_total,
            "serviced_tokens_t": total_token_usage / 1_000_000_000_000, # Trillion
            "consumed_kwh_gwh": (total_variable_cost / power_cost_kwh) / 1_000_000 if power_cost_kwh > 0 else 0 # GWh
        },
        "pnl_annual": {
            "revenue": total_revenue,
            "cost": total_cost,
            "profit": total_profit
        },
        "pnl_segments": segment_pnl,
        "payback_years": payback_years
    }
