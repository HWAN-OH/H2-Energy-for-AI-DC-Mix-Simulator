import pandas as pd
import numpy as np

def calculate_5yr_tco(config, user_inputs):
    """
    Calculates 5-year TCO with detailed cost breakdowns for CAPEX and OPEX.
    """
    demand_profile = user_inputs['demand_profile']
    energy_mix = user_inputs['energy_mix']
    econ_assumptions = user_inputs['econ_assumptions']
    scenario_params = user_inputs['scenario_params']
    
    tech_params = config.get('energy_sources', {})
    asset_lifetime = config.get('asset_lifetime_years', 20)
    discount_rate = econ_assumptions['discount_rate']

    # --- Initial CAPEX Calculation ---
    initial_capex = 0
    capex_details = {}
    peak_demand_kw_yr1 = demand_profile['peak_demand_mw'].iloc[0] * 1000

    for source, mix in energy_mix.items():
        if source != 'grid' and mix > 0:
            capacity_kw = peak_demand_kw_yr1 * (mix / 100)
            capex = capacity_kw * tech_params.get(source, {}).get('capex_per_kw', 0)
            capex_details[f"{source}_capex"] = capex
            initial_capex += capex

    # --- Initialize variables for loop ---
    results = []
    opex_breakdown_pv = {}
    total_opex_pv = 0
    total_capex_pv = initial_capex # Year 1 CAPEX is already at PV
    total_demand_pv_kwh = 0

    for index, demand_row in demand_profile.iterrows():
        simulation_year = index + 1
        actual_year = demand_row['year']
        annual_demand_kwh = demand_row['demand_mwh'] * 1000
        peak_demand_kw = demand_row['peak_demand_mw'] * 1000
        discount_factor = 1 / ((1 + discount_rate) ** simulation_year)

        # --- Annual CAPEX (Replacements) ---
        annual_capex_replacement = 0
        fc_params = tech_params.get('hydrogen_SOFC', {})
        stack_lifetime = fc_params.get('stack_lifetime_years', 4)
        if simulation_year > 1 and (simulation_year - 1) % stack_lifetime == 0 and energy_mix.get('hydrogen_SOFC', 0) > 0:
            fc_capacity_kw = peak_demand_kw_yr1 * (energy_mix['hydrogen_SOFC'] / 100)
            replacement_rate = fc_params.get('stack_replacement_cost_rate', 0.4)
            replacement_cost = (fc_capacity_kw * fc_params.get('capex_per_kw', 0)) * replacement_rate
            annual_capex_replacement = replacement_cost
            capex_details["h2_stack_replacement_cost_y" + str(simulation_year)] = replacement_cost
        
        total_capex_pv += annual_capex_replacement * discount_factor
        
        # --- Annual OPEX Calculation ---
        opex_details_annual = {}
        initial_grid_price = scenario_params.get('grid_price_per_kwh', 0.12)
        initial_ng_price = scenario_params.get('gas_fuel_cost_per_kwh', 0.08)

        grid_kwh = annual_demand_kwh * (energy_mix.get('grid', 0) / 100)
        opex_details_annual['grid_purchase_cost'] = grid_kwh * (initial_grid_price * ((1 + econ_assumptions['grid_escalation']) ** (simulation_year - 1)))
        
        total_emissions_kg = grid_kwh * tech_params.get('grid', {}).get('carbon_emission_factor', 0)
        
        opex_details_annual['o&m_cost'] = 0
        opex_details_annual['h2_fuel_cost'] = 0
        opex_details_annual['ng_fuel_cost'] = 0

        for source in ['solar', 'wind', 'hydrogen_SOFC', 'NG_SOFC']:
            if energy_mix.get(source, 0) > 0:
                capacity_kw = peak_demand_kw_yr1 * (energy_mix[source] / 100)
                opex_details_annual['o&m_cost'] += (capacity_kw * tech_params.get(source, {}).get('capex_per_kw', 0)) * tech_params.get(source, {}).get('opex_rate', 0.015)
                
                if source == 'hydrogen_SOFC':
                    opex_details_annual['h2_fuel_cost'] += (annual_demand_kwh * (energy_mix[source] / 100)) * (econ_assumptions['h2_fuel_cost'] * ((1 + econ_assumptions['fuel_escalation']) ** (simulation_year - 1)))
                elif source == 'NG_SOFC':
                    ng_kwh = annual_demand_kwh * (energy_mix[source] / 100)
                    opex_details_annual['ng_fuel_cost'] += ng_kwh * (initial_ng_price * ((1 + econ_assumptions['fuel_escalation']) ** (simulation_year - 1)))
                    total_emissions_kg += ng_kwh * tech_params.get(source, {}).get('carbon_emission_factor', 0)

        opex_details_annual['carbon_tax_cost'] = 0
        if econ_assumptions['carbon_tax_year'] and simulation_year >= econ_assumptions['carbon_tax_year']:
            opex_details_annual['carbon_tax_cost'] = (total_emissions_kg / 1000) * econ_assumptions['carbon_tax_price']
        
        annual_opex = sum(opex_details_annual.values())
        opex_pv = annual_opex * discount_factor
        total_opex_pv += opex_pv
        total_demand_pv_kwh += annual_demand_kwh * discount_factor

        # Accumulate PV of each OPEX component
        for key, value in opex_details_annual.items():
            opex_breakdown_pv[key] = opex_breakdown_pv.get(key, 0) + (value * discount_factor)
        
        results.append({
            'year': actual_year,
            'annual_capex': initial_capex if simulation_year == 1 else annual_capex_replacement,
            'annual_opex': annual_opex,
        })

    tco_5yr = total_capex_pv + total_opex_pv
    
    summary = {
        '5_Year_TCO': tco_5yr,
        'Total_CAPEX_PV': total_capex_pv,
        'Total_OPEX_PV': total_opex_pv,
        'LCOE_Avg_5yr': (tco_5yr / total_demand_pv_kwh) * 1000 if total_demand_pv_kwh > 0 else 0
    }
    
    return pd.DataFrame(results), summary, capex_details, opex_breakdown_pv
