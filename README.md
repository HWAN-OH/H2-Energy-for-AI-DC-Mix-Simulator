<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Datacenter Business Simulator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-top: 1em;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 0.5em;
        }
        strong {
            color: #24292e;
        }
        .live-app-link {
            display: inline-block;
            padding: 12px 20px;
            background-color: #2ea44f;
            color: white;
            font-weight: bold;
            text-align: center;
            border-radius: 6px;
            margin: 1em 0;
        }
        .live-app-link:hover {
            background-color: #2c974b;
            text-decoration: none;
        }
    </style>
</head>
<body>

    <h1>AI Datacenter Business Simulator</h1>
    <p>A comprehensive decision-support tool designed to analyze the realistic Profit & Loss (P&L) and payback period of AI services, helping you formulate an optimal business strategy.</p>

    <hr>

    <h2>AI 데이터센터 사업성 시뮬레이터</h2>
    <p>AI 서비스의 현실적인 손익(P&L)과 투자 회수 기간을 분석하여, 최적의 비즈니스 전략을 수립할 수 있도록 돕는 종합 의사결정 지원 도구입니다.</p>
    
    <hr>

    <a href="https://h2-energy-for-ai-dc-mix-simulator-lokmn9dwmkrbtmp7ovd3pn.streamlit.app/" class="live-app-link"><strong>&gt;&gt;&gt; Click to Launch Live App / 라이브 앱 실행하기</strong></a>

    <img src="https://i.imgur.com/GZqB3sL.png" alt="Simulator's Final UI">

    <h2>Overview</h2>
    <p>The success of an AI datacenter business depends on the delicate balance of complex variables: hardware, power, architecture, and pricing. This simulator is designed to analyze these key strategic elements within an integrated financial model, helping you find answers to the essential question: <strong>'How can we actually make a profit?'</strong></p>
    <p>Moving beyond the limitations of the 'Scale-up' strategy, which relies solely on increasing LLM model size, this tool quantitatively analyzes the business impact of an <strong>'Intelligent Architecture'</strong> that efficiently controls the LLM. Based on this analysis, it proposes a realistic payback period and an optimal pricing strategy.</p>

    <h2>개요</h2>
    <p>AI 데이터센터 사업의 성공은 하드웨어, 전력, 아키텍처, 그리고 요금제라는 복잡한 변수들의 균형에 달려있습니다. 이 시뮬레이터는 이러한 핵심 전략 요소들을 통합된 재무 모델 안에서 분석하여, 단순한 비용 계산을 넘어 <strong>'어떻게 해야 돈을 벌 수 있는가?'</strong> 라는 본질적인 질문에 대한 답을 찾을 수 있도록 설계되었습니다.</p>
    <p>특히, LLM 모델의 크기에만 의존하는 'Scale-up' 전략의 한계를 넘어, LLM을 효율적으로 제어하는 <strong>'지능형 아키텍처(Intelligent Architecture)'</strong>가 사업성에 미치는 영향을 정량적으로 분석하고, 이를 바탕으로 현실적인 투자 회수 기간과 최적의 가격 정책까지 제안합니다.</p>

    <h2>Key Features</h2>
    <ul>
        <li><strong>Integrated Business Modeling:</strong> Calculates the annual P&L and the crucial <strong>Operating Cash Flow</strong> by incorporating everything from initial investment (CAPEX) like datacenter construction and hardware procurement, to operating expenses (OPEX) such as power and maintenance, and even depreciation.</li>
        <li><strong>Strategic Choice Analysis:</strong> Instantly see how changes in key strategic variables impact business viability.
            <ul>
                <li><strong>Hardware Portfolio:</strong> The budget allocation strategy between high-performance and standard GPUs.</li>
                <li><strong>Power Source:</strong> Cost structure analysis between the conventional grid and renewable energy.</li>
                <li><strong>Intelligent Architecture:</strong> Application of a superior architecture that achieves higher efficiency with the same hardware.</li>
            </ul>
        </li>
        <li><strong>Realistic Payback Period Analysis:</strong> Calculates the actual payback period based on <strong>real cash flow</strong>, which includes depreciation, rather than just accounting profit.</li>
        <li><strong>'What-If' Pricing Simulation:</strong> Simulates how opportunity cost and final profit change when a specific monthly fixed-fee plan is applied, compared to usage-based revenue.</li>
        <li><strong>Optimal Pricing Recommendation:</strong> The system reverse-calculates and proposes the optimal monthly fees required to achieve the financial target of a <strong>'5-year investment payback'</strong> under all chosen strategies.</li>
    </ul>

    <h2>핵심 기능</h2>
    <ul>
        <li><strong>통합 비즈니스 모델링:</strong> 데이터센터 건설, 하드웨어 구매 등 초기 투자(CAPEX)부터 전력, 유지보수 등 운영비(OPEX), 그리고 감가상각비까지 모두 반영하여 연간 손익(P&L)과 핵심적인 <strong>영업 현금흐름(Operating Cash Flow)</strong>을 계산합니다.</li>
        <li><strong>전략적 선택 분석:</strong> 다음과 같은 핵심 전략 변수들을 직접 조절하며 사업성의 변화를 즉시 확인할 수 있습니다.
            <ul>
                <li><strong>하드웨어 포트폴리오:</strong> 고성능 GPU와 표준 GPU의 예산 분배 전략</li>
                <li><strong>전력 공급 방식:</strong> 일반 전력망과 재생에너지의 비용 구조 차이 분석</li>
                <li><strong>지능형 아키텍처:</strong> 동일 하드웨어에서 더 높은 효율을 내는 상위 아키텍처 적용 여부</li>
            </ul>
        </li>
        <li><strong>현실적인 투자 회수 기간 분석:</strong> 회계적 이익이 아닌, 감가상각비가 반영된 <strong>실제 현금흐름</strong>을 기반으로 현재 전략 하에서의 현실적인 투자 회수 기간을 계산합니다.</li>
        <li><strong>'What-If' 요금제 시뮬레이션:</strong> 특정 월간 고정 요금제를 설정했을 경우, 사용량 기반 매출 대비 기회비용과 최종 손익이 어떻게 변하는지 시뮬레이션합니다.</li>
        <li><strong>최적 요금제 제안:</strong> 설정된 모든 전략 하에서 <strong>'5년 내 투자금 회수'</strong>라는 재무 목표를 달성하기 위해 필요한 최적의 월간 요금제를 시스템이 역으로 계산하여 제안합니다.</li>
    </ul>

    <h2>How to Use</h2>
    <ol>
        <li>Navigate to the <a href="https://h2-energy-for-ai-dc-mix-simulator-lokmn9dwmkrbtmp7ovd3pn.streamlit.app/"><strong>Live App</strong></a>.</li>
        <li>In the <strong>sidebar</strong> on the left, configure key <strong>strategic variables</strong> such as datacenter size, hardware, power, and intelligent architecture.</li>
        <li>(Optional) In the <strong>'Pricing Strategy'</strong> section, enter hypothetical monthly fees for your 'What-if' analysis.</li>
        <li>Click the <strong>'Run Analysis'</strong> button.</li>
        <li>Review the <strong>4-step analysis report</strong> on the screen to derive strategic insights.</li>
    </ol>

    <h2>사용 방법</h2>
    <ol>
        <li><a href="https://h2-energy-for-ai-dc-mix-simulator-lokmn9dwmkrbtmp7ovd3pn.streamlit.app/"><strong>라이브 앱</strong></a>에 접속합니다.</li>
        <li>화면 왼쪽의 <strong>사이드바</strong>에서 데이터센터 규모, 하드웨어, 전력, 지능형 아키텍처 등 핵심 <strong>전략 변수</strong>들을 설정합니다.</li>
        <li>(선택 사항) <strong>'요금제 전략 설정'</strong> 섹션에서, 'What-if' 분석을 위한 가상의 월 요금을 입력합니다.</li>
        <li><strong>'분석 실행'</strong> 버튼을 클릭합니다.</li>
        <li>화면에 표시되는 <strong>4단계 분석 리포트</strong>를 통해 결과를 확인하고 전략적 인사이트를 도출합니다.</li>
    </ol>

    <h2>Report Structure</h2>
    <ul>
        <li><strong>Section 1: Core Business Potential & Cash Flow:</strong> Shows the annual P&L and actual cash flow based on the maximum efficiency (usage-based revenue) of the selected strategy.</li>
        <li><strong>Section 2: P&L Analysis by Customer Segment:</strong> Analyzes the monthly per-user revenue, cost, and profit to assess the health of the unit economics.</li>
        <li><strong>Section 3: 'What-If' Analysis:</strong> Analyzes the changes in profit and opportunity cost when the 'fixed-fee plan' entered in the sidebar is applied.</li>
        <li><strong>Section 4: Final Summary & Payback Analysis:</strong> Presents the realistic payback period for the current strategy and recommends an optimal pricing plan to achieve the '5-year payback' target.</li>
    </ul>

    <h2>분석 리포트 구조</h2>
    <ul>
        <li><strong>섹션 1: 핵심 사업 잠재력 및 현금흐름:</strong> 선택된 전략의 최대 효율(사용량 기반 매출)을 기준으로 한 연간 손익과 실제 현금흐름을 보여줍니다.</li>
        <li><strong>섹션 2: 고객 그룹별 손익 분석:</strong> 사업의 최소 단위인 '고객 한 명'을 기준으로, 월간 인당 매출, 원가, 이익을 분석하여 단위 경제(Unit Economics)의 건전성을 파악합니다.</li>
        <li><strong>섹션 3: 'What-If' 분석:</strong> 사이드바에서 입력한 '고정 요금제'를 적용했을 때의 손익 변화와 기회비용을 분석합니다.</li>
        <li><strong>섹션 4: 최종 요약 및 투자 회수 기간 분석:</strong> 현재 전략의 현실적인 투자 회수 기간을 제시하고, '5년 회수' 목표 달성을 위한 최적의 요금제를 제안합니다.</li>
    </ul>

    <h2>Project Philosophy</h2>
    <p>This tool was developed by <a href="https://www.linkedin.com/in/shoh1224/"><strong>Oh Sunghwan</strong></a>, a professional with deep expertise across the energy, manufacturing, and technology sectors. It reflects a core belief: the most pressing challenges of our time can only be solved by bridging the gap between deep industry knowledge and data-driven, systems-level thinking.</p>

    <h2>프로젝트 철학</h2>
    <p>이 도구는 에너지, 제조, 기술 산업 전반에 걸친 깊은 전문성을 보유한 <a href="https://www.linkedin.com/in/shoh1224/"><strong>오승환 (Oh Sunghwan)</strong></a>에 의해 개발되었습니다. 이는 우리 시대의 가장 시급한 문제들이, 깊이 있는 산업 지식과 데이터 기반의 시스템적 사고 사이의 간극을 메울 때에만 해결될 수 있다는 핵심 신념을 반영합니다.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. Copyright (c) 2025, Oh Sunghwan.</p>

    <h2>라이선스</h2>
    <p>이 프로젝트는 MIT 라이선스를 따릅니다. Copyright (c) 2025, Oh Sunghwan.</p>

</body>
</html>
