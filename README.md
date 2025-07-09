# AI Data Center Energy Strategy Simulator

A strategic decision-making tool designed to analyze and optimize the 5-year Total Cost of Ownership (TCO) for AI data center energy portfolios. This simulator empowers business leaders and investors to design their optimal energy mix and navigate the complex economic and environmental variables of the future.

![Simulator Screenshot](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/assets/174906093/d385f096-7c39-4d69-a8c4-e40e2b957648)


## Overview

The era of AI demands unprecedented levels of energy, making energy strategy a critical factor for the success and sustainability of any data center operation. This simulator moves beyond simple LCOE calculations to provide a comprehensive, 5-year TCO analysis, allowing users to model complex scenarios and make data-driven decisions.

This tool was born from a real-world need to answer the most critical question for data center operators: **"What is the most economically viable and sustainable energy strategy for my facility over the next five years?"**

## Key Features

- **5-Year TCO Analysis:** Calculates the full Total Cost of Ownership, including initial CAPEX, ongoing OPEX, asset replacement costs, and future carbon taxes.
- **Dynamic Scenario Design:** Interactively design your own energy portfolio by adjusting the mix of Grid power, Solar, Wind, and Hydrogen/Natural Gas Fuel Cells.
- **Global Market Scenarios:** Analyze project feasibility across different regions (e.g., USA, South Korea, EU) with realistic, market-specific energy pricing.
- **Financial Modeling:** Incorporates key financial metrics like Discount Rate and Present Value (PV) for a true "apples-to-apples" comparison of long-term investments.

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

## Key Assumptions & Data Sources

The credibility of this simulation rests on the transparency of its underlying data. The default values in `config.yml` are not arbitrary; they are representative figures derived from a survey of recent industry reports, market data, and established energy benchmarks.

-   **Market Scenarios (Grid & Gas Prices):** The regional electricity and natural gas prices are based on publicly available data and reports from sources such as the **U.S. Energy Information Administration (EIA)**, **Eurostat**, and analysis of the Korean industrial market. They are intended to reflect the higher, all-in costs for new, large-scale data center customers, which include infrastructure and grid upgrade costs, not just simple retail rates.

-   **Technology Costs (CAPEX/OPEX):** The capital and operational expenditures for technologies like Solar, Wind, and SOFC are based on industry benchmarks from leading energy analysis institutions like **Lazard's LCOE Analysis**, **NREL**, and various market intelligence reports.

-   **No Subsidies Assumption:** **Crucially, this model does NOT include any government subsidies, tax credits (like the U.S. IRA), or other incentives.** It is a pure, unsubsidized cost-based analysis, providing a conservative baseline for economic feasibility.

## Core Logic & Simulation Scale

The simulation engine (`calculator.py`) performs a year-by-year analysis based on the user's scenario. The total required capacity of the power sources is determined by the `peak_demand_mw` specified in the `demand_profile.csv` for each year.

**The provided example `demand_profile.csv` simulates a data center scaling from an initial peak load of 40 MW to a final load of 100 MW over 5 years.** Users can adapt the simulation to any scale by modifying this CSV file.

## Project Philosophy

This tool was developed by **[OH SEONG-HWAN](https://www.linkedin.com/in/shoh1224/)**, a leader with deep expertise across the energy, manufacturing, and technology sectors. It reflects a core belief: the most pressing challenges of our time, from energy transition to AI infrastructure, can only be solved by bridging the gap between deep industry knowledge and data-driven, systems-level thinking.

This simulator is an open invitation to all builders, operators, and visionaries to join in shaping a more sustainable and intelligent future.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
