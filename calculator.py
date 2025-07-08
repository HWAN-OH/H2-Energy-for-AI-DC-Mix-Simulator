mport streamlit as st
import pandas as pd
import numpy as np

def calculate_5yr_tco(config, user_inputs):
    """
    Calculates the 5-year TCO using a simplified config structure.
    단순화된 config 구조를 사용하여 5년 TCO를 계산합니다.
    """
    
    demand_profile = user_inputs['demand_profile']
    energy_mix = user_inputs['energy_mix']
    econ_assumptions = user_inputs['econ_assumptions']
    
    # --- FIX: Directly access the simplified 'energy_sources' ---
    # 단순화된 'energy_sources'에 직접 접근합니다.
    tech_params = config.get('energy_sources', {})
    if not tech_params:
        st.error("Configuration Error: 'energy_sources' section is missing in config.yml.")
        return pd.DataFrame(), {}

    results = []
    total_capex_pv = 0
    total_opex_pv = 0

    for year in range(1, config.get('simulation_period_years', 5) + 1):
        # Use standardized lowercase column names
        # 표준화된 소문자 열 이름을 사용합니다.
        demand_row = demand_profile[demand_profile['year'] == year]
        if demand_row.empty: continue
            
        annual_demand_kwh = demand_row['demand_mwh'].iloc[0] * 1000
        peak_demand_kw = demand_row['peak_demand_mw'].iloc[0] * 1000

        # --- 1. Calculate Annual CAPEX ---
        annual_capex = 0
        if year == 1:
            for source, mix in energy_mix.items():
                if source != 'grid' and mix > 0:
                    capacity_kw = peak_demand_kw * (mix / 100)
                    annual_capex += capacity_kw * tech_params.get(source, {}).get('capex_per_kw', 0)
        
        # Fuel cell stack replacement
        # 연료전지 스택 교체
        fc_params = tech_params.get('hydrogen_SOFC', {})
        stack_lifetime = fc_params.get('stack_lifetime_years', 3)
        if year == stack_lifetime + 1 and energy_mix.get('hydrogen_SOFC', 0) > 0:
            fc_capacity_kw = peak_demand_kw * (energy_mix['hydrogen_SOFC'] / 100)
            replacement_rate = fc_params.get('stack_replacement_cost_rate', 0.4)
            annual_capex += (fc_capacity_kw * fc_params.get('capex_per_kw', 0)) * replacement_rate

        # --- 2. Calculate Annual OPEX ---
        annual_opex = 0
        total_energy_generated = 1 # Avoid division by zero
        total_emissions_kg = 0
        
        # Grid
        grid_params = tech_params.get('grid', {})
        grid_kwh = annual_demand_kwh * (energy_mix.get('grid', 0) / 100)
        grid_price = grid_params.get('price_per_kwh', 0.12) * ((1 + econ_assumptions['grid_escalation']) ** (year - 1))
        annual_opex += grid_kwh * grid_price
        total_energy_generated += grid_kwh
        total_emissions_kg += grid_kwh * grid_params.get('carbon_emission_factor', 0)
        
        # Renewables & Fuel Cell
        for source in ['solar', 'wind', 'hydrogen_SOFC']:
            if energy_mix.get(source, 0) > 0:
                source_params = tech_params.get(source, {})
                capacity_kw = peak_demand_kw * (energy_mix[source] / 100)
                
                # O&M Cost
                annual_opex += (capacity_kw * source_params.get('capex_per_kw', 0)) * source_params.get('opex_rate', 0.015)
                
                # Energy Generation & Fuel Cost
                if source == 'hydrogen_SOFC':
                    energy_kwh = annual_demand_kwh * (energy_mix[source] / 100)
                    fuel_cost = econ_assumptions['h2_fuel_cost'] * ((1 + econ_assumptions['fuel_escalation']) ** (year - 1))
                    annual_opex += energy_kwh * fuel_cost
                else: # Solar & Wind
                    energy_kwh = capacity_kw * 8760 * source_params.get('capacity_factor', 0)
                
                total_energy_generated += energy_kwh

        # Carbon Tax
        if econ_assumptions['carbon_tax_year'] and year >= econ_assumptions['carbon_tax_year']:
            annual_opex += (total_emissions_kg / 1000) * econ_assumptions['carbon_tax_price']

        # --- 3. Store results ---
        discount_factor = 1 / ((1 + econ_assumptions['discount_rate']) ** year)
        capex_pv = annual_capex * discount_factor
        opex_pv = annual_opex * discount_factor
        total_capex_pv += capex_pv
        total_opex_pv += opex_pv
        results.append({
            'year': year,
            'annual capex': annual_capex,
            'annual opex': annual_opex,
            'total annual cost': annual_capex + annual_opex,
            'capex (pv)': capex_pv,
            'opex (pv)': opex_pv,
            'total cost (pv)': capex_pv + opex_pv,
            'lcoe ($/mwh)': ((annual_capex + annual_opex) / total_energy_generated) * 1000
        })

    tco_5yr = total_capex_pv + total_opex_pv
    
    summary = {
        '5_Year_TCO': tco_5yr,
        'Total_CAPEX_PV': total_capex_pv,
        'Total_OPEX_PV': total_opex_pv,
        'LCOE_Avg_5yr': (tco_5yr / (demand_profile['demand_mwh'].sum() * 1000)) if demand_profile['demand_mwh'].sum() > 0 else 0
    }
    return pd.DataFrame(results), summary
