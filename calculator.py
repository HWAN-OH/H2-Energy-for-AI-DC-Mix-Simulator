# calculator.py (v17.0 - Final Logic Separation Fix)
import yaml
import pandas as pd

def calculate_business_case(
    dc_size_mw,
    use_clean_power,
    apply_mirrormind,
    high_perf_gpu_ratio,
    utilization_rate,
    market_price_per_m_tokens,
    standard_fee,
    premium_fee,
    lang
):
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    inv_conf = config['investment']
    hw_conf = config['hardware']
    op_conf = config['operating_expenses']
    rd_conf = config['research_and_development']
    model_conf = config['model_and_market']
    tiers_conf = model_conf['tiers']

    HOURS_PER_YEAR = 8760
    PAYBACK_YEARS_TARGET = 5
    high_perf_gpu_ratio /= 100.0

    # --- 1. CAPEX & GPU ---
    dc_construction_cost = inv_conf['dc_capex_per_mw'] * dc_size_mw
    it_hw_budget = inv_conf['it_budget_per_mw'] * dc_size_mw
    total_investment = dc_construction_cost + it_hw_budget
    num_high_perf_gpus = (it_hw_budget * high_perf_gpu_ratio) // hw_conf['high_perf_gpu']['cost'] if hw_conf['high_perf_gpu']['cost'] > 0 else 0
    num_standard_gpus = (it_hw_budget * (1 - high_perf_gpu_ratio)) // hw_conf['standard_gpu']['cost'] if hw_conf['standard_gpu']['cost'] > 0 else 0

    # --- 2. Capacity ---
    arch_efficiency = model_conf['intelligent_arch_efficiency'] if apply_mirrormind else 1.0
    tokens_from_high_perf = num_high_perf_gpus * hw_conf['high_perf_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    tokens_from_standard = num_standard_gpus * hw_conf['standard_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    total_token_capacity = (tokens_from_high_perf + tokens_from_standard) * arch_efficiency
    serviced_tokens = total_token_capacity * (utilization_rate / 100.0)

    # --- 3. Base Costs (Revenue Independent) ---
    it_power_consumption_mw = dc_size_mw * (utilization_rate / 100.0)
    total_power_consumption_mw = it_power_consumption_mw * op_conf['pue']
    power_cost_kwh_rate = 0.18 if use_clean_power == 'Renewable' else 0.12
    power_cost = total_power_consumption_mw * HOURS_PER_YEAR * 1000 * power_cost_kwh_rate
    maintenance_cost = op_conf['maintenance_and_cooling_per_mw'] * dc_size_mw
    personnel_cost = op_conf['personnel_and_other_per_mw'] * dc_size_mw
    cost_of_revenue = power_cost + maintenance_cost + personnel_cost
    
    dc_depreciation = dc_construction_cost / inv_conf['amortization_years']['datacenter']
    it_depreciation = it_hw_budget / inv_conf['amortization_years']['it_hardware']
    rd_amortization = (rd_conf['total_model_development_cost'] / rd_conf['global_datacenter_count_for_cost_allocation']) / inv_conf['amortization_years']['research_and_development']
    d_and_a = dc_depreciation + it_depreciation
    
    base_operating_cost = cost_of_revenue + d_and_a + rd_amortization
    sgna_rate = op_conf['sgna_as_percent_of_revenue'] / 100.0

    # --- 4. Per-User Metrics Calculation ---
    total_users = model_conf['total_users_for_100mw'] * (dc_size_mw / 100.0)
    total_token_demand_ratio = sum(t['ratio'] * t['monthly_token_usage_m'] for t in tiers_conf.values())
    
    segment_narrative_data = []
    for tier_name, tier_info in tiers_conf.items():
        num_users_in_tier = total_users * tier_info['ratio']
        if num_users_in_tier == 0: continue

        token_usage_ratio = (tier_info['ratio'] * tier_info['monthly_token_usage_m']) / total_token_demand_ratio if total_token_demand_ratio > 0 else 0
        
        # --- 4.1. Usage-Based Scenario (for Section 2) ---
        tier_revenue_annual_usage_based = (serviced_tokens * token_usage_ratio / 1e6) * market_price_per_m_tokens if tier_name != 'free' else 0
        revenue_per_user_annual = tier_revenue_annual_usage_based / num_users_in_tier if num_users_in_tier > 0 else 0
        
        # To calculate usage-based profit, we need a usage-based total cost
        usage_based_revenue_total = (serviced_tokens / 1e6) * market_price_per_m_tokens * sum(t['ratio'] for n, t in tiers_conf.items() if n != 'free')
        usage_based_sgna = usage_based_revenue_total * sgna_rate
        usage_based_total_cost = base_operating_cost + usage_based_sgna
        
        tier_cost_annual_usage_based = usage_based_total_cost * token_usage_ratio
        cost_per_user_annual_usage_based = tier_cost_annual_usage_based / num_users_in_tier if num_users_in_tier > 0 else 0
        
        # --- 4.2. Fixed-Fee Scenario (for Section 3) ---
        fixed_fee = 0
        if tier_name == 'standard': fixed_fee = standard_fee
        elif tier_name == 'premium': fixed_fee = premium_fee
        
        # To calculate fixed-fee profit, we need a fixed-fee total cost
        fixed_fee_revenue_total = (total_users * tiers_conf['standard']['ratio'] * standard_fee + total_users * tiers_conf['premium']['ratio'] * premium_fee) * 12
        fixed_fee_sgna = fixed_fee_revenue_total * sgna_rate
        fixed_fee_total_cost = base_operating_cost + fixed_fee_sgna
        
        tier_cost_annual_fixed_fee = fixed_fee_total_cost * token_usage_ratio
        cost_per_user_annual_fixed_fee = tier_cost_annual_fixed_fee / num_users_in_tier if num_users_in_tier > 0 else 0
        
        new_profit_per_user = fixed_fee - (cost_per_user_annual_fixed_fee / 12.0)
        opportunity_cost = (revenue_per_user_annual / 12.0) - fixed_fee

        segment_narrative_data.append({
            "tier_name_key": f"tier_{tier_name}", "num_users": num_users_in_tier,
            "revenue_per_user": revenue_per_user_annual / 12.0,
            "cost_per_user": cost_per_user_annual_usage_based / 12.0, # Section 2 uses usage-based cost
            "profit_per_user": (revenue_per_user_annual - cost_per_user_annual_usage_based) / 12.0,
            "fixed_fee": fixed_fee,
            "new_profit_per_user": new_profit_per_user, # Section 3 uses fixed-fee cost
            "opportunity_cost": opportunity_cost,
        })

    # --- 5. Recommended Pricing Calculation (Based on Usage Potential) ---
    target_annual_op_profit = total_investment / PAYBACK_YEARS_TARGET
    required_annual_revenue = (target_annual_op_profit + base_operating_cost) / (1 - sgna_rate)
    
    total_potential_revenue = sum(s['revenue_per_user'] * 12 * s['num_users'] for s in segment_narrative_data if s['tier_name_key'] != 'tier_free')
    price_ratio = required_annual_revenue / total_potential_revenue if total_potential_revenue > 0 else 1

    recommended_standard_fee = segment_narrative_data[1]['revenue_per_user'] * price_ratio
    recommended_premium_fee = segment_narrative_data[2]['revenue_per_user'] * price_ratio
    
    recommendation = {
        "standard_fee": recommended_standard_fee,
        "premium_fee": recommended_premium_fee,
        "is_achievable": recommended_premium_fee < 500 and recommended_standard_fee < 100
    }

    # --- 6. Final P&L for Display (Section 1 - Based on Fixed-Fee Scenario) ---
    pnl_annual = {
        'revenue': fixed_fee_revenue_total, 
        'cost_of_revenue': cost_of_revenue, 
        'gross_profit': fixed_fee_revenue_total - cost_of_revenue,
        'sg_and_a': fixed_fee_sgna, 
        'd_and_a': d_and_a, 
        'it_depreciation': it_depreciation,
        'rd_amortization': rd_amortization,
        'operating_profit': fixed_fee_revenue_total - fixed_fee_total_cost,
        'annual_cash_flow': (fixed_fee_revenue_total - fixed_fee_total_cost) + d_and_a,
    }

    results = {
        "pnl_annual": pnl_annual,
        "segment_narratives": segment_narrative_data,
        "total_investment": total_investment,
        "assumptions": {
            "gpu_mix_string": f"H:{int(num_high_perf_gpus)} / S:{int(num_standard_gpus)}",
            "utilization_rate": utilization_rate,
            "serviced_tokens_t": serviced_tokens / 1e12,
        },
        "recommendation": recommendation,
    }
    return results
