import pandas as pd
import numpy as np

def calculate_integrated_tco(config, user_inputs):
    """
    Calculates the fully integrated 5-year TCO and required revenue for target IRR.
    """
    # --- 1. Unpack all inputs ---
    demand_profile = user_inputs['demand_profile']
    apply_mirrormind = user_inputs['apply_mirrormind']
    high_perf_hw_ratio = user_inputs['high_perf_hw_ratio'] / 100.0
    econ_assumptions = user_inputs['econ_assumptions']
    scenario_params = user_inputs['scenario_params']
    target_irr = econ_assumptions['target_irr'] # 목표 IRR 추가
    
    # ... (기존 2, 3, 4, 5, 6 단계는 동일) ...
    
    # --- 2. Load strategic assumptions from config ---
    sa = config.get('strategic_assumptions', {})
    mm_config = config.get('mirrormind_assumptions', {})
    tech_params = config.get('energy_sources', {})
    ra = config.get('revenue_assumptions', {}) # 매출 가정 로드

    # --- 3. Determine core parameters based on MirrorMind selection ---
    if apply_mirrormind:
        workload_factor = mm_config.get('workload_efficiency_factor', 1.0)
        energy_mix = mm_config.get('optimized_energy_mix', {})
    else:
        workload_factor = 1.0
        energy_mix = mm_config.get('standard_energy_mix', {})

    adj_demand_profile = demand_profile.copy()
    adj_demand_profile['demand_mwh'] *= workload_factor
    adj_demand_profile['peak_demand_mw'] *= workload_factor
    
    total_it_load_mw = adj_demand_profile['peak_demand_mw'].iloc[-1]

    # --- 4. Calculate DC Construction & IT Hardware CAPEX ---
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
    num_high_gpu = perf_from_high / h_gpu.get('performance_unit', 10)
    num_low_gpu = perf_from_low / l_gpu.get('performance_unit', 1)
    it_hardware_capex = (num_high_gpu * h_gpu.get('cost_per_unit', 0)) + \
                        (num_low_gpu * l_gpu.get('cost_per_unit', 0))

    # --- 5. Calculate 5-Year Energy TCO ---
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
        grid_cost = (annual_demand_kwh * (energy_mix.get('grid', 0) / 100)) * scenario_params.get('grid_price_per_kwh', 0)
        ng_cost = (annual_demand_kwh * (energy_mix.get('NG_SOFC', 0) / 100)) * scenario_params.get('gas_fuel_cost_per_kwh', 0)
        total_energy_opex_pv += (grid_cost + ng_cost) * discount_factor
        
    energy_tco_5yr = initial_energy_capex + total_energy_opex_pv

    # --- 6. Calculate 5-Year Maintenance & Depreciation Effects ---
    annual_maintenance_cost = dc_construction_capex * sa.get('maintenance_rate_of_construction_capex', 0.02)
    maintenance_cost_5yr_pv = sum([annual_maintenance_cost / ((1 + econ_assumptions['discount_rate']) ** (i+1)) for i in range(5)])

    building_depreciation_per_year = dc_construction_capex / sa.get('building_depreciation_years', 40)
    it_hw_depreciation_per_year = it_hardware_capex / sa.get('it_hw_depreciation_years', 5)
    tax_shield_5yr_pv = 0
    for i in range(5):
        annual_depreciation = building_depreciation_per_year + it_hw_depreciation_per_year
        tax_shield = annual_depreciation * sa.get('corporate_tax_rate', 0.25)
        tax_shield_5yr_pv += tax_shield / ((1 + econ_assumptions['discount_rate']) ** (i+1))

    # --- 7. Final Integrated TCO Calculation ---
    total_investment_cost = dc_construction_capex + it_hardware_capex
    total_operating_cost_pv = energy_tco_5yr + maintenance_cost_5yr_pv
    integrated_tco = (total_investment_cost + total_operating_cost_pv) - tax_shield_5yr_pv

    # --- 8. [NEW] Calculate Required Revenue for Target IRR ---
    # To achieve target IRR, PV of cash inflows must equal PV of cash outflows (TCO).
    pv_of_outflows = integrated_tco
    
    # Calculate Present Value Annuity Factor
    if target_irr > 0:
        pvaf = (1 - (1 + target_irr)**-5) / target_irr
    else:
        pvaf = 5

    required_annual_revenue = pv_of_outflows / pvaf if pvaf > 0 else 0
    
    # Translate revenue into business metrics (using final year capacity)
    avg_annual_demand_mwh = adj_demand_profile['demand_mwh'].mean()
    tokens_per_mwh = ra.get('tokens_processed_per_mwh', 1)
    
    total_tokens_per_year = avg_annual_demand_mwh * tokens_per_mwh
    price_per_million_tokens = (required_annual_revenue / (total_tokens_per_year / 1_000_000)) if total_tokens_per_year > 0 else 0
    
    users_per_mw = ra.get('active_users_per_mw', 1)
    total_users = total_it_load_mw * users_per_mw
    monthly_fee_per_user = (required_annual_revenue / total_users / 12) if total_users > 0 else 0
    
    # --- 9. Prepare Summary Output ---
    summary = {
        "final_integrated_tco_5yr": integrated_tco,
        "investment_per_mw": integrated_tco / total_it_load_mw if total_it_load_mw > 0 else 0,
        "breakdown": {
            "A_DC_Construction_CAPEX": dc_construction_capex,
            "B_IT_Hardware_CAPEX": it_hardware_capex,
            "C_Energy_TCO_5yr": energy_tco_5yr,
            "D_Maintenance_Cost_5yr_PV": maintenance_cost_5yr_pv,
            "E_Tax_Shield_5yr_PV": -tax_shield_5yr_pv,
        },
        "viability": {
            "required_annual_revenue": required_annual_revenue,
            "price_per_million_tokens": price_per_million_tokens,
            "monthly_fee_per_user": monthly_fee_per_user
        }
    }
    return summary
