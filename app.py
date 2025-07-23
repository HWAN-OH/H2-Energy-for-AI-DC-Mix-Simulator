import pandas as pd
import numpy as np

def calculate_integrated_tco(config, user_inputs):
    """
    Calculates the fully integrated 5-year TCO for an AI Data Center.
    This includes DC Construction, IT Hardware, Energy, Maintenance, and Depreciation effects.
    """
    # --- 1. Unpack all inputs ---
    demand_profile = user_inputs['demand_profile']
    apply_mirrormind = user_inputs['apply_mirrormind']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    econ_assumptions = user_inputs['econ_assumptions']
    scenario_params = user_inputs['scenario_params']
    
    # --- 2. Load strategic assumptions from config ---
    sa = config.get('strategic_assumptions', {})
    mm_config = config.get('mirrormind_assumptions', {})
    tech_params = config.get('energy_sources', {})
    
    # --- 3. Determine core parameters based on MirrorMind selection ---
    if apply_mirrormind:
        workload_factor = mm_config.get('workload_efficiency_factor', 1.0)
        energy_mix = mm_config.get('optimized_energy_mix', {})
    else:
        workload_factor = 1.0
        energy_mix = mm_config.get('standard_energy_mix', {})

    # Adjust demand profile based on workload efficiency
    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    
    total_it_load_mw = adj_demand_profile['peak_demand_mw'].iloc[-1] # Final peak demand

    # --- 4. Calculate DC Construction & IT Hardware CAPEX (at t=0) ---
    # Construction CAPEX with penalty for low-cost hardware
    base_construction_cost_per_mw = sa.get('dc_construction_cost_per_mw', 10000000)
    penalty_factor = sa.get('low_cost_hw_penalty_factor', 1.2)
    
    # The construction cost is a blend based on the hardware mix
    effective_construction_cost_per_mw = (base_construction_cost_per_mw * high_perf_hw_ratio) + \
                                         (base_construction_cost_per_mw * penalty_factor * (1 - high_perf_hw_ratio))
    
    dc_construction_capex = effective_construction_cost_per_mw * total_it_load_mw

    # IT Hardware CAPEX
    h_gpu = sa.get('high_perf_gpu', {})
    l_gpu = sa.get('low_cost_gpu', {})
    
    # Total performance units needed for the entire DC at final scale
    # Assuming a hypothetical total performance requirement for a 100MW non-MM DC
    base_total_performance_units = (demand_profile['peak_demand_mw'].iloc[-1] / 100) * 2000 * h_gpu.get('performance_unit', 10)
    
    required_performance_units = base_total_performance_units * workload_factor
    
    perf_from_high = required_performance_units * high_perf_hw_ratio
    perf_from_low = required_performance_units * (1 - high_perf_hw_ratio)
    
    num_high_gpu = perf_from_high / h_gpu.get('performance_unit', 10)
    num_low_gpu = perf_from_low / l_gpu.get('performance_unit', 1)
    
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    # --- 5. Calculate 5-Year Energy TCO ---
    # This part reuses a simplified energy calculation logic
    initial_energy_capex = 0
    peak_demand_kw_yr1 = adj_demand_profile['peak_demand_mw'].iloc[0] * 1000
    for source, mix in energy_mix.items():
        if source != 'grid' and mix > 0:
            capacity_kw = peak_demand_kw_yr1 * (mix / 100)
            initial_energy_capex += capacity_kw * tech_params.get(source, {}).get('capex_per_kw', 0)
    
    total_energy_opex_pv = 0
    for index, row in adj_demand_profile.iterrows():
        year = index + 1
        discount_factor = 1 / ((1 + econ_assumptions['discount_rate']) ** year)
        annual_demand_kwh = row['demand_mwh'] * 1000
        
        # Simplified OPEX calculation for this integrated model
        grid_cost = (annual_demand_kwh * (energy_mix.get('grid', 0) / 100)) * scenario_params.get('grid_price_per_kwh', 0)
        ng_cost = (annual_demand_kwh * (energy_mix.get('NG_SOFC', 0) / 100)) * scenario_params.get('gas_fuel_cost_per_kwh', 0)
        
        total_energy_opex_pv += (grid_cost + ng_cost) * discount_factor
        
    energy_tco_5yr = initial_energy_capex + total_energy_opex_pv

    # --- 6. Calculate 5-Year Maintenance & Depreciation Effects ---
    # Maintenance Cost
    annual_maintenance_cost = dc_construction_capex * sa.get('maintenance_rate_of_construction_capex', 0.02)
    maintenance_cost_5yr_pv = sum([annual_maintenance_cost / ((1 + econ_assumptions['discount_rate']) ** (i+1)) for i in range(5)])

    # Depreciation Tax Shield
    building_depreciation_per_year = dc_construction_capex / sa.get('building_depreciation_years', 40)
    it_hw_depreciation_per_year = it_hardware_capex / sa.get('it_hw_depreciation_years', 5)
    
    tax_shield_5yr_pv = 0
    for i in range(5):
        annual_depreciation = building_depreciation_per_year + it_hw_depreciation_per_year
        tax_shield = annual_depreciation * sa.get('corporate_tax_rate', 0.25)
        tax_shield_5yr_pv += tax_shield / ((1 + econ_assumptions['discount_rate']) ** (i+1))

    # --- 7. Final Integrated TCO Calculation ---
    integrated_tco = (dc_construction_capex + it_hardware_capex + energy_tco_5yr + maintenance_cost_5yr_pv) - tax_shield_5yr_pv

    # --- 8. Prepare Summary Output ---
    summary = {
        "final_integrated_tco_5yr": integrated_tco,
        "investment_per_mw": integrated_tco / total_it_load_mw if total_it_load_mw > 0 else 0,
        "breakdown": {
            "A_DC_Construction_CAPEX": dc_construction_capex,
            "B_IT_Hardware_CAPEX": it_hardware_capex,
            "C_Energy_TCO_5yr": energy_tco_5yr,
            "D_Maintenance_Cost_5yr_PV": maintenance_cost_5yr_pv,
            "E_Tax_Shield_5yr_PV": -tax_shield_5yr_pv,
        }
    }
    return summary
