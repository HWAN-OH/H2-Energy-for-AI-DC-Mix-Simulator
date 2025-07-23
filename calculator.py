import pandas as pd
import numpy as np

def calculate_business_case(config, user_inputs):
    """
    Calculates both required revenue for a target IRR and the payback period
    based on assumed user fees.
    """
    # --- 1. Unpack all inputs & assumptions ---
    demand_profile = user_inputs['demand_profile']
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    target_irr = user_inputs['target_irr'] / 100.0
    assumed_low_tier_fee = user_inputs['assumed_low_tier_fee']
    electricity_price = user_inputs['electricity_price']
    
    biz_config = config.get('business_assumptions', {})
    user_config = config.get('user_assumptions', {})
    infra_config = config.get('infrastructure_assumptions', {})
    arch_config = config.get('advanced_architecture_assumptions', {})
    service_config = config.get('service_unit_assumptions', {})
    
    analysis_years = biz_config.get('analysis_years', 10)

    # --- 2. Determine core parameters based on user choices ---
    workload_factor = arch_config.get('workload_efficiency_factor', 1.0) if apply_advanced_arch else 1.0
    
    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    
    # --- 3. Calculate Initial Investments (CAPEX at Year 0) ---
    base_construction_cost_per_mw = infra_config.get('dc_construction_cost_per_mw', 10000000)
    penalty_factor = infra_config.get('low_cost_hw_penalty_factor', 1.2)
    effective_construction_cost_per_mw = (base_construction_cost_per_mw * high_perf_hw_ratio) + \
                                         (base_construction_cost_per_mw * penalty_factor * (1 - high_perf_hw_ratio))
    dc_construction_capex = effective_construction_cost_per_mw * demand_profile['peak_demand_mw'].iloc[-1]
    
    h_gpu = infra_config.get('high_perf_gpu', {})
    l_gpu = infra_config.get('low_cost_gpu', {})
    base_total_performance_units = (demand_profile['peak_demand_mw'].iloc[-1] / 100) * 2000 * h_gpu.get('performance_unit', 10)
    required_performance_units = base_total_performance_units * workload_factor
    num_high_gpu = (required_performance_units * high_perf_hw_ratio) / h_gpu.get('performance_unit', 1)
    num_low_gpu = (required_performance_units * (1 - high_perf_hw_ratio)) / l_gpu.get('performance_unit', 1)
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    initial_investment = dc_construction_capex + it_hardware_capex

    # --- 4. Analysis A: Required Revenue for Target IRR ---
    cash_outflows_pv = initial_investment
    it_reinvestment_capex = it_hardware_capex
    cash_outflows_pv += it_reinvestment_capex / ((1 + target_irr) ** 5)

    for year in range(1, analysis_years + 1):
        demand_row = adj_demand_profile.iloc[min(year - 1, 4)]
        annual_electricity_cost = (demand_row['demand_mwh'] * 1000) * electricity_price
        annual_maintenance = dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02)
        cash_outflows_pv += (annual_electricity_cost + annual_maintenance) / ((1 + target_irr) ** year)
        
        depreciation_y1_5 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
        depreciation_y6_10 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_reinvestment_capex / infra_config.get('it_hw_depreciation_years', 5))
        annual_depreciation = depreciation_y1_5 if year <= 5 else depreciation_y6_10
        tax_shield = annual_depreciation * infra_config.get('corporate_tax_rate', 0.25)
        cash_outflows_pv -= tax_shield / ((1 + target_irr) ** year)

    building_salvage_value = dc_construction_capex * (infra_config.get('building_depreciation_years', 40) - analysis_years) / infra_config.get('building_depreciation_years', 40)
    cash_outflows_pv -= building_salvage_value / ((1 + target_irr) ** analysis_years)

    pvaf = (1 - (1 + target_irr)**-analysis_years) / target_irr if target_irr > 0 else analysis_years
    required_annual_revenue = cash_outflows_pv / pvaf if pvaf > 0 else 0
    
    avg_annual_demand_mwh = adj_demand_profile['demand_mwh'].mean()
    price_per_million_tokens = (required_annual_revenue / (avg_annual_demand_mwh * service_config.get('tokens_processed_per_mwh', 1) / 1_000_000)) if avg_annual_demand_mwh > 0 else 0

    # --- 5. Analysis B: Payback Period ---
    assumed_high_tier_fee = assumed_low_tier_fee * user_config.get('high_to_low_pricing_ratio', 10)
    total_users = user_config.get('total_users', 0)
    low_tier_users = total_users * user_config.get('low_tier_user_pct', 0)
    high_tier_users = total_users * user_config.get('high_tier_user_pct', 0)
    
    assumed_annual_revenue = ((low_tier_users * assumed_low_tier_fee) + (high_tier_users * assumed_high_tier_fee)) * 12
    
    cumulative_cash_flow = -initial_investment
    payback_period = -1
    
    for year in range(1, analysis_years + 1):
        demand_row = adj_demand_profile.iloc[min(year - 1, 4)]
        annual_opex = (demand_row['demand_mwh'] * 1000) * electricity_price + \
                      (dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02))
        
        net_cash_flow = assumed_annual_revenue - annual_opex
        
        # Add back depreciation for cash flow calculation, then subtract tax
        depreciation_y1_5 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
        depreciation_y6_10 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_reinvestment_capex / infra_config.get('it_hw_depreciation_years', 5))
        annual_depreciation = depreciation_y1_5 if year <= 5 else depreciation_y6_10
        
        taxable_income = assumed_annual_revenue - annual_opex - annual_depreciation
        tax = taxable_income * infra_config.get('corporate_tax_rate', 0.25)
        
        # After-tax cash flow
        net_cash_flow_after_tax = assumed_annual_revenue - annual_opex - tax
        
        if year == 5:
            net_cash_flow_after_tax -= it_reinvestment_capex
        
        if cumulative_cash_flow + net_cash_flow_after_tax > 0 and payback_period == -1:
            payback_period = (year - 1) + (-cumulative_cash_flow / net_cash_flow_after_tax)
        
        cumulative_cash_flow += net_cash_flow_after_tax
        
    if payback_period == -1:
        payback_period = float('inf') # Indicates payback is beyond the analysis period

    # --- 6. Prepare Summary Output ---
    summary = {
        "required_annual_revenue": required_annual_revenue,
        "price_per_million_tokens": price_per_million_tokens,
        "payback_period": payback_period
    }
    return summary
