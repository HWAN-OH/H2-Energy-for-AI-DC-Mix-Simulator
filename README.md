# AI Data Center Energy Strategy Simulator

A strategic decision-making tool designed to analyze and optimize the 5-year Total Cost of Ownership (TCO) for AI data center energy portfolios. This simulator empowers business leaders and investors to design their optimal energy mix and navigate the complex economic and environmental variables of the future.

![Simulator Screenshot](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/assets/174906093/d385f096-7c39-4d69-a8c4-e40e2b957648)


## Overview

The era of AI demands unprecedented levels of energy, making energy strategy a critical factor for the success and sustainability of any data center operation. This simulator moves beyond simple LCOE calculations to provide a comprehensive, 5-year TCO analysis, allowing users to model complex scenarios and make data-driven decisions.

This tool was born from a real-world need to answer the most critical question for data center operators: **"What is the most economically viable and sustainable energy strategy for my facility over the next five years?"**

## Key Features

- **5-Year TCO Analysis:** Calculates the full Total Cost of Ownership, including initial CAPEX, ongoing OPEX, asset replacement costs (e.g., fuel cell stacks), and future carbon taxes.
- **Dynamic Scenario Design:** Interactively design your own energy portfolio by adjusting the mix of Grid power, Solar, Wind, and Hydrogen Fuel Cells (SOFC).
- **Economic Assumption Modeling:** Factor in real-world economic variables like discount rates, annual price escalations for grid power and fuel, and potential carbon tax scenarios.
- **Present Value (PV) Calculation:** All future costs are discounted to their present value, enabling a true "apples-to-apples" comparison of long-term investments.
- **Intuitive Visualization:** Key metrics (TCO, LCOE, CAPEX) and annual cost trends are visualized through an interactive dashboard for clear, immediate insights.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator.git](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator.git)
    cd H2-Energy-for-AI-DC-Mix-Simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare your data (Optional):**
    - Modify `demand_profile.csv` with your own 5-year forecast for energy demand (MWh) and peak load (MW).
    - Adjust the base assumptions for technology costs and performance in `config.yml`.

4.  **Run the simulator:**
    ```bash
    streamlit run app.py
    ```

5.  **Configure & Analyze:**
    - Use the sidebar to design your energy mix and set economic assumptions.
    - Click "Run Analysis" to view the comprehensive results on the main dashboard.

## Core Logic & Simulation Scale

The simulation engine (`calculator.py`) performs a year-by-year analysis based on the user's scenario. The total required capacity of the power sources is determined by the `peak_demand_mw` specified in the `demand_profile.csv` for each year.

**The provided example `demand_profile.csv` simulates a data center starting with an initial peak load of approximately 8.5 MW, which grows over the 5-year period.** Users can adapt the simulation to any scale by modifying this CSV file to reflect their specific project's load profile.

1.  **Annual CAPEX Calculation:** Initial investments are calculated in Year 1 based on the required capacity to meet peak demand. Mid-life asset replacement costs (like SOFC stack replacements) are factored in at the specified year.
2.  **Annual OPEX Calculation:** Operational costs are calculated annually, including variable costs (grid power, fuel) subject to escalation rates, and fixed costs (O&M) based on a percentage of CAPEX.
3.  **Present Value (PV) Analysis:** All annual costs (both CAPEX and OPEX) are discounted to their present value using the user-defined discount rate.
4.  **TCO & LCOE Calculation:** The sum of all discounted costs over the 5-year period yields the final TCO. The average LCOE is then derived from this total cost and the total energy demand.

## Project Philosophy

This tool was developed by **[OH SEONG-HWAN](https://www.linkedin.com/in/shoh1224/)**, a leader with deep expertise across the energy, manufacturing, and technology sectors. It reflects a core belief: the most pressing challenges of our time, from energy transition to AI infrastructure, can only be solved by bridging the gap between deep industry knowledge and data-driven, systems-level thinking.

This simulator is an open invitation to all builders, operators, and visionaries to join in shaping a more sustainable and intelligent future.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
