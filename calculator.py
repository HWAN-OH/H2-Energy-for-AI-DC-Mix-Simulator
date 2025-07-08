import pandas as pd
import numpy as np

def calculate_5yr_tco(config, user_inputs):
    """
    Calculates the 5-year TCO. This version corrects the LCOE calculation.
    LCOE 계산 로직이 수정된 버전입니다.
    """
    demand_profile = user_inputs['demand_profile']
    energy_mix = user_inputs['energy_mix']
    econ_assumptions = user_inputs['econ_assumptions']
    
    tech_params = config.get('energy_sources', {})
    if not tech_params:
        # This case is handled in app.py, but as a safeguard:
        # app.py에서 처리되지만, 안전장치로 추가합니다.
        return pd.DataFrame(), {}

    results = []
    total_capex_pv = 0
    total_opex_pv = 0

    # Iterate through the years present in the demand profile
    # demand_profile에 있는 연도를 기준으로 반복합니다.
    for index, demand_row in demand_profile.iterrows():
        
        simulation_year = index + 1 # Relative year for calculations (1, 2, 3...)
        actual_year = demand_row['year'] # Actual year from data (e.g., 2025, 2026...)
            
        annual_demand_kwh = demand_row['demand_mwh'] * 1000
        peak_demand_kw = demand_row['peak_demand_mw'] * 1000

        # --- 1. Calculate Annual CAPEX ---
        annual_capex = 0
        # Initial investment only occurs in the first year of the simulation
        # 초기 투자는 시뮬레이션의 첫 해에만 발생합니다.
        if simulation_year == 1:
            for source, mix in energy_mix.items():
                if source != 'grid' and mix > 0:
                    capacity_kw = peak_demand_kw * (mix / 100)
                    annual_capex += capacity_kw * tech_params.get(source, {}).get('capex_per_kw', 0)
        
        # Fuel cell stack replacement
        # 연료전지 스택 교체
        fc_params = tech_params.get('hydrogen_SOFC', {})
        stack_lifetime = fc_params.get('stack_lifetime_years', 3)
        if simulation_year == stack_lifetime + 1 and energy_mix.get('hydrogen_SOFC', 0) > 0:
            fc_capacity_kw = peak_demand_kw * (energy_mix['hydrogen_SOFC'] / 100)
            replacement_rate = fc_params.get('stack_replacement_cost_rate', 0.4)
            annual_capex += (fc_capacity_kw * fc_params.get('capex_per_kw', 0)) * replacement_rate

        # --- 2. Calculate Annual OPEX ---
        annual_opex = 0
        total_emissions_kg = 0
        
        # Grid
        grid_params = tech_params.get('grid', {})
        grid_kwh = annual_demand_kwh * (energy_mix.get('grid', 0) / 100)
        grid_price = grid_params.get('price_per_kwh', 0.12) * ((1 + econ_assumptions['grid_escalation']) ** (simulation_year - 1))
        annual_opex += grid_kwh * grid_price
        total_emissions_kg += grid_kwh * grid_params.get('carbon_emission_factor', 0)
        
        # Renewables & Fuel Cell
        for source in ['solar', 'wind', 'hydrogen_SOFC']:
            if energy_mix.get(source, 0) > 0:
                source_params = tech_params.get(source, {})
                capacity_kw = peak_demand_kw * (energy_mix[source] / 100)
                
                # O&M Cost
                annual_opex += (capacity_kw * source_params.get('capex_per_kw', 0)) * source_params.get('opex_rate', 0.015)
                
                # Fuel Cost for SOFC
                if source == 'hydrogen_SOFC':
                    energy_kwh = annual_demand_kwh * (energy_mix[source] / 100)
                    fuel_cost = econ_assumptions['h2_fuel_cost'] * ((1 + econ_assumptions['fuel_escalation']) ** (simulation_year - 1))
                    annual_opex += energy_kwh * fuel_cost

        # Carbon Tax
        if econ_assumptions['carbon_tax_year'] and simulation_year >= econ_assumptions['carbon_tax_year']:
            annual_opex += (total_emissions_kg / 1000) * econ_assumptions['carbon_tax_price']

        # --- 3. Store results and calculate Present Value (PV) ---
        discount_factor = 1 / ((1 + econ_assumptions['discount_rate']) ** simulation_year)
        capex_pv = annual_capex * discount_factor
        opex_pv = annual_opex * discount_factor
        total_capex_pv += capex_pv
        total_opex_pv += opex_pv
        
        # --- FIX: LCOE denominator is now annual_demand_kwh ---
        # LCOE 분모를 연간 실제 수요량으로 수정합니다.
        lcoe_mwh = ((annual_capex + annual_opex) / annual_demand_kwh) * 1000 if annual_demand_kwh > 0 else 0
        
        results.append({
            'year': actual_year,
            'annual capex': annual_capex,
            'annual opex': annual_opex,
            'total annual cost': annual_capex + annual_opex,
            'capex (pv)': capex_pv,
            'opex (pv)': opex_pv,
            'total cost (pv)': capex_pv + opex_pv,
            'lcoe ($/mwh)': lcoe_mwh
        })

    tco_5yr = total_capex_pv + total_opex_pv
    total_demand_mwh = demand_profile['demand_mwh'].sum()
    
    summary = {
        '5_Year_TCO': tco_5yr,
        'Total_CAPEX_PV': total_capex_pv,
        'Total_OPEX_PV': total_opex_pv,
        'LCOE_Avg_5yr': (tco_5yr / (total_demand_mwh * 1000)) * 1000 if total_demand_mwh > 0 else 0
    }
    return pd.DataFrame(results), summary
