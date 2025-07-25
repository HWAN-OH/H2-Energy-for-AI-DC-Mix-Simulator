# what_if_calculator.py (v2.0 - Standalone P&L Calculation)
# This module is dedicated to the 'What-If' analysis for the fixed-fee pricing scenario.

def analyze_fixed_fee_scenario(core_results, standard_fee, premium_fee):
    """
    Calculates the profit, opportunity cost, and a full P&L for a fixed-fee scenario.
    This calculation is completely independent of the main usage-based model.

    Args:
        core_results (dict): The full results dictionary from the core calculator.
        standard_fee (float): The user-defined monthly fee for the Standard tier.
        premium_fee (float): The user-defined monthly fee for the Premium tier.

    Returns:
        tuple: A tuple containing:
            - what_if_narratives (list): The updated list of segment narratives.
            - pnl_what_if (dict): A new P&L dictionary for the what-if scenario.
    """
    segment_narratives = core_results['segment_narratives']
    pnl_core = core_results['pnl_annual']
    
    what_if_narratives = []
    total_users_standard = 0
    total_users_premium = 0

    for segment in segment_narratives:
        updated_segment = segment.copy()

        fixed_fee = 0
        if segment['tier_name_key'] == 'tier_standard':
            fixed_fee = standard_fee
            total_users_standard = segment['num_users']
        elif segment['tier_name_key'] == 'tier_premium':
            fixed_fee = premium_fee
            total_users_premium = segment['num_users']
        
        cost_per_user = segment['cost_per_user']
        usage_based_revenue_per_user = segment['revenue_per_user']

        new_profit_per_user = fixed_fee - cost_per_user
        opportunity_cost = usage_based_revenue_per_user - fixed_fee
        
        updated_segment['fixed_fee'] = fixed_fee
        updated_segment['new_profit_per_user'] = new_profit_per_user
        updated_segment['opportunity_cost'] = opportunity_cost
        
        what_if_narratives.append(updated_segment)
        
    # --- [NEW] Calculate the full annual P&L for this what-if scenario ---
    # Base costs that don't depend on revenue
    cost_of_revenue = pnl_core['cost_of_revenue']
    d_and_a = pnl_core['d_and_a']
    rd_amortization = pnl_core['rd_amortization']
    
    # Revenue-dependent costs
    what_if_revenue = (total_users_standard * standard_fee + total_users_premium * premium_fee) * 12
    what_if_sg_and_a = what_if_revenue * (pnl_core['sg_and_a'] / pnl_core['revenue'] if pnl_core['revenue'] > 0 else 0) # Use the same SG&A rate
    
    what_if_gross_profit = what_if_revenue - cost_of_revenue
    what_if_operating_profit = what_if_gross_profit - what_if_sg_and_a - d_and_a - rd_amortization
    
    pnl_what_if = {
        'revenue': what_if_revenue,
        'cost_of_revenue': cost_of_revenue,
        'gross_profit': what_if_gross_profit,
        'sg_and_a': what_if_sg_and_a,
        'd_and_a': d_and_a,
        'rd_amortization': rd_amortization,
        'operating_profit': what_if_operating_profit,
    }
        
    return what_if_narratives, pnl_what_if
