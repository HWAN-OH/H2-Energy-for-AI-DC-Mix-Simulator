{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/blob/main/interpreter.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# interpreter.py\n",
        "# 시뮬레이션 결과를 분석하고, 서술형 해설과 전략적 제언을 생성합니다.\n",
        "\n",
        "def generate_narrative(user_inputs, user_summary, benchmark_df, t):\n",
        "    \"\"\"\n",
        "    사용자의 선택과 결과 데이터를 바탕으로 동적인 해설을 생성합니다.\n",
        "\n",
        "    Args:\n",
        "        user_inputs (dict): 사용자가 사이드바에서 선택한 모든 입력값.\n",
        "        user_summary (dict): 사용자의 시나리오에 대한 계산 결과 요약.\n",
        "        benchmark_df (pd.DataFrame): 4가지 핵심 전략에 대한 벤치마크 데이터.\n",
        "        t (function): 현재 선택된 언어에 맞는 문자열을 반환하는 함수.\n",
        "\n",
        "    Returns:\n",
        "        str: Markdown 형식의 동적 분석 리포트.\n",
        "    \"\"\"\n",
        "    # --- 1. 입력 변수 추출 ---\n",
        "    apply_mm = user_inputs.get('apply_mirrormind', False)\n",
        "    hw_ratio = user_inputs.get('high_perf_hw_ratio', 100)\n",
        "    target_irr = user_inputs.get('econ_assumptions', {}).get('target_irr', 0.08) * 100\n",
        "    user_investment_per_mw = user_summary.get('investment_per_mw', 0)\n",
        "    viability = user_summary.get('viability', {})\n",
        "\n",
        "    # --- 2. 사용자 전략 정의 ---\n",
        "    if hw_ratio > 80:\n",
        "        hw_strategy = t('hw_strategy_high')\n",
        "    elif hw_ratio < 20:\n",
        "        hw_strategy = t('hw_strategy_low')\n",
        "    else:\n",
        "        hw_strategy = t('hw_strategy_hybrid')\n",
        "\n",
        "    # --- 3. 리포트 본문 생성 시작 ---\n",
        "    narrative = f\"### {t('narrative_title')}\\n\\n\"\n",
        "\n",
        "    # --- 3.1. 선택 전략 요약 ---\n",
        "    narrative += f\"**{t('your_choice_title')}**\\n\"\n",
        "    narrative += f\"👉 {t('your_choice_text').format(apply_mm_text=t('applied') if apply_mm else t('not_applied'), hw_strategy=hw_strategy, investment_per_mw=f'${user_investment_per_mw:,.2f} M')}\\n\\n\"\n",
        "\n",
        "    # --- 3.2. 핵심 동인 분석 ---\n",
        "    narrative += f\"**{t('key_driver_title')}**\\n\"\n",
        "    if apply_mm:\n",
        "        narrative += f\"✅ **{t('driver_mm_on_title')}** {t('driver_mm_on_text')}\\n\"\n",
        "        try:\n",
        "            option_3_cost_str = benchmark_df[benchmark_df[t('strategy_col_1')] == t('option_3_name')][t('strategy_col_3')].iloc[0]\n",
        "            narrative += f\"   - {t('driver_mm_on_subtext').format(option_3_cost=option_3_cost_str)}\\n\\n\"\n",
        "        except (IndexError, KeyError):\n",
        "            pass # 벤치마크 데이터가 없는 경우를 대비\n",
        "    else:\n",
        "        narrative += f\"⚠️ **{t('driver_mm_off_title')}** {t('driver_mm_off_text')}\\n\"\n",
        "        try:\n",
        "            option_1_cost_str = benchmark_df[benchmark_df[t('strategy_col_1')] == t('option_1_name')][t('strategy_col_3')].iloc[0]\n",
        "            narrative += f\"   - {t('driver_mm_off_subtext').format(option_1_cost=option_1_cost_str)}\\n\\n\"\n",
        "        except (IndexError, KeyError):\n",
        "            pass\n",
        "\n",
        "    # --- 3.3. 사업 타당성 평가 ---\n",
        "    narrative += f\"**{t('viability_title')}**\\n\"\n",
        "    narrative += f\"📈 {t('viability_text').format(investment_per_mw=f'${user_investment_per_mw:,.2f} M', target_irr=target_irr, annual_revenue=viability.get('required_annual_revenue', 0), token_price=viability.get('price_per_million_tokens', 0), user_fee=viability.get('monthly_fee_per_user', 0))}\\n\\n\"\n",
        "\n",
        "    # --- 3.4. 전략적 제언 ---\n",
        "    narrative += f\"**{t('recommendation_title')}**\\n\"\n",
        "    if apply_mm:\n",
        "        if hw_ratio == 100:\n",
        "            narrative += f\"👍 **{t('rec_mm_high_title')}** {t('rec_mm_high_text')}\\n\"\n",
        "        elif hw_ratio == 0:\n",
        "            narrative += f\"💡 **{t('rec_mm_low_title')}** {t('rec_mm_low_text')}\\n\"\n",
        "        else:\n",
        "            narrative += f\"🎯 **{t('rec_mm_hybrid_title')}** {t('rec_mm_hybrid_text')}\\n\"\n",
        "    else:\n",
        "        narrative += f\"🔥 **{t('rec_no_mm_title')}** {t('rec_no_mm_text')}\\n\"\n",
        "\n",
        "    narrative += f\"   - {t('viability_recommendation')}\\n\"\n",
        "\n",
        "    return narrative"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "id": "Uhf6VD5LY7yU"
      }
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}