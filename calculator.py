import pandas as pd
import numpy as np

def calculate_integrated_tco(config, user_inputs):
    """
    Calculates the 5-year TCO for cost comparison and a more realistic 10-year
    business viability analysis including reinvestment and salvage value.
    """
    # --- 1. Unpack all inputs & assumptions ---
    demand_profile = user_inputs['demand_profile']
    apply_advanced_arch = user_inputs['apply_advanced_arch']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    econ_assumptions = user_inputs['econ_assumptions']
    target_irr = econ_assumptions['target_irr']
    
    sa = config.get('strategic_assumptions', {})
    arch_config = config.get('advanced_architecture_assumptions', {})
    power_mix_config = config.get('power_mix_options', {})
    ra = config.get('revenue_assumptions', {})
    tech_params = config.get('energy_sources', {})
    
    # --- 2. Determine core parameters based on user choices ---
    workload_factor = arch_config.get('workload_efficiency_factor', 1.0) if apply_advanced_arch else 1.0
    energy_mix = power_mix_config.get('carbon_free_mix', {}) if user_inputs['use_carbon_free_mix'] else power_mix_config.get('standard_mix', {})

    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    total_it_load_mw = adj_demand_profile['peak_demand_mw'].iloc[-1]

    # --- 3. Calculate Initial Investments (CAPEX at Year 0) ---
    base_construction_cost_per_mw = sa.get('dc_construction_cost_per_mw', 10000000)
    penalty_factor = sa.get('low_cost_hw_penalty_factor', 1.2)
    effective_construction_cost_per_mw = (base_construction_cost_per_mw * high_perf_hw_ratio) + \
                                         (base_construction_cost_per_mw * penalty_factor * (1 - high_perf_hw_ratio))
    dc_construction_capex = effective_construction_cost_per_mw * total_it_load_mw
    
    h_gpu = sa.get('high_perf_gpu', {})
    l_gpu = sa.get('low_cost_gpu', {})
    base_total_performance_units = (demand_profile['peak_demand_mw'].iloc[-1] / 100) * 2000 * h_gpu.get('performance_unit', 10)
    required_performance_units = base_total_performance_units * workload_factor
    perf_from_high = required_performance_units * high_perf_hw_ratio
    perf_from_low = required_performance_units * (1 - high_perf_hw_ratio)
    num_high_gpu = perf_from_high / h_gpu.get('performance_unit', 10) if h_gpu.get('performance_unit', 10) > 0 else 0
    num_low_gpu = perf_from_low / l_gpu.get('performance_unit', 1) if l_gpu.get('performance_unit', 1) > 0 else 0
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    initial_energy_capex = 0
    peak_demand_kw_yr1 = adj_demand_profile['peak_demand_mw'].iloc[0] * 1000
    for source, mix in energy_mix.items():
        if source != 'grid' and mix > 0:
            initial_energy_capex += (peak_demand_kw_yr1 * (mix / 100)) * tech_params.get(source, {}).get('capex_per_kw', 0)

    # --- 4. Calculate 5-Year TCO (for simple cost comparison) ---
    total_energy_opex_pv_5yr = 0
    for i in range(5):
        annual_demand_kwh = adj_demand_profile['demand_mwh'].iloc[i] * 1000
        grid_cost = (annual_demand_kwh * (energy_mix.get('grid', 0) / 100)) * user_inputs['scenario_params'].get('grid_price_per_kwh', 0)
        ng_cost = (annual_demand_kwh * (energy_mix.get('NG_SOFC', 0) / 100)) * user_inputs['scenario_params'].get('gas_fuel_cost_per_kwh', 0)
        total_energy_opex_pv_5yr += (grid_cost + ng_cost) / ((1 + econ_assumptions['discount_rate']) ** (i+1))
    
    maintenance_cost_5yr_pv = sum([(dc_construction_capex * sa.get('maintenance_rate_of_construction_capex', 0.02)) / ((1 + econ_assumptions['discount_rate']) ** (i+1)) for i in range(5)])
    tax_shield_5yr_pv = sum([((dc_construction_capex / sa.get('building_depreciation_years', 40)) + (it_hardware_capex / sa.get('it_hw_depreciation_years', 5))) * sa.get('corporate_tax_rate', 0.25) / ((1 + econ_assumptions['discount_rate']) ** (i+1)) for i in range(5)])
    
    tco_5yr = (dc_construction_capex + it_hardware_capex + initial_energy_capex + total_energy_opex_pv_5yr + maintenance_cost_5yr_pv) - tax_shield_5yr_pv

    # --- 5. Realistic Business Viability Analysis (10-Year Horizon) ---
    viability_years = sa.get('viability_analysis_years', 10)
    cash_outflows_pv = dc_construction_capex + it_hardware_capex + initial_energy_capex

    it_reinvestment_capex = it_hardware_capex 
    cash_outflows_pv += it_reinvestment_capex / ((1 + target_irr) ** 5)

    for year in range(1, viability_years + 1):
        demand_row = adj_demand_profile.iloc[min(year - 1, 4)]
        
        annual_energy_opex = (demand_row['demand_mwh'] * 1000) * \
                             ((energy_mix.get('grid', 0)/100 * user_inputs['scenario_params'].get('grid_price_per_kwh',0)) + \
                              (energy_mix.get('NG_SOFC',0)/100 * user_inputs['scenario_params'].get('gas_fuel_cost_per_kwh',0)))
        annual_maintenance = dc_construction_capex * sa.get('maintenance_rate_of_construction_capex', 0.02)
        
        cash_outflows_pv += (annual_energy_opex + annual_maintenance) / ((1 + target_irr) ** year)

        depreciation_y1_5 = (dc_construction_capex / sa.get('building_depreciation_years', 40)) + (it_hardware_capex / sa.get('it_hw_depreciation_years', 5))
        depreciation_y6_10 = (dc_construction_capex / sa.get('building_depreciation_years', 40)) + (it_reinvestment_capex / sa.get('it_hw_depreciation_years', 5))
        
        annual_depreciation = depreciation_y1_5 if year <= 5 else depreciation_y6_10
        tax_shield = annual_depreciation * sa.get('corporate_tax_rate', 0.25)
        cash_outflows_pv -= tax_shield / ((1 + target_irr) ** year)

    building_salvage_value = dc_construction_capex * (sa.get('building_depreciation_years', 40) - viability_years) / sa.get('building_depreciation_years', 40)
    cash_outflows_pv -= building_salvage_value / ((1 + target_irr) ** viability_years)

    if target_irr > 0:
        pvaf = (1 - (1 + target_irr)**-viability_years) / target_irr
    else:
        pvaf = viability_years
    required_annual_revenue = cash_outflows_pv / pvaf if pvaf > 0 else 0

    physical_dc_mw = demand_profile['peak_demand_mw'].iloc[-1] 
    total_serviceable_users = (physical_dc_mw * ra.get('active_users_per_mw', 1)) / workload_factor
    avg_annual_demand_mwh = adj_demand_profile['demand_mwh'].mean()
    price_per_million_tokens = (required_annual_revenue / (avg_annual_demand_mwh * ra.get('tokens_processed_per_mwh', 1) / 1_000_000)) if avg_annual_demand_mwh > 0 else 0
    monthly_fee_per_user = (required_annual_revenue / total_serviceable_users / 12) if total_serviceable_users > 0 else 0

    # --- 6. Prepare Summary Output ---
    summary = {
        "final_integrated_tco_5yr": tco_5yr,
        "investment_per_mw": tco_5yr / total_it_load_mw if total_it_load_mw > 0 else 0,
        "viability": {
            "required_annual_revenue": required_annual_revenue,
            "price_per_million_tokens": price_per_million_tokens,
            "monthly_fee_per_user": monthly_fee_per_user,
            "total_serviceable_users": total_serviceable_users
        }
    }
    return summary
