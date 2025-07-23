# localization.py (v2.3)

loc_strings = {
    'ko': {
        'app_title': "💡 AI 데이터센터 통합 TCO & 사업 타당성 시뮬레이터 (v2.3)",
        # ... (기존 텍스트 동일) ...
        'section_3_header': "3. 사업 목표 설정",
        'target_irr_label': "목표 내부수익률 (IRR, %)",
        'viability_header': "사업 타당성 분석 (목표 IRR 달성 기준)",
        'annual_revenue_label': "필요 연간 매출",
        'token_price_label': "필요 서비스 단가 (백만 토큰 당)",
        'user_fee_label': "필요 사용자당 월 요금",
        # --- Narrative Generation Strings ---
        'narrative_expander_title': "결과 해설 및 전략적 제언",
        'narrative_title': "AI 전략 분석 리포트",
        'your_choice_title': "선택한 전략",
        # ... (기존 텍스트 동일) ...
        'viability_title': "사업 타당성 평가",
        'viability_text': "선택하신 인프라 투자({investment_per_mw} / MW)를 정당화하고 목표 IRR {target_irr}%를 달성하기 위해서는, 연간 약 **${annual_revenue:,.0f}**의 매출이 필요합니다. 이는 서비스 단가로는 **백만 토큰당 ${token_price:.4f}**, 혹은 **사용자당 월 ${user_fee:.2f}**의 요금 수준에 해당합니다.",
        'viability_recommendation': "이 가격 지표를 현재 시장의 경쟁 환경 및 가격 정책과 비교하여, 당신의 비즈니스 모델이 현실적으로 생존 가능한지, 혹은 가격 경쟁력을 갖추기 위해 TCO를 더 절감해야 하는지 판단하는 핵심 기준으로 삼으십시오."
    },
    'en': {
        'app_title': "💡 AI DC Integrated TCO & Business Viability Simulator (v2.3)",
        # ... (기존 텍스트 동일) ...
        'section_3_header': "3. Business Goals",
        'target_irr_label': "Target IRR (%)",
        'viability_header': "Business Viability Analysis (to achieve Target IRR)",
        'annual_revenue_label': "Required Annual Revenue",
        'token_price_label': "Required Service Price (per 1M tokens)",
        'user_fee_label': "Required Monthly Fee per User",
        # --- Narrative Generation Strings ---
        'narrative_expander_title': "Interpretation & Strategic Recommendation",
        'narrative_title': "AI Strategy Analysis Report",
        'your_choice_title': "Your Chosen Strategy",
        # ... (기존 텍스트 동일) ...
        'viability_title': "Business Viability Assessment",
        'viability_text': "To justify your infrastructure investment of **{investment_per_mw} per MW** and achieve a **{target_irr}% Target IRR**, your business needs to generate approximately **${annual_revenue:,.0f} in annual revenue**. This translates to a service price point of **${token_price:.4f} per million tokens**, or a **monthly fee of ${user_fee:.2f} per user**.",
        'viability_recommendation': "Use this pricing benchmark as a critical standard to assess your business model's viability against the current competitive market landscape. It will help you determine if your pricing is realistic or if you need to further reduce TCO to gain a competitive edge."
    }
}
```python
# interpreter.py (v2.3)

def generate_narrative(user_inputs, user_summary, benchmark_df, t):
    """
    사용자의 선택과 결과 데이터를 바탕으로 동적인 해설을 생성합니다.
    """
    # --- 1. 입력 변수 추출 ---
    apply_mm = user_inputs['apply_mirrormind']
    hw_ratio = user_inputs['high_perf_hw_ratio']
    target_irr = user_inputs['econ_assumptions']['target_irr'] * 100
    user_investment_per_mw = user_summary.get('investment_per_mw', 0)
    viability = user_summary.get('viability', {})
    
    # ... (기존 2, 3, 4 단계는 동일) ...
    hw_strategy = t('hw_strategy_high') if hw_ratio > 80 else t('hw_strategy_low') if hw_ratio < 20 else t('hw_strategy_hybrid')
    
    narrative = f"### {t('narrative_title')}\n\n"
    narrative += f"**{t('your_choice_title')}**\n"
    narrative += f"👉 {t('your_choice_text').format(apply_mm_text=t('applied') if apply_mm else t('not_applied'), hw_strategy=hw_strategy, investment_per_mw=f'${user_investment_per_mw:,.2f} M')}\n\n"

    narrative += f"**{t('key_driver_title')}**\n"
    if apply_mm:
        narrative += f"✅ **{t('driver_mm_on_title')}** {t('driver_mm_on_text')}\n"
        option_3_cost_str = benchmark_df[benchmark_df[t('strategy_col_1')] == t('option_3_name')][t('strategy_col_3')].iloc[0]
        narrative += f"   - {t('driver_mm_on_subtext').format(option_3_cost=option_3_cost_str)}\n\n"
    else:
        narrative += f"⚠️ **{t('driver_mm_off_title')}** {t('driver_mm_off_text')}\n"
        option_1_cost_str = benchmark_df[benchmark_df[t('strategy_col_1')] == t('option_1_name')][t('strategy_col_3')].iloc[0]
        narrative += f"   - {t('driver_mm_off_subtext').format(option_1_cost=option_1_cost_str)}\n\n"

    # --- 5. 사업 타당성 평가 추가 ---
    narrative += f"**{t('viability_title')}**\n"
    narrative += f"📈 {t('viability_text').format(investment_per_mw=f'${user_investment_per_mw:,.2f} M', target_irr=target_irr, annual_revenue=viability.get('required_annual_revenue', 0), token_price=viability.get('price_per_million_tokens', 0), user_fee=viability.get('monthly_fee_per_user', 0))}\n\n"


    # --- 6. 전략적 제언 ---
    narrative += f"**{t('recommendation_title')}**\n"
    if apply_mm:
        if hw_ratio == 100:
            narrative += f"👍 **{t('rec_mm_high_title')}** {t('rec_mm_high_text')}\n"
        elif hw_ratio == 0:
            narrative += f"💡 **{t('rec_mm_low_title')}** {t('rec_mm_low_text')}\n"
        else:
            narrative += f"🎯 **{t('rec_mm_hybrid_title')}** {t('rec_mm_hybrid_text')}\n"
    else:
        narrative += f"🔥 **{t('rec_no_mm_title')}** {t('rec_no_mm_text')}\n"
        
    narrative += f"   - {t('viability_recommendation')}\n"

    return narrative
