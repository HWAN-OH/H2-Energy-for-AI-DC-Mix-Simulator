# AI Data Center TCO & Strategy Simulator (v2.0)

A comprehensive strategic decision-making tool designed to analyze and optimize the 5-year Total Cost of Ownership (TCO) for AI data centers. This simulator moves beyond simple energy analysis to provide a fully integrated model that includes **IT Hardware Strategy**, **Architectural Efficiency**, **Physical Construction Costs**, and **Energy Portfolio Management**.

![Simulator Screenshot](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/assets/174906093/d385f096-7c39-4d69-a8c4-e40e2b957648) <!-- Placeholder image -->

## Overview

The economics of AI data centers are complex. A winning strategy requires balancing the costs of IT hardware, the efficiency of the software architecture, the physical construction of the facility, and the long-term cost of energy. This simulator provides a unified framework to analyze these trade-offs and identify the optimal investment path.

This upgraded version (v2.0) directly incorporates the "MirrorMind" architectural efficiency concept, allowing leaders to quantify the economic impact of investing in a smarter architecture versus simply buying more or cheaper hardware.

## Key Features

- **Integrated TCO Modeling:** Calculates a comprehensive 5-year TCO, including DC construction, IT hardware, energy, maintenance, and depreciation tax shield effects.
- **Strategic Choice Analysis:** Directly compare different strategic postures by toggling key options:
    - **MirrorMind Architecture:** Quantify the value of architectural efficiency.
    - **Hardware Portfolio Mix:** Find the optimal balance between high-performance and low-cost hardware.
- **Realistic Cost Assumptions:** The model is built on verifiable industry data for construction costs, hardware pricing, and energy rates.
- **Dynamic Scenario Simulation:** Interactively adjust your core strategic choices and immediately see the impact on your bottom line, represented as the final `Investment per MW`.

## How to Use

1.  **Clone the repository and install dependencies:**
    ```bash
    git clone [https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator.git](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator.git)
    cd H2-Energy-for-AI-DC-Mix-Simulator
    pip install -r requirements.txt
    ```

2.  **Run the simulator:**
    ```bash
    streamlit run app.py
    ```

3.  **Configure Your Scenario in the Sidebar:**
    - **Core Strategic Choices:** This is the heart of the simulation.
        - **Toggle `MirrorMind 아키텍처 적용`:** Decide whether to apply the architectural efficiency model. This is the most impactful choice.
        - **Adjust `고성능 하드웨어(H100) 비중 (%)`:** Define your hardware strategy based on your specific workload needs.
    - **Market & Economic Assumptions:** Select your target region and set the discount rate.

4.  **Run and Analyze:**
    - Click the **`Run TCO Analysis`** button.
    - Review the key metrics: **Final Integrated TCO** and **Final Investment per MW**.
    - Use the pie chart to understand the cost composition of your chosen strategy.
    - Experiment with different configurations to find your optimal path.

## Project Philosophy

This tool was developed by **[OH SEONG-HWAN](https://www.linkedin.com/in/shoh1224/)**, a leader with deep expertise across the energy, manufacturing, and technology sectors. It reflects a core belief: the most pressing challenges of our time can only be solved by bridging the gap between deep industry knowledge and data-driven, systems-level thinking.

## License

This project is licensed under the MIT License. Copyright (c) 2025, OH SUNG-HWAN.
