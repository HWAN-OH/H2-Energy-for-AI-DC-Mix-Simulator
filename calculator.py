import numpy_financial as npf

def calculate_profitability(config, infra_mode):
    """
    Calculates the required revenue and user fees to meet a target IRR
    for a given infrastructure model (Cloud vs. On-Premise) based on cash flow.
    """
    # --- 1. Load all assumptions from config ---
    biz_config = config.get('business_assumptions', {})
    model_config = config.get('model_assumptions', {})
    user_config = config.get('user_assumptions', {})
    infra_config = config['infrastructure_models'][infra_mode]

    analysis_years = biz_config.get('analysis_years', 3)
    target_irr = biz_config.get('target_irr', 0.08)
    
    # --- 2. Construct the Cash Flow timeline ---
    cash_flows = [0] * (analysis_years + 1) # [Year 0, Year 1, ..., Year N]

    # --- 2.1. Year 0 Outflows (Initial Investment) ---
    initial_investment = model_config.get('training_cost', 0)
    if infra_mode == 'on_premise':
        initial_investment += infra_config.get('initial_capex_server', 0)
        initial_investment += infra_config.get('initial_capex_facility', 0)
    cash_flows[0] = -initial_investment

    # --- 2.2. Year 1 to N Outflows (Annual Operating Costs) ---
    annual_opex = biz_config.get('annual_rd_personnel_cost', 0) + infra_config.get('annual_opex', 0)
    for i in range(1, analysis_years + 1):
        cash_flows[i] = -annual_opex

    # --- 3. Calculate the Present Value (PV) of all cash outflows ---
    # This represents the total value of the investment in today's money.
    pv_of_outflows = npf.npv(target_irr, cash_flows)

    # --- 4. Calculate the required annual revenue to achieve the target IRR ---
    # The PV of future revenues must equal the PV of outflows.
    # We use the Present Value of Annuity formula to find the required annual revenue.
    if target_irr > 0:
        pv_annuity_factor = (1 - (1 + target_irr)**-analysis_years) / target_irr
    else:
        pv_annuity_factor = analysis_years
    
    # Note: pv_of_outflows is negative, so we multiply by -1
    required_annual_revenue = (-pv_of_outflows) / pv_annuity_factor if pv_annuity_factor > 0 else 0
    required_monthly_revenue = required_annual_revenue / 12

    # --- 5. Calculate required user fees based on the revenue target ---
    total_users = user_config.get('total_users', 0)
    low_tier_users = total_users * user_config.get('low_tier_user_pct', 0)
    high_tier_users = total_users * user_config.get('high_tier_user_pct', 0)
    pricing_ratio = user_config.get('high_to_low_pricing_ratio', 10)

    # Logic: Monthly Revenue = (low_users * x) + (high_users * ratio * x)
    # x = Monthly Revenue / (low_users + ratio * high_users)
    denominator = low_tier_users + (pricing_ratio * high_tier_users)
    
    low_tier_fee = required_monthly_revenue / denominator if denominator > 0 else 0
    high_tier_fee = low_tier_fee * pricing_ratio

    # --- 6. Prepare Summary Output ---
    summary = {
        "total_cash_outflow_pv": -pv_of_outflows,
        "required_monthly_revenue": required_monthly_revenue,
        "low_tier_fee": low_tier_fee,
        "high_tier_fee": high_tier_fee
    }
    return summary
