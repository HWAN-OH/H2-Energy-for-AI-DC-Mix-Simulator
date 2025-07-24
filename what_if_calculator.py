# what_if_calculator.py
# This module is dedicated to the 'What-If' analysis for the fixed-fee pricing scenario.

def analyze_fixed_fee_scenario(segment_narratives, standard_fee, premium_fee):
    """
    Calculates the profit and opportunity cost for a fixed-fee scenario.
    This calculation is completely independent of the main usage-based model.

    Args:
        segment_narratives (list): A list of dictionaries containing the pre-calculated
                                   usage-based metrics for each user segment.
        standard_fee (float): The user-defined monthly fee for the Standard tier.
        premium_fee (float): The user-defined monthly fee for the Premium tier.

    Returns:
        list: The updated list of segment narrative dictionaries, with new keys
              for the fixed-fee analysis.
    """
    what_if_results = []
    for segment in segment_narratives:
        # Create a copy to avoid modifying the original data
        updated_segment = segment.copy()

        fixed_fee = 0
        if segment['tier_name_key'] == 'tier_standard':
            fixed_fee = standard_fee
        elif segment['tier_name_key'] == 'tier_premium':
            fixed_fee = premium_fee
        
        # The core cost per user is already calculated based on the true usage potential.
        cost_per_user = segment['cost_per_user']
        usage_based_revenue_per_user = segment['revenue_per_user']

        # Calculate the what-if metrics
        new_profit_per_user = fixed_fee - cost_per_user
        opportunity_cost = usage_based_revenue_per_user - fixed_fee
        
        updated_segment['fixed_fee'] = fixed_fee
        updated_segment['new_profit_per_user'] = new_profit_per_user
        updated_segment['opportunity_cost'] = opportunity_cost
        
        what_if_results.append(updated_segment)
        
    return what_if_results
