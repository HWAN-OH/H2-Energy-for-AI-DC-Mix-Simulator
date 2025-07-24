{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/blob/main/what_if_calculator.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# what_if_calculator.py\n",
        "# This module is dedicated to the 'What-If' analysis for the fixed-fee pricing scenario.\n",
        "\n",
        "def analyze_fixed_fee_scenario(segment_narratives, standard_fee, premium_fee):\n",
        "    \"\"\"\n",
        "    Calculates the profit and opportunity cost for a fixed-fee scenario.\n",
        "    This calculation is completely independent of the main usage-based model.\n",
        "\n",
        "    Args:\n",
        "        segment_narratives (list): A list of dictionaries containing the pre-calculated\n",
        "                                   usage-based metrics for each user segment.\n",
        "        standard_fee (float): The user-defined monthly fee for the Standard tier.\n",
        "        premium_fee (float): The user-defined monthly fee for the Premium tier.\n",
        "\n",
        "    Returns:\n",
        "        list: The updated list of segment narrative dictionaries, with new keys\n",
        "              for the fixed-fee analysis.\n",
        "    \"\"\"\n",
        "    what_if_results = []\n",
        "    for segment in segment_narratives:\n",
        "        # Create a copy to avoid modifying the original data\n",
        "        updated_segment = segment.copy()\n",
        "\n",
        "        fixed_fee = 0\n",
        "        if segment['tier_name_key'] == 'tier_standard':\n",
        "            fixed_fee = standard_fee\n",
        "        elif segment['tier_name_key'] == 'tier_premium':\n",
        "            fixed_fee = premium_fee\n",
        "\n",
        "        # The core cost per user is already calculated based on the true usage potential.\n",
        "        cost_per_user = segment['cost_per_user']\n",
        "        usage_based_revenue_per_user = segment['revenue_per_user']\n",
        "\n",
        "        # Calculate the what-if metrics\n",
        "        new_profit_per_user = fixed_fee - cost_per_user\n",
        "        opportunity_cost = usage_based_revenue_per_user - fixed_fee\n",
        "\n",
        "        updated_segment['fixed_fee'] = fixed_fee\n",
        "        updated_segment['new_profit_per_user'] = new_profit_per_user\n",
        "        updated_segment['opportunity_cost'] = opportunity_cost\n",
        "\n",
        "        what_if_results.append(updated_segment)\n",
        "\n",
        "    return what_if_results"
      ],
      "outputs": [],
      "execution_count": null,
      "metadata": {
        "id": "x4TXAdnFmhSs"
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