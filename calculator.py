import pandas as pd
import numpy as np
import numpy_financial as npf

def calculate_business_case(config, user_inputs):
    """
    Calculates TCO, required revenue for IRR, detailed unit economics, and projected payback period.
    """
    # --- 1. Unpack all inputs & assumptions ---
    demand_profile = user_inputs['demand_profile']
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    target_irr = user_inputs['target_irr'] / 100.0
    paid_tier_fee = user_inputs['paid_tier_fee']
    premium_tier_fee = user_inputs['premium_tier_fee']
    electricity_price = user_inputs['electricity_price']

    biz_config = config.get('business_assumptions', {})
    user_config = config.get('user_assumptions', {})
    infra_config = config.get('infrastructure_assumptions', {})
    arch_config = config.get('advanced_architecture_assumptions', {})
    service_config = config.get('service_unit_assumptions', {})

    analysis_years = biz_config.get('analysis_years', 10)

    # --- 2. Adjust demand based on architecture choice ---
    workload_factor = arch_config.get('workload_efficiency_factor', 1.0) if apply_advanced_arch else 1.0
    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    
    original_final_peak_demand_mw = demand_profile['peak_demand_mw'].iloc[-1]
    adj_final_peak_demand_mw = adj_demand_profile['peak_demand_mw'].iloc[-1]
    
    # --- BUG FIX: Determine the actual physical DC size based on the architecture choice ---
    # 아키텍처 적용 시, 실제 건설하는 데이터센터의 물리적 크기(MW)를 결정합니다.
    effective_dc_size_mw = adj_final_peak_demand_mw

    # --- 3. Calculate Initial Investments (CAPEX at Year 0) ---
    base_construction_cost_per_mw = infra_config.get('dc_construction_cost_per_mw', 10000000)
    penalty_factor = infra_config.get('low_cost_hw_penalty_factor', 1.2)
    effective_construction_cost_per_mw = (base_construction_cost_per_mw * high_perf_hw_ratio) + \
                                         (base_construction_cost_per_mw * penalty_factor * (1 - high_perf_hw_ratio))
    
    # --- BUG FIX: DC 건설비용을 실제 물리적 크기 기준으로 계산합니다.
    dc_construction_capex = effective_construction_cost_per_mw * effective_dc_size_mw

    h_gpu = infra_config.get('high_perf_gpu', {})
    l_gpu = infra_config.get('low_cost_gpu', {})
    
    # --- BUG FIX: IT 하드웨어 구매 비용도 실제 물리적 크기 기준으로 계산합니다.
    base_total_performance_units = (effective_dc_size_mw / 100) * 2000 * h_gpu.get('performance_unit', 10)
    required_performance_units = base_total_performance_units 
    
    num_high_gpu = (required_performance_units * high_perf_hw_ratio) / h_gpu.get('performance_unit', 1)
    num_low_gpu = (required_performance_units * (1 - high_perf_hw_ratio)) / l_gpu.get('performance_unit', 1)
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    initial_investment = dc_construction_capex + it_hardware_capex
    it_reinvestment_capex = it_hardware_capex

    # --- 4. Analysis A: Required Revenue for Target IRR (Cost Basis) ---
    cost_cash_outflows = [0] * (analysis_years + 1)
    cost_cash_outflows[0] = -initial_investment
    cost_cash_outflows[5] -= it_reinvestment_capex

    for year in range(1, analysis_years + 1):
        demand_row = adj_demand_profile.iloc[min(year - 1, len(adj_demand_profile) - 1)]
        annual_electricity_cost = (demand_row['demand_mwh'] * 1000) * electricity_price
        annual_maintenance = dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02)
        
        depreciation_y1_5 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
        depreciation_y6_10 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_reinvestment_capex / infra_config.get('it_hw_depreciation_years', 5))
        annual_depreciation = depreciation_y1_5 if year <= 5 else depreciation_y6_10
        
        taxable_income_op = -(annual_electricity_cost + annual_maintenance + annual_depreciation)
        tax_shield = -taxable_income_op * infra_config.get('corporate_tax_rate', 0.25)
        cost_cash_outflows[year] -= (annual_electricity_cost + annual_maintenance - tax_shield)
    
    building_salvage_value = dc_construction_capex * (infra_config.get('building_depreciation_years', 40) - analysis_years) / infra_config.get('building_depreciation_years', 40)
    cost_cash_outflows[analysis_years] += building_salvage_value

    required_npv = -npf.npv(target_irr, cost_cash_outflows)
    pvaf = (1 - (1 + target_irr)**-analysis_years) / target_irr if target_irr > 0 else analysis_years
    required_annual_revenue = required_npv / pvaf if pvaf > 0 else 0

    avg_annual_demand_mwh = adj_demand_profile['demand_mwh'].mean()
    total_tokens_processed_annually_millions = avg_annual_demand_mwh * service_config.get('tokens_processed_per_mwh', 1) / 1_000_000
    price_per_million_tokens = required_annual_revenue / total_tokens_processed_annually_millions if total_tokens_processed_annually_millions > 0 else 0

    # --- 5. Analysis B: Unit Economics ---
    total_users = user_config.get('total_users_for_100mw', 0) * (original_final_peak_demand_mw / 100)
    tier_fees = {'free': 0, 'paid': paid_tier_fee, 'premium': premium_tier_fee}
    unit_economics = {}
    
    for tier_name, tier_data in user_config.get('tiers', {}).items():
        unit_economics[tier_name] = {
            'token_usage': tier_data.get('monthly_token_usage_millions', 0),
            'cost': tier_data.get('monthly_token_usage_millions', 0) * price_per_million_tokens,
            'revenue': tier_fees.get(tier_name, 0),
            'profit': tier_fees.get(tier_name, 0) - (tier_data.get('monthly_token_usage_millions', 0) * price_per_million_tokens),
            'num_users': total_users * tier_data.get('ratio', 0)
        }

    # --- 6. Analysis C: Payback Period Calculation ---
    assumed_annual_revenue = (unit_economics['paid']['num_users'] * unit_economics['paid']['revenue'] +
                              unit_economics['premium']['num_users'] * unit_economics['premium']['revenue']) * 12

    cumulative_cash_flow = -initial_investment
    payback_period = float('inf')
    last_year_net_cash_flow = 0

    for year in range(1, analysis_years + 1):
        demand_row = adj_demand_profile.iloc[min(year - 1, len(adj_demand_profile) - 1)]
        annual_opex = (demand_row['demand_mwh'] * 1000) * electricity_price + \
                      (dc_construction_capex * infra_config.get('maintenance_rate_of_construction_capex', 0.02))
        
        depreciation_y1_5 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_hardware_capex / infra_config.get('it_hw_depreciation_years', 5))
        depreciation_y6_10 = (dc_construction_capex / infra_config.get('building_depreciation_years', 40)) + (it_reinvestment_capex / infra_config.get('it_hw_depreciation_years', 5))
        annual_depreciation = depreciation_y1_5 if year <= 5 else depreciation_y6_10
        
        taxable_income = assumed_annual_revenue - annual_opex - annual_depreciation
        tax = max(0, taxable_income * infra_config.get('corporate_tax_rate', 0.25))
        
        net_cash_flow_after_tax = assumed_annual_revenue - annual_opex - tax
        
        if year == 5:
            net_cash_flow_after_tax -= it_reinvestment_capex
        
        if cumulative_cash_flow + net_cash_flow_after_tax >= 0 and payback_period == float('inf'):
            payback_period = (year - 1) + (-cumulative_cash_flow / net_cash_flow_after_tax)
        
        cumulative_cash_flow += net_cash_flow_after_tax
        if year == analysis_years:
            last_year_net_cash_flow = net_cash_flow_after_tax

    if payback_period == float('inf') and last_year_net_cash_flow > 0:
        remaining_balance = -cumulative_cash_flow
        additional_years = remaining_balance / last_year_net_cash_flow
        payback_period = analysis_years + additional_years

    # --- 7. Prepare Summary Output ---
    summary = {
        "required_annual_revenue": required_annual_revenue,
        "price_per_million_tokens": price_per_million_tokens,
        "unit_economics": unit_economics,
        "payback_period": payback_period
    }
    return summary
