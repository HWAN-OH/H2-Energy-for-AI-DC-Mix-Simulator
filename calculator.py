import pandas as pd
import numpy as np

def calculate_5yr_tco(config, user_inputs):
    """
    Calculates the 5-year Total Cost of Ownership (TCO) for a given energy mix scenario.
    """
    
    # Unpack user inputs
    demand_profile = user_inputs['demand_profile']
    energy_mix = user_inputs['energy_mix']
    econ_assumptions = user_inputs['econ_assumptions']
    
    # Get technology parameters from config
    tech_params = config['energy_sources']

    results = []
    total_capex_pv = 0
    total_opex_pv = 0

    for year in range(1, config['simulation_period_years'] + 1):
        annual_demand_kwh = demand_profile.loc[demand_profile['Year'] == year, 'Demand_MWh'].iloc[0] * 1000
        peak_demand_kw = demand_profile.loc[demand_profile['Year'] == year, 'Peak_Demand_MW'].iloc[0] * 1000

        # --- 1. Calculate Annual CAPEX ---
        annual_capex = 0
        
        # Initial investment in Year 1
        if year == 1:
            for source, mix in energy_mix.items():
                if source != 'grid' and mix > 0:
                    capacity_kw = peak_demand_kw * (mix / 100)
                    annual_capex += capacity_kw * tech_params[source]['capex_per_kw']
        
        # Fuel cell stack replacement
        fc_params = tech_params['hydrogen_SOFC']
        if year == fc_params['stack_lifetime_years'] + 1 and energy_mix.get('hydrogen_SOFC', 0) > 0:
            fc_capacity_kw = peak_demand_kw * (energy_mix['hydrogen_SOFC'] / 100)
            annual_capex += (fc_capacity_kw * fc_params['capex_per_kw']) * fc_params['stack_replacement_cost_rate']

        # --- 2. Calculate Annual OPEX ---
        annual_opex = 0
        total_energy_generated = 0
        total_emissions_kg = 0
        
        # Grid cost & emissions
        grid_kwh = annual_demand_kwh * (energy_mix.get('grid', 0) / 100)
        grid_price = tech_params['grid']['price_per_kwh'] * ((1 + econ_assumptions['grid_escalation']) ** (year - 1))
        annual_opex += grid_kwh * grid_price
        total_energy_generated += grid_kwh
        total_emissions_kg += grid_kwh * tech_params['grid']['carbon_emission_factor']
        
        # Solar & Wind OPEX and generation
        for source in ['solar', 'wind']:
            if energy_mix.get(source, 0) > 0:
                capacity_kw = peak_demand_kw * (energy_mix[source] / 100)
                annual_opex += (capacity_kw * tech_params[source]['capex_per_kw']) * tech_params[source]['opex_rate']
                energy_kwh = capacity_kw * 8760 * tech_params[source]['capacity_factor']
                total_energy_generated += energy_kwh

        # Hydrogen SOFC OPEX and generation
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
            'Year': year,
            'Annual CAPEX': annual_capex,
            'Annual OPEX': annual_opex,
            'Total Annual Cost': annual_capex + annual_opex,
            'CAPEX (PV)': capex_pv,
            'OPEX (PV)': opex_pv,
            'Total Cost (PV)': capex_pv + opex_pv,
            'LCOE ($/MWh)': ((annual_capex + annual_opex) / total_energy_generated) * 1000 if total_energy_generated > 0 else 0
        })

    tco_5yr = total_capex_pv + total_opex_pv
    
    summary = {
        '5_Year_TCO': tco_5yr,
        'Total_CAPEX_PV': total_capex_pv,
        'Total_OPEX_PV': total_opex_pv,
        'LCOE_Avg_5yr': (tco_5yr / (demand_profile['Demand_MWh'].sum() * 1000)) * 1000 if demand_profile['Demand_MWh'].sum() > 0 else 0
    }

    return pd.DataFrame(results), summary
