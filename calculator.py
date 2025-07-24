import pandas as pd
import numpy as np

def calculate_business_case(config, user_inputs):
    """
    Calculates P&L based on a unit-cost structure linked to hardware performance.
    """
    # --- 1. Unpack all inputs & assumptions ---
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    
    biz_config = config.get('business_assumptions', {})
    perf_config = config.get('performance_assumptions', {})
    user_config = config.get('user_assumptions', {})
    op_config = config.get('operating_assumptions', {})

    # --- 2. Hardware Investment & Performance Analysis ---
    it_budget = biz_config.get('it_hardware_budget', 0)
    budget_for_high_perf = it_budget * high_perf_hw_ratio
    budget_for_low_cost = it_budget * (1 - high_perf_hw_ratio)

    h_gpu = perf_config.get('high_perf_gpu', {})
    l_gpu = perf_config.get('low_cost_gpu', {})

    num_high_gpu = budget_for_high_perf / h_gpu.get('cost_per_unit', 1)
    num_low_gpu = budget_for_low_cost / l_gpu.get('cost_per_unit', 1)

    total_performance_score = (num_high_gpu * h_gpu.get('performance_score_per_unit', 0)) + \
                              (num_low_gpu * l_gpu.get('performance_score_per_unit', 0))

    # --- 3. Capacity Calculation ---
    m_tokens_per_hour = total_performance_score * perf_config.get('m_tokens_per_hour_per_performance_score', 0)
    total_annual_token_capacity_millions = m_tokens_per_hour * 24 * 365

    # --- 4. Cost Structure & Unit Cost Analysis ---
    # Annual Costs
    dc_construction_capex = biz_config.get('dc_construction_budget', 0)
    it_hardware_capex = it_budget

    annual_dc_depreciation = dc_construction_capex / op_config.get('building_depreciation_years', 40)
    annual_it_depreciation = it_hardware_capex / op_config.get('it_hw_depreciation_years', 5)
    
    total_it_power_watts = it_hardware_capex * op_config.get('watts_per_dollar_of_it_hardware', 0)
    total_dc_power_watts = total_it_power_watts * op_config.get('pue', 1.5)
    total_annual_kwh = (total_dc_power_watts * 24 * 365) / 1000
    annual_electricity_cost = total_annual_kwh * op_config.get('electricity_price_per_kwh', 0)

    annual_maintenance_cost = dc_construction_capex * op_config.get('maintenance_rate_of_construction_capex', 0)

    total_annual_cost = annual_dc_depreciation + annual_it_depreciation + annual_electricity_cost + annual_maintenance_cost
    
    # Unit Cost
    cost_per_million_tokens = total_annual_cost / total_annual_token_capacity_millions if total_annual_token_capacity_millions > 0 else 0

    # --- 5. Profitability Analysis (P&L) ---
    user_set = user_config.get('user_set_composition', {})
    tokens_per_user_set_monthly = sum([
        tier['ratio'] * tier['monthly_token_usage_millions']
        for tier in user_set.values()
    ])
    tokens_per_user_set_annually = tokens_per_user_set_monthly * 12

    num_user_sets_supported = total_annual_token_capacity_millions / tokens_per_user_set_annually if tokens_per_user_set_annually > 0 else 0
    
    total_users_supported = num_user_sets_supported * sum(tier['ratio'] for tier in user_set.values())
    paid_users = num_user_sets_supported * user_set.get('paid', {}).get('ratio', 0)
    premium_users = num_user_sets_supported * user_set.get('premium', {}).get('ratio', 0)

    pricing = user_config.get('pricing', {})
    annual_revenue = (paid_users * pricing.get('paid_tier_fee', 0) + premium_users * pricing.get('premium_tier_fee', 0)) * 12

    operating_profit = annual_revenue - total_annual_cost

    # --- 6. Prepare Summary ---
    summary = {
        'hw_investment': it_budget,
        'total_performance_score': total_performance_score,
        'annual_token_capacity': total_annual_token_capacity_millions,
        'total_annual_cost': total_annual_cost,
        'cost_per_million_tokens': cost_per_million_tokens,
        'total_users_supported': total_users_supported,
        'annual_revenue': annual_revenue,
        'operating_profit': operating_profit,
    }
    return summary
