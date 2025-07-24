# calculator.py (수정된 코드)
import yaml
import numpy_financial as npf

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

    HOURS_PER_YEAR = 8760
    high_perf_gpu_ratio /= 100.0  # Convert percentage to ratio

    # --- 1. CAPEX (초기 투자비) 계산 ---
    dc_construction_cost = inv_conf['dc_capex_per_mw'] * dc_size_mw
    it_hw_budget = inv_conf['it_budget_per_mw'] * dc_size_mw

    # GPU 댓수 계산
    num_high_perf_gpus = (it_hw_budget * high_perf_gpu_ratio) // hw_conf['high_perf_gpu']['cost']
    num_standard_gpus = (it_hw_budget * (1 - high_perf_gpu_ratio)) // hw_conf['standard_gpu']['cost']
    total_investment = dc_construction_cost + it_hw_budget

    # --- 2. 연간 토큰 처리량 (Capacity) 계산 ---
    arch_efficiency = model_conf['intelligent_arch_efficiency'] if apply_mirrormind else 1.0
    
    tokens_from_high_perf = num_high_perf_gpus * hw_conf['high_perf_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    tokens_from_standard = num_standard_gpus * hw_conf['standard_gpu']['m_tokens_per_hour'] * 1e6 * HOURS_PER_YEAR
    
    total_token_capacity = (tokens_from_high_perf + tokens_from_standard) * arch_efficiency
    serviced_tokens = total_token_capacity * (utilization_rate / 100.0)

    # --- 3. P&L (손익계산서) 계산 ---
    # 3.1. 매출 (Revenue)
    revenue = (serviced_tokens / 1e6) * market_price_per_m_tokens

    # 3.2. 매출 원가 (Cost of Revenue)
    it_power_consumption_mw = (serviced_tokens / total_token_capacity if total_token_capacity > 0 else 0) * (dc_size_mw * (utilization_rate/100))
    total_power_consumption_mw = it_power_consumption_mw * op_conf['pue']
    power_cost = total_power_consumption_mw * HOURS_PER_YEAR * 1000 * (0.18 if use_clean_power == 'Renewable' else 0.12) # MWh -> kWh
    cost_of_revenue = power_cost + (op_conf['maintenance_and_cooling_per_mw'] * dc_size_mw)
    
    gross_profit = revenue - cost_of_revenue

    # 3.3. 영업 비용 (Operating Expenses)
    sg_and_a = revenue * (op_conf['sgna_as_percent_of_revenue'] / 100.0)
    dc_depreciation = dc_construction_cost / inv_conf['amortization_years']['datacenter']
    it_depreciation = it_hw_budget / inv_conf['amortization_years']['it_hardware']
    rd_amortization = (rd_conf['total_model_development_cost'] / rd_conf['global_datacenter_count_for_cost_allocation']) / inv_conf['amortization_years']['research_and_development']
    d_and_a = dc_depreciation + it_depreciation

    operating_profit = gross_profit - sg_and_a - d_and_a - rd_amortization

    # --- 4. 결과 정리 ---
    pnl_annual = {
        'revenue': revenue,
        'cost_of_revenue': cost_of_revenue,
        'gross_profit': gross_profit,
        'sg_and_a': sg_and_a,
        'd_and_a': d_and_a,
        'it_depreciation': it_depreciation, # 상세 표기를 위해 별도 전달
        'rd_amortization': rd_amortization,
        'operating_profit': operating_profit,
    }

    results = {
        "pnl_annual": pnl_annual,
        "assumptions": {
            "gpu_mix_string": f"H_GPU: {int(num_high_perf_gpus)}, S_GPU: {int(num_standard_gpus)}",
            "utilization_rate": utilization_rate,
            "serviced_tokens_t": serviced_tokens / 1e12, # 조 단위
        },
    }

    return results
