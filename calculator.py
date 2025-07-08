import streamlit as st
import pandas as pd
import numpy as np

def calculate_5yr_tco(config, user_inputs):
    """
    Calculates the 5-year Total Cost of Ownership (TCO) for a given energy mix scenario.
    This version includes robust error handling for config file structure.
    """
    
    # Unpack user inputs
    demand_profile = user_inputs['demand_profile']
    energy_mix = user_inputs['energy_mix']
    econ_assumptions = user_inputs['econ_assumptions']
    
    # --- FIX: Defensively access config parameters using .get() ---
    transition_phase_config = config.get('transition_phase', {})
    initial_phase_config = config.get('initial_phase', {})

    if not transition_phase_config or not initial_phase_config:
        st.error("Configuration Error: 'initial_phase' or 'transition_phase' section is missing in config.yml.")
        return pd.DataFrame(), {}

    tech_params = transition_phase_config.get('energy_sources', {})
    grid_params = initial_phase_config.get('energy_sources', {}).get('grid', {})

    if not tech_params or not grid_params:
        st.error("Configuration Error: 'energy_sources' or 'grid' section is missing in config.yml.")
        return pd.DataFrame(), {}

    results = []
    total_capex_pv = 0
    total_opex_pv = 0

    for year in range(1, config.get('simulation_period_years', 5) + 1):
        demand_row = demand_profile[demand_profile['Year'] == year]
        if demand_row.empty:
            continue
            
        annual_demand_kwh = demand_row['Demand_MWh'].iloc[0] * 1000
        peak_demand_kw = demand_row['Peak_Demand_MW'].iloc[0] * 1000

        # --- 1. Calculate Annual CAPEX ---
        annual_capex = 0
        if year == 1:
            for source, mix in energy_mix.items():
                if source != 'grid' and mix > 0:
                    capacity_kw = peak_demand_kw * (mix / 100)
                    source_params = tech_params.get(source) or tech_params.get('hydrogen', {}).get('SOFC', {})
                    if source_params:
                        annual_capex += capacity_kw * source_params.get('capex_per_kw', 0)

        # Fuel cell stack replacement
        fc_params = tech_params.get('hydrogen', {}).get('SOFC', {})
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
        grid_kwh = annual_demand_kwh * (energy_mix.get('grid', 0) / 100)
        grid_price = grid_params.get('price_per_kwh', 0.12) * ((1 + econ_assumptions['grid_escalation']) ** (year - 1))
        annual_opex += grid_kwh * grid_price
        total_energy_generated += grid_kwh
        total_emissions_kg += grid_kwh * grid_params.get('carbon_emission_factor', 0)
        
        # Renewables
        for source in ['solar', 'wind']:
            if energy_mix.get(source, 0) > 0:
                source_params = tech_params.get(source, {})
                capacity_kw = peak_demand_kw * (energy_mix[source] / 100)
                annual_opex += (capacity_kw * source_params.get('capex_per_kw', 0)) * source_params.get('opex_rate', 0.015)
                energy_kwh = capacity_kw * 8760 * source_params.get('capacity_factor', 0)
                total_energy_generated += energy_kwh

        # Hydrogen SOFC
        if energy_mix.get('hydrogen_SOFC', 0) > 0:
            fc_kwh_generated = annual_demand_kwh * (energy_mix['hydrogen_SOFC'] / 100)
            fuel_cost = econ_assumptions['h2_fuel_cost'] * ((1 + econ_assumptions['fuel_escalation']) ** (year - 1))
            annual_opex += fc_kwh_generated * fuel_cost
            total_energy_generated += fc_kwh_generated

        # Carbon Tax
        if econ_assumptions['carbon_tax_year'] and year >= econ_assumptions['carbon_tax_year']:
            annual_opex += (total_emissions_kg / 1000) * econ_assumptions['carbon_tax_price']

        # --- 3. Store results and calculate PV ---
        discount_factor = 1 / ((1 + econ_assumptions['discount_rate']) ** year)
        capex_pv = annual_capex * discount_factor
        opex_pv = annual_opex * discount_factor
        
        total_capex_pv += capex_pv
        total_opex_pv += opex_pv

        results.append({
            'Year': year, 'Annual CAPEX': annual_capex, 'Annual OPEX': annual_opex,
            'Total Annual Cost': annual_capex + annual_opex, 'CAPEX (PV)': capex_pv,
            'OPEX (PV)': opex_pv, 'Total Cost (PV)': capex_pv + opex_pv,
            'LCOE ($/MWh)': ((annual_capex + annual_opex) / total_energy_generated) * 1000
        })

    tco_5yr = total_capex_pv + total_opex_pv
    
    summary = {
        '5_Year_TCO': tco_5yr, 'Total_CAPEX_PV': total_capex_pv,
        'Total_OPEX_PV': total_opex_pv,
        'LCOE_Avg_5yr': (tco_5yr / (demand_profile['Demand_MWh'].sum() * 1000)) * 1000 if demand_profile['Demand_MWh'].sum() > 0 else 0
    }

    return pd.DataFrame(results), summary
