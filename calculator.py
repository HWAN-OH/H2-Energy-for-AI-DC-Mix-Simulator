# calculator.py (v3.0 - Refactored P&L Logic)
import yaml
import pandas as pd

def calculate_business_case(
    dc_size_mw,
    use_clean_power,
    apply_mirrormind,
    high_perf_gpu_ratio,
    utilization_rate,
    market_price_per_m_tokens,
    lang
):
    # [1] config.yml 로드
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)

    # --- 설정 값 추출 ---
    inv_conf = config['investment']
    hw_conf = config['hardware']
    op_conf = config['operating_expenses']
    rd_conf = config['research_and_development']
    model_conf = config['model_and_market']
    tiers_conf = model_conf['tiers']

    HOURS_PER_YEAR = 8760
    high_perf_gpu_ratio /= 100.0

    # --- 1. CAPEX 및 GPU 구성 ---
    dc_construction_cost = inv_conf['dc_capex_per_mw'] * dc_size_mw
    it_hw_budget = inv_conf['it_budget_per_mw'] * dc_size_mw
    total_investment = dc_construction_cost + it_hw_budget
    num_high_perf_gpus = (it_hw_budget * high_perf_gpu_ratio) // hw_conf['high_perf_gpu']['cost'] if hw_conf['high_perf_gpu']['cost'] > 0 else 0
    num_standard_gpus = (it_hw_budget * (1 - high_perf_gpu_ratio)) // hw_conf['standard_gpu']['cost'] if hw_conf['standard_gpu']['cost'] > 0 else 0

    # --- 2. 연간 토큰 처리량 (Capacity) ---
    arch_efficiency = model_conf['intelligent_arch_efficiency'] if apply_mirrormind else 1.0
    tokens_from_high_perf = num_high_perf_gpus * hw_conf['high_perf_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    tokens_from_standard = num_standard_gpus * hw_conf['standard_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    total_token_capacity = (tokens_from_high_perf + tokens_from_standard) * arch_efficiency
    serviced_tokens = total_token_capacity * (utilization_rate / 100.0)

    # --- 3. 고객 그룹별 토큰 및 매출 계산 ---
    segment_data = []
    total_token_demand_ratio = sum(t['ratio'] * t['monthly_token_usage_m'] for t in tiers_conf.values())

    for tier_name, tier_info in tiers_conf.items():
        token_usage_ratio = (tier_info['ratio'] * tier_info['monthly_token_usage_m']) / total_token_demand_ratio if total_token_demand_ratio > 0 else 0
        segment_tokens = serviced_tokens * token_usage_ratio
        
        # 그룹별 매출: Free 티어는 0, 나머지는 시장가 적용
        segment_revenue = (segment_tokens / 1e6) * market_price_per_m_tokens if tier_name != 'free' else 0
        
        segment_data.append({
            "segment": tier_name.title(),
            "token_usage_ratio": token_usage_ratio,
            "total_revenue": segment_revenue,
            "total_cost": 0, # Placeholder
            "total_profit": 0 # Placeholder
        })

    # --- 4. 통합 손익계산서 (P&L) 계산 ---
    # 4.1. 매출 (Revenue) - 세그먼트 매출의 합으로 계산하여 논리 일관성 확보
    revenue = sum(s['total_revenue'] for s in segment_data)

    # 4.2. 비용 (Costs)
    # 전력비는 전체 서비스된 토큰량에 기반
    it_power_consumption_mw = (serviced_tokens / total_token_capacity if total_token_capacity > 0 else 0) * (dc_size_mw * (utilization_rate/100))
    total_power_consumption_mw = it_power_consumption_mw * op_conf['pue']
    power_cost_kwh_rate = 0.18 if use_clean_power == 'Renewable' else 0.12
    power_cost = total_power_consumption_mw * HOURS_PER_YEAR * 1000 * power_cost_kwh_rate
    
    cost_of_revenue = power_cost + (op_conf['maintenance_and_cooling_per_mw'] * dc_size_mw)
    sg_and_a = revenue * (op_conf['sgna_as_percent_of_revenue'] / 100.0)
    dc_depreciation = dc_construction_cost / inv_conf['amortization_years']['datacenter']
    it_depreciation = it_hw_budget / inv_conf['amortization_years']['it_hardware']
    rd_amortization = (rd_conf['total_model_development_cost'] / rd_conf['global_datacenter_count_for_cost_allocation']) / inv_conf['amortization_years']['research_and_development']
    d_and_a = dc_depreciation + it_depreciation
    
    total_operating_cost = cost_of_revenue + sg_and_a + d_and_a + rd_amortization

    # 4.3. 이익 (Profit)
    gross_profit = revenue - cost_of_revenue
    operating_profit = gross_profit - sg_and_a - d_and_a - rd_amortization

    # --- 5. 그룹별 비용 및 손익 재계산 ---
    for s in segment_data:
        s['total_cost'] = total_operating_cost * s['token_usage_ratio']
        s['total_profit'] = s['total_revenue'] - s['total_cost']

    # --- 6. 결과 정리 ---
    pnl_annual = {
        'revenue': revenue,
        'cost_of_revenue': cost_of_revenue,
        'gross_profit': gross_profit,
        'sg_and_a': sg_and_a,
        'd_and_a': d_and_a,
        'it_depreciation': it_depreciation,
        'rd_amortization': rd_amortization,
        'operating_profit': operating_profit,
    }
    
    # 결과 출력 전, 중간 계산에 사용된 키(token_usage_ratio) 제거
    pnl_by_segment = [{k: v for k, v in s.items() if k != 'token_usage_ratio'} for s in segment_data]

    results = {
        "pnl_annual": pnl_annual,
        "pnl_by_segment": pnl_by_segment,
        "total_investment": total_investment,
        "assumptions": {
            "gpu_mix_string": f"H:{int(num_high_perf_gpus)} / S:{int(num_standard_gpus)}",
            "utilization_rate": utilization_rate,
            "serviced_tokens_t": serviced_tokens / 1e12,
        },
    }

    return results
