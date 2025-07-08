
# H2-Energy-Mix-Simulator

This Streamlit app simulates a 3-year transition in energy sourcing for critical facilities, starting with NG-based fuel cells and moving towards renewables and hydrogen fuel cells (SOFCs).

## Features

- Simulate annual energy cost and carbon emissions
- Compare two phases:
  - Initial Phase: NG fuel cell + Grid
  - Transition Phase: Solar + Wind + H2 SOFC + Diesel Backup
- Adjustable energy mix via sidebar sliders

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
