# AI Datacenter Business Simulator

A comprehensive decision-support tool designed to analyze the realistic Profit & Loss (P&L) and payback period of AI services, helping you formulate an optimal business strategy.

---

## AI 데이터센터 사업성 시뮬레이터

AI 서비스의 현실적인 손익(P&L)과 투자 회수 기간을 분석하여, 최적의 비즈니스 전략을 수립할 수 있도록 돕는 종합 의사결정 지원 도구입니다.

---

[**>>> Click to Launch Live App / 라이브 앱 실행하기**](https://h2-energy-for-ai-dc-mix-simulator-lokmn9dwmkrbtmp7ovd3pn.streamlit.app/)

![Simulator's Final UI](https://github.com/HWAN-OH/H2-Energy-for-AI-DC-Mix-Simulator/blob/b3be6fc9d4a7b25f32a46099c36543946a7a9104/paper/AI%20DC%20%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7.png)

## Overview

The success of an AI datacenter business depends on the delicate balance of complex variables: hardware, power, architecture, and pricing. This simulator is designed to analyze these key strategic elements within an integrated financial model, helping you find answers to the essential question: **'How can we actually make a profit?'**

Moving beyond the limitations of the 'Scale-up' strategy, which relies solely on increasing LLM model size, this tool quantitatively analyzes the business impact of an **'Intelligent Architecture'** that efficiently controls the LLM. Based on this analysis, it proposes a realistic payback period and an optimal pricing strategy.

---

## 개요

AI 데이터센터 사업의 성공은 하드웨어, 전력, 아키텍처, 그리고 요금제라는 복잡한 변수들의 균형에 달려있습니다. 이 시뮬레이터는 이러한 핵심 전략 요소들을 통합된 재무 모델 안에서 분석하여, 단순한 비용 계산을 넘어 **'어떻게 해야 돈을 벌 수 있는가?'** 라는 본질적인 질문에 대한 답을 찾을 수 있도록 설계되었습니다.

특히, LLM 모델의 크기에만 의존하는 'Scale-up' 전략의 한계를 넘어, LLM을 효율적으로 제어하는 **'지능형 아키텍처(Intelligent Architecture)'**가 사업성에 미치는 영향을 정량적으로 분석하고, 이를 바탕으로 현실적인 투자 회수 기간과 최적의 가격 정책까지 제안합니다.

## Key Features

1.  **Integrated Business Modeling:** Calculates the annual P&L and the crucial **Operating Cash Flow** by incorporating everything from initial investment (CAPEX) like datacenter construction and hardware procurement, to operating expenses (OPEX) such as power and maintenance, and even depreciation.
2.  **Strategic Choice Analysis:** Instantly see how changes in key strategic variables impact business viability.
    * **Hardware Portfolio:** The budget allocation strategy between high-performance and standard GPUs.
    * **Power Source:** Cost structure analysis between the conventional grid and renewable energy.
    * **Intelligent Architecture:** Application of a superior architecture that achieves higher efficiency with the same hardware.
3.  **Realistic Payback Period Analysis:** Calculates the actual payback period based on **real cash flow**, which includes depreciation, rather than just accounting profit.
4.  **'What-If' Pricing Simulation:** Simulates how opportunity cost and final profit change when a specific monthly fixed-fee plan is applied, compared to usage-based revenue.
5.  **Optimal Pricing Recommendation:** The system reverse-calculates and proposes the optimal monthly fees required to achieve the financial target of a **'5-year investment payback'** under all chosen strategies.

---

## 핵심 기능

1.  **통합 비즈니스 모델링:** 데이터센터 건설, 하드웨어 구매 등 초기 투자(CAPEX)부터 전력, 유지보수 등 운영비(OPEX), 그리고 감가상각비까지 모두 반영하여 연간 손익(P&L)과 핵심적인 **영업 현금흐름(Operating Cash Flow)**을 계산합니다.
2.  **전략적 선택 분석:** 다음과 같은 핵심 전략 변수들을 직접 조절하며 사업성의 변화를 즉시 확인할 수 있습니다.
    * **하드웨어 포트폴리오:** 고성능 GPU와 표준 GPU의 예산 분배 전략
    * **전력 공급 방식:** 일반 전력망과 재생에너지의 비용 구조 차이 분석
    * **지능형 아키텍처:** 동일 하드웨어에서 더 높은 효율을 내는 상위 아키텍처 적용 여부
3.  **현실적인 투자 회수 기간 분석:** 회계적 이익이 아닌, 감가상각비가 반영된 **실제 현금흐름**을 기반으로 현재 전략 하에서의 현실적인 투자 회수 기간을 계산합니다.
4.  **'What-If' 요금제 시뮬레이션:** 특정 월간 고정 요금제를 설정했을 경우, 사용량 기반 매출 대비 기회비용과 최종 손익이 어떻게 변하는지 시뮬레이션합니다.
5.  **최적 요금제 제안:** 설정된 모든 전략 하에서 **'5년 내 투자금 회수'**라는 재무 목표를 달성하기 위해 필요한 최적의 월간 요금제를 시스템이 역으로 계산하여 제안합니다.

---

## Project Philosophy

This tool was developed by **[Oh Sunghwan](https://www.linkedin.com/in/shoh1224/)**, a professional with deep expertise across the energy, manufacturing, and technology sectors. It reflects a core belief: the most pressing challenges of our time can only be solved by bridging the gap between deep industry knowledge and data-driven, systems-level thinking.

---

## 프로젝트 철학

이 도구는 에너지, 제조, 기술 산업 전반에 걸친 깊은 전문성을 보유한 **[오승환 (Oh Sunghwan)](https://www.linkedin.com/in/shoh1224/)**에 의해 개발되었습니다. 이는 우리 시대의 가장 시급한 문제들이, 깊이 있는 산업 지식과 데이터 기반의 시스템적 사고 사이의 간극을 메울 때에만 해결될 수 있다는 핵심 신념을 반영합니다.

---

## License

This project is licensed under the MIT License. Copyright (c) 2025, Oh Sunghwan.

---

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. Copyright (c) 2025, Oh Sunghwan.
