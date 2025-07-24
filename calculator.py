import numpy as np
import numpy_financial as npf

def calculate_business_case(config, user_inputs):
    # --- 1. Unpack all inputs & config ---
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    target_irr = user_inputs['target_irr'] / 100.0
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    electricity_price = user_inputs['electricity_price']
    
    # Unpack config sections
    biz_conf = config.get('business_assumptions', {})
    infra_conf = config.get('infrastructure_assumptions', {})
    hw_conf = config.get('hardware_specs', {})
    arch_conf = config.get('advanced_architecture', {})
    user_conf = config.get('user_model', {})

    # --- 2. Calculate Infrastructure & Capacity ---
    # For simplicity, we assume a 100MW DC project size
    DC_SIZE_MW = 100
    
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

    # --- 3. Calculate Costs (Annual P&L Basis) ---
    # Operating Costs
    total_it_power_watts = it_hardware_budget * infra_conf.get('watts_per_dollar_of_it_hardware', 0)
    total_dc_power_watts = total_it_power_watts * infra_conf.get('pue', 1.5)
    total_annual_kwh = (total_dc_power_watts * 24 * 365) / 1000
    annual_electricity_cost = total_annual_kwh * electricity_price
    annual_maintenance_cost = dc_construction_capex * infra_conf.get('maintenance_rate_of_construction_capex', 0)
    total_annual_operating_cost = annual_electricity_cost + annual_maintenance_cost

    # Depreciation
    annual_dc_depreciation = dc_construction_capex / infra_conf.get('building_depreciation_years', 40)
    annual_it_depreciation = it_hardware_budget / infra_conf.get('it_hw_depreciation_years', 5)
    total_annual_depreciation = annual_dc_depreciation + annual_it_depreciation

    # Fully Loaded Cost
    total_annual_cost = total_annual_operating_cost + total_annual_depreciation
    fully_loaded_cost_per_m_tokens = total_annual_cost / annual_token_capacity_millions if annual_token_capacity_millions > 0 else 0

    # --- 4. Calculate Revenue & Profitability ---
    user_set = user_conf.get('user_set_composition', {})
    tokens_per_user_set_monthly = sum([
        tier['ratio'] * tier['monthly_token_usage_millions'] for tier in user_set.values()
    ])
    
    # Apply advanced architecture to reduce demand
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
    # Payback Period
    initial_investment = dc_construction_capex + it_hardware_budget
    it_reinvestment = it_hardware_budget
    cash_flow_years = [0] * biz_conf.get('analysis_years', 10)
    ebit = operating_profit
    tax = max(0, ebit * biz_conf.get('corporate_tax_rate', 0.25))
    net_op_profit = ebit - tax
    op_cash_flow = net_op_profit + total_annual_depreciation

    cumulative_cash_flow = -initial_investment
    payback_period = float('inf')
    for i in range(len(cash_flow_years)):
        year_cash_flow = op_cash_flow
        if (i + 1) == 5: # Reinvestment year
            year_cash_flow -= it_reinvestment
        
        if cumulative_cash_flow + year_cash_flow >= 0 and payback_period == float('inf'):
            payback_period = i + (-cumulative_cash_flow / year_cash_flow)
        cumulative_cash_flow += year_cash_flow

    # Break-even users
    fixed_costs = total_annual_depreciation
    contribution_per_user_set = revenue_per_user_set_monthly * 12 - (tokens_per_user_set_annually * (total_annual_operating_cost / annual_token_capacity_millions if annual_token_capacity_millions > 0 else 0))
    
    if contribution_per_user_set > 0:
        breakeven_user_sets = fixed_costs / contribution_per_user_set
        breakeven_total_users = breakeven_user_sets * sum(tier['ratio'] for tier in user_set.values())
    else:
        breakeven_total_users = float('inf')

    return {
        "pnl": {
            "revenue": annual_revenue,
            "cost": total_annual_cost,
            "profit": operating_profit
        },
        "unit_pnl": unit_pnl,
        "breakeven": {
            "payback_period": payback_period,
            "required_users": breakeven_total_users
        }
    }
