import numpy as np

def calculate_business_case(config, user_inputs):
    # --- 1. Unpack all inputs & config ---
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    electricity_price = user_inputs['electricity_price']
    
    biz_conf = config.get('business_assumptions', {})
    infra_conf = config.get('infrastructure_assumptions', {})
    hw_conf = config.get('hardware_specs', {})
    arch_conf = config.get('advanced_architecture', {})
    rd_conf = config.get('research_and_development', {})
    user_conf = config.get('user_model', {})
    op_conf = config.get('operating_scenarios', {})

    # --- 2. Calculate Infrastructure & Capacity ---
    DC_SIZE_MW = infra_conf.get('dc_size_mw', 100)
    
    dc_construction_capex = infra_conf.get('dc_construction_cost_per_mw', 0) * DC_SIZE_MW
    it_hardware_budget = infra_conf.get('it_hardware_budget_per_mw', 0) * DC_SIZE_MW
    
    budget_for_high_perf = it_hardware_budget * high_perf_hw_ratio
    budget_for_low_cost = it_hardware_budget * (1 - high_perf_hw_ratio)

    h_gpu = hw_conf.get('high_perf_gpu', {})
    l_gpu = hw_conf.get('low_cost_gpu', {})
    
    num_high_gpu = budget_for_high_perf / h_gpu.get('cost_per_unit', 1)
    num_low_gpu = budget_for_low_cost / l_gpu.get('cost_per_unit', 1)
    
    total_token_capacity_per_hour = (num_high_gpu * h_gpu.get('m_tokens_per_hour_per_unit', 0)) + \
                                    (num_low_gpu * l_gpu.get('m_tokens_per_hour_per_unit', 0))
    
    annual_token_capacity_millions = total_token_capacity_per_hour * 24 * 365

    # --- 3. Calculate Annual Costs (P&L) ---
    # Operating Costs
    annual_maintenance_cost = dc_construction_capex * op_conf.get('maintenance_rate_of_construction_capex', 0)
    total_it_power_watts = it_hardware_budget * op_conf.get('watts_per_dollar_of_it_hardware', 0)
    total_dc_power_watts = total_it_power_watts * op_conf.get('pue', 1.5)
    total_annual_kwh = (total_dc_power_watts * 24 * 365) / 1000
    annual_electricity_cost = total_annual_kwh * electricity_price
    
    # Depreciation & Amortization
    annual_dc_depreciation = dc_construction_capex / infra_conf.get('building_depreciation_years', 40)
    annual_it_depreciation = it_hardware_budget / infra_conf.get('it_hw_depreciation_years', 5)
    
    model_dev_cost = rd_conf.get('total_model_development_cost', 0)
    model_amort_years = rd_conf.get('model_amortization_years', 1)
    global_dcs = rd_conf.get('global_datacenter_count_for_cost_allocation', 1)
    annual_rd_amortization = (model_dev_cost / global_dcs) / model_amort_years if model_amort_years > 0 and global_dcs > 0 else 0

    total_annual_cost = annual_maintenance_cost + annual_electricity_cost + annual_dc_depreciation + annual_it_depreciation + annual_rd_amortization
    
    # --- 4. Calculate Revenue & Profitability ---
    user_set = user_conf.get('user_set_composition', {})
    tokens_per_user_set_monthly = sum([tier['ratio'] * tier['monthly_token_usage_millions'] for tier in user_set.values()])
    
    if apply_advanced_arch:
        tokens_per_user_set_monthly *= arch_conf.get('workload_efficiency_factor', 1.0)

    tokens_per_user_set_annually = tokens_per_user_set_monthly * 12
    num_user_sets_supported = annual_token_capacity_millions / tokens_per_user_set_annually if tokens_per_user_set_annually > 0 else 0
    
    pricing = user_conf.get('pricing', {})
    revenue_per_user_set_monthly = (user_set['paid']['ratio'] * pricing.get('paid_tier_fee', 0)) + \
                                   (user_set['premium']['ratio'] * pricing.get('premium_tier_fee', 0))
    
    annual_revenue = num_user_sets_supported * revenue_per_user_set_monthly * 12
    operating_profit = annual_revenue - total_annual_cost

    # --- 5. Per-User P&L ---
    fully_loaded_cost_per_m_tokens = total_annual_cost / annual_token_capacity_millions if annual_token_capacity_millions > 0 else 0
    unit_pnl = {}
    for tier_name, tier_data in user_set.items():
        monthly_tokens = tier_data['monthly_token_usage_millions']
        if apply_advanced_arch:
            monthly_tokens *= arch_conf.get('workload_efficiency_factor', 1.0)
        
        user_cost = monthly_tokens * fully_loaded_cost_per_m_tokens
        user_revenue = pricing.get(f"{tier_name}_tier_fee", 0) if tier_name != 'free' else 0
        unit_pnl[tier_name] = {
            'usage': monthly_tokens,
            'cost': user_cost,
            'revenue': user_revenue,
            'profit': user_revenue - user_cost
        }

    # --- 6. Break-Even Analysis ---
    initial_investment = dc_construction_capex + it_hardware_budget
    total_annual_depreciation = annual_dc_depreciation + annual_it_depreciation + annual_rd_amortization
    ebit = operating_profit
    tax = max(0, ebit * biz_conf.get('corporate_tax_rate', 0.25))
    op_cash_flow = ebit - tax + total_annual_depreciation
    
    payback_period = float('inf')
    if op_cash_flow > 0:
        # Simplified payback for P&L model
        payback_period = initial_investment / op_cash_flow

    fixed_costs = total_annual_depreciation + annual_rd_amortization + annual_maintenance_cost
    variable_cost_per_m_tokens = (annual_electricity_cost / annual_token_capacity_millions) if annual_token_capacity_millions > 0 else 0
    revenue_per_m_tokens = (annual_revenue / annual_token_capacity_millions) if annual_token_capacity_millions > 0 else 0
    contribution_margin_per_token = revenue_per_m_tokens - variable_cost_per_m_tokens

    breakeven_tokens_millions = fixed_costs / contribution_margin_per_token if contribution_margin_per_token > 0 else float('inf')
    breakeven_total_users = (breakeven_tokens_millions / tokens_per_user_set_annually) * sum(tier['ratio'] for tier in user_set.values()) if tokens_per_user_set_annually > 0 and breakeven_tokens_millions != float('inf') else float('inf')

    return {
        "pnl": { "revenue": annual_revenue, "cost": total_annual_cost, "profit": operating_profit },
        "unit_pnl": unit_pnl,
        "breakeven": { "payback_period": payback_period, "required_users": breakeven_total_users }
    }
