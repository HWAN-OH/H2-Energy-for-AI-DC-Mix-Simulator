import yaml
import pandas as pd

def calculate_business_case(dc_size_mw, use_clean_power, target_irr, apply_mirrormind, lang):
    """
    Calculates AI DC business performance and returns structured data for the UI.
    """
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    HOURS_PER_YEAR = 8760

    dc_conf = config["dc_defaults"]
    token_conf = config["token_processing"]
    tiers_conf = config["tiers"]
    assumptions = config["assumptions"]

    TOKEN_PER_KWH = token_conf["token_per_kwh"]
    EFFICIENCY = token_conf["mirrormind_efficiency"] if apply_mirrormind else 1.0

    power_cost = dc_conf["power_cost_kwh"][use_clean_power]
    
    # Correctly apply amortization over the entire period
    annual_capex = (dc_conf["capex_per_mw"] * dc_size_mw) / dc_conf["amortization_years"]
    annual_opex = dc_conf["opex_per_mw_per_year"] * dc_size_mw

    total_power_kwh = dc_size_mw * 1000 * HOURS_PER_YEAR
    total_token_capacity = total_power_kwh * TOKEN_PER_KWH * EFFICIENCY

    token_demand = 0
    # Calculate total token demand based on the assumption of total users
    for tier in tiers_conf:
        tier_conf = tiers_conf[tier]
        token_demand += tier_conf["monthly_token_usage"] * 12 * tier_conf["ratio"] * assumptions["users_total"]

    # Scale down the number of users if capacity is less than demand
    scale_ratio = min(1.0, total_token_capacity / token_demand if token_demand > 0 else 1.0)
    actual_users_total = int(assumptions["users_total"] * scale_ratio)

    total_revenue = 0
    total_usage = 0
    
    # Calculate revenue based on actual supported users
    for tier in ["free", "standard", "premium"]:
        tier_conf = tiers_conf[tier]
        users_in_tier = int(actual_users_total * tier_conf["ratio"])
        usage_in_tier = tier_conf["monthly_token_usage"] * 12 * users_in_tier
        unit_price = tier_conf["price_per_million_token"] / 1_000_000
        total_revenue += usage_in_tier * unit_price
        total_usage += usage_in_tier
        
    # Cost is based on actual usage, not max capacity
    total_power_consumed_kwh = (total_usage / EFFICIENCY) / TOKEN_PER_KWH if TOKEN_PER_KWH > 0 else 0
    total_power_cost = total_power_consumed_kwh * power_cost
    
    total_cost = annual_capex + annual_opex + total_power_cost
    total_profit = total_revenue - total_cost

    # Create Annual P&L DataFrame
    pnl_data = {
        "Item": [t("pnl_revenue", lang), t("pnl_cost", lang), t("pnl_profit", lang)],
        "Amount ($)": [total_revenue, total_cost, total_profit]
    }
    pnl_df = pd.DataFrame(pnl_data)

    # Create Per-User Annual P&L DataFrame
    per_user_pnl_df = None
    if actual_users_total > 0:
        per_user_pnl_data = {
            "Item": [t("pnl_revenue", lang), t("pnl_cost", lang), t("pnl_profit", lang)],
            "Amount ($)": [
                total_revenue / actual_users_total,
                total_cost / actual_users_total,
                total_profit / actual_users_total
            ]
        }
        per_user_pnl_df = pd.DataFrame(per_user_pnl_data)

    # Break-even analysis
    avg_rev_per_user = total_revenue / actual_users_total if actual_users_total > 0 else 0
    variable_cost_per_user = total_power_cost / actual_users_total if actual_users_total > 0 else 0
    contribution_margin_per_user = avg_rev_per_user - variable_cost_per_user
    fixed_costs = annual_capex + annual_opex
    
    break_even_users = int(fixed_costs / contribution_margin_per_user) if contribution_margin_per_user > 0 else float('inf')

    # Recommendations
    recommendations = []
    if total_profit < 0:
        recommendations.append(f"- {t('reco_price_increase', lang)}")
        if not apply_mirrormind:
            recommendations.append(f"- {t('reco_efficiency_improvement', lang)}")
    else:
        recommendations.append(f"- {t('reco_profit_positive', lang)}")


    return {
        "pnl_df": pnl_df,
        "per_user_pnl_df": per_user_pnl_df,
        "break_even_users": break_even_users,
        "recommendations": "\n".join(recommendations),
        "dc_size": dc_size_mw
    }

