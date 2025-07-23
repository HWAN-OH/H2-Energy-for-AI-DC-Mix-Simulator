import pandas as pd
import numpy as np
import numpy_financial as npf

def calculate_business_case(config, user_inputs):
    """
    Calculates a full P&L, unit economics based on operating costs, and payback period.
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
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    
    original_final_peak_demand_mw = demand_profile['peak_demand_mw'].iloc[-1]
    effective_dc_size_mw = adj_demand_profile['peak_demand_mw'].iloc[-1]

    # --- 3. Calculate CAPEX and Depreciation ---
    base_construction_cost_per_mw = infra_config.get('dc_construction_cost_per_mw', 10)
    dc_construction_capex = base_construction_cost_per_mw * effective_dc_size_mw

    h_gpu = infra_config.get('high_perf_gpu', {})
    l_gpu = infra_config.get('low_cost_gpu', {})
    base_total_performance_units = (effective_dc_size_mw / 100) * 2000 * h_gpu.get('performance_unit', 10)
    num_high_gpu = (base_total_performance_units * high_perf_hw_ratio) / h_gpu.get('performance_unit', 1)
    num_low_gpu = (base_total_performance_units * (1 - high_perf_hw_ratio)) / l_gpu.get('performance_unit', 1)
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    initial_investment = dc_construction_capex + it_hardware_capex
    it_reinvestment_capex = it_hardware_capex

    # --- 4. Build Annual P&L Statement (using Year 5 as representative) ---
    pnl = {}
    year_5_demand = adj_demand_profile.iloc[4]

    # Revenue
    total_users = user_config.get('total_users_for_100mw', 0) * (original_final_peak_demand_mw / 100)
    paid_users = total_users * user_config.get('tiers', {}).get('paid', {}).get('ratio', 0)
    premium_users = total_users * user_config.get('tiers', {}).get('premium', {}).get('ratio', 0)
    pnl['revenue'] = (paid_users * paid_tier_fee + premium_users * premium_tier_fee) * 12

    # Operating Costs (COGS-like)
    pnl['op_cost_electricity'] = year_5_demand['demand_mwh'] * 1000 * electricity_price
    pnl['op_cost_maintenance'] = dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02)
    
    # Depreciation & Amortization
    pnl['depreciation_amortization_asset'] = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + \
                                             (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
    
    model_dev_cost = rd_config.get('total_model_development_cost', 0)
    model_amort_years = rd_config.get('model_amortization_years', 3)
    global_dcs = rd_config.get('global_datacenter_count', 1)
    pnl['depreciation_amortization_rd'] = (model_dev_cost / global_dcs) / model_amort_years if model_amort_years > 0 and global_dcs > 0 else 0

    # Operating Profit (EBIT)
    pnl['operating_profit'] = pnl['revenue'] - pnl['op_cost_electricity'] - pnl['op_cost_maintenance'] - \
                              pnl['depreciation_amortization_asset'] - pnl['depreciation_amortization_rd']

    # --- 5. Unit Economics based on Operating Costs ---
    unit_economics = {}
    total_op_cost_per_mwh = (pnl['op_cost_electricity'] + pnl['op_cost_maintenance']) / year_5_demand['demand_mwh'] if year_5_demand['demand_mwh'] > 0 else 0
    tokens_per_mwh = config.get('service_unit_assumptions',{}).get('tokens_processed_per_mwh', 1)
    op_cost_per_million_tokens = (total_op_cost_per_mwh / tokens_per_mwh) * 1_000_000 if tokens_per_mwh > 0 else 0

    tier_fees = {'free': 0, 'paid': paid_tier_fee, 'premium': premium_tier_fee}
    for tier_name, tier_data in user_config.get('tiers', {}).items():
        unit_economics[tier_name] = {
            'cost': tier_data.get('monthly_token_usage_millions', 0) * op_cost_per_million_tokens,
            'revenue': tier_fees.get(tier_name, 0),
            'profit': tier_fees.get(tier_name, 0) - (tier_data.get('monthly_token_usage_millions', 0) * op_cost_per_million_tokens)
        }

    # --- 6. Payback Period Calculation based on Cash Flow ---
    cumulative_cash_flow = -initial_investment
    payback_period = float('inf')
    last_year_net_cash_flow = 0
    
    for year in range(1, analysis_years + 1):
        # EBIAT (Earnings Before Interest, After Tax) as proxy for operating cash flow
        # For simplicity, we use the Year 5 P&L for all years, but adjust for reinvestment
        ebit = pnl['operating_profit']
        tax = max(0, ebit * infra_config.get('corporate_tax_rate', 0.25))
        # Add back non-cash charges
        op_cash_flow = ebit - tax + pnl['depreciation_amortization_asset'] + pnl['depreciation_amortization_rd']
        
        if year == 5:
            op_cash_flow -= it_reinvestment_capex
        
        if cumulative_cash_flow + op_cash_flow >= 0 and payback_period == float('inf'):
            payback_period = (year - 1) + (-cumulative_cash_flow / op_cash_flow) if op_cash_flow > 0 else float('inf')
        
        cumulative_cash_flow += op_cash_flow
        if year == analysis_years:
            last_year_net_cash_flow = op_cash_flow
            
    if payback_period == float('inf') and last_year_net_cash_flow > 0:
        remaining_balance = -cumulative_cash_flow
        additional_years = remaining_balance / last_year_net_cash_flow
        payback_period = analysis_years + additional_years

    return {
        "pnl": pnl,
        "unit_economics": unit_economics,
        "payback_period": payback_period
    }
