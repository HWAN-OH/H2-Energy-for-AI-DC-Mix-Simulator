import pandas as pd
import numpy as np
import numpy_financial as npf

def calculate_business_case(config, user_inputs):
    """
    Calculates a full P&L for the entire business and for a single user.
    """
    # --- 1. Unpack all inputs & assumptions ---
    demand_profile = user_inputs['demand_profile']
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    paid_tier_fee = user_inputs['paid_tier_fee']
    premium_tier_fee = user_inputs['premium_tier_fee']
    electricity_price = user_inputs['electricity_price']

    user_config = config.get('user_assumptions', {})
    infra_config = config.get('infrastructure_assumptions', {})
    arch_config = config.get('advanced_architecture_assumptions', {})
    rd_config = config.get('research_and_development_assumptions', {})
    analysis_years = config.get('business_assumptions', {}).get('analysis_years', 10)

    # --- 2. Determine Effective DC Size and Costs ---
    workload_factor = arch_config.get('workload_efficiency_factor', 1.0) if apply_advanced_arch else 1.0
    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    
    original_final_peak_demand_mw = demand_profile['peak_demand_mw'].iloc[-1]
    effective_dc_size_mw = adj_demand_profile['peak_demand_mw'].iloc[-1]

    # --- 3. Calculate CAPEX and Annual P&L (using Year 5 as representative) ---
    dc_construction_capex = infra_config.get('dc_construction_cost_per_mw', 10) * effective_dc_size_mw
    
    h_gpu = infra_config.get('high_perf_gpu', {})
    l_gpu = infra_config.get('low_cost_gpu', {})
    base_total_performance_units = (effective_dc_size_mw / 100) * 2000 * h_gpu.get('performance_unit', 10)
    num_high_gpu = (base_total_performance_units * high_perf_hw_ratio) / h_gpu.get('performance_unit', 1)
    num_low_gpu = (base_total_performance_units * (1 - high_perf_hw_ratio)) / l_gpu.get('performance_unit', 1)
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    initial_investment = dc_construction_capex + it_hardware_capex
    it_reinvestment_capex = it_hardware_capex

    # P&L Calculation
    pnl = {}
    year_5_demand = adj_demand_profile.iloc[4]
    
    total_users = user_config.get('total_users_for_100mw', 0) * (original_final_peak_demand_mw / 100)
    paid_users = total_users * user_config.get('tiers', {}).get('paid', {}).get('ratio', 0)
    premium_users = total_users * user_config.get('tiers', {}).get('premium', {}).get('ratio', 0)
    pnl['revenue'] = (paid_users * paid_tier_fee + premium_users * premium_tier_fee) * 12

    pnl['cost_of_revenue'] = year_5_demand['demand_mwh'] * 1000 * electricity_price + \
                             dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02)
    
    pnl['gross_profit'] = pnl['revenue'] - pnl['cost_of_revenue']

    pnl['depreciation_amortization_asset'] = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + \
                                             (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
    
    model_dev_cost = rd_config.get('total_model_development_cost', 0)
    model_amort_years = rd_config.get('model_amortization_years', 3)
    global_dcs = rd_config.get('global_datacenter_count', 1)
    pnl['depreciation_amortization_rd'] = (model_dev_cost / global_dcs) / model_amort_years if model_amort_years > 0 and global_dcs > 0 else 0
    
    pnl['operating_expenses'] = pnl['depreciation_amortization_asset'] + pnl['depreciation_amortization_rd']
    pnl['operating_profit'] = pnl['gross_profit'] - pnl['operating_expenses']

    # --- 4. Per-User P&L ---
    total_annual_tokens_millions = sum([
        (total_users * tier_data['ratio']) * tier_data['monthly_token_usage_millions'] * 12
        for tier_name, tier_data in user_config.get('tiers', {}).items()
    ])
    
    total_annual_cost = pnl['cost_of_revenue'] + pnl['operating_expenses']
    fully_loaded_cost_per_million_tokens = total_annual_cost / total_annual_tokens_millions if total_annual_tokens_millions > 0 else 0

    unit_pnl = {}
    tier_fees = {'free': 0, 'paid': paid_tier_fee, 'premium': premium_tier_fee}
    for tier_name, tier_data in user_config.get('tiers', {}).items():
        monthly_tokens = tier_data.get('monthly_token_usage_millions', 0)
        
        user_revenue = tier_fees.get(tier_name, 0)
        user_cost = monthly_tokens * fully_loaded_cost_per_million_tokens
        user_op_profit = user_revenue - user_cost
        
        unit_pnl[tier_name] = {
            'revenue': user_revenue,
            'cost': user_cost,
            'profit': user_op_profit,
        }

    # --- 5. Payback Period Calculation ---
    payback_period = float('inf') # Placeholder, as P&L is now the focus

    return {
        "pnl": pnl,
        "unit_pnl": unit_pnl,
        "payback_period": payback_period
    }
