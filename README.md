# Watershed Project: Malshiras Taluka Groundwater & XLRM Management Analysis (CE766)

Empirical seasonal depth-to-water (DTW) baseline analysis and **XLRM (Uncertainties, Levers, Relationships, Measures)** water-balance simulation for **Malshiras Taluka (Solapur District, Maharashtra, India)** over **2015–2019**.

---

## 📁 Repository Structure

| File / Folder | Description |
| :--- | :--- |
| [`final_submission/`](final_submission/) | **Final Project Submission Package**: Contains individual Moodle visual files (`Figure_1_Baseline_Seasonal_DTW.png`, `Figure_2_XLRM_Management_Scenarios.png`), scenario summary table (`xlrm_scenario_summary_2015_2019.csv`), and copy-paste submission text (`CE766_Final_Submission_Copy_Paste_Guide.pdf` & `.txt`). |
| [`well_level_groundwater_2015_2019.csv`](well_level_groundwater_2015_2019.csv) | Seasonal well-level DTW observations (in m bgl) across 22 monitoring wells (14 SGWD/GSDA, 8 CGWB) transcribed from Table 02 of the GSDA Malshiras report. |
| [`annual_rainfall_2015_2019.csv`](annual_rainfall_2015_2019.csv) | Official annual rainfall records for Malshiras Taluka (2015–2019). |
| [`groundwater_preliminary_analysis.py`](groundwater_preliminary_analysis.py) | Preliminary baseline script computing seasonal means, valid well counts ($n$), and baseline Figure 1. |
| [`groundwater_final_xlrm_analysis.py`](groundwater_final_xlrm_analysis.py) | **Final XLRM analysis script** implementing the Water Table Fluctuation (WTF) aquifer water-balance model across policy levers ($L_0\text{–}L_3$) and specific yield uncertainties ($S_y \in [0.015, 0.025]$). |
| [`calculated_seasonal_summary.csv`](calculated_seasonal_summary.csv) | Baseline seasonal DTW means, valid sample counts, and observed seasonal rise ($\Delta h_{\text{obs}}$). |
| [`final_submission/xlrm_scenario_summary_2015_2019.csv`](final_submission/xlrm_scenario_summary_2015_2019.csv) | Complete XLRM simulation outputs across all policy levers and parameter uncertainty bounds (2015–2019). |

---

## 🚀 Reproducing the Analysis

```bash
# 1. Activate virtual environment (or create one with python3 -m venv .venv)
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run preliminary baseline analysis
python groundwater_preliminary_analysis.py

# 3. Run final XLRM scenario & uncertainty analysis (outputs to final_submission/)
python groundwater_final_xlrm_analysis.py
```

---

## 📊 Methodology Summary (XLRM Framework)

Grounded in the **Water Table Fluctuation (WTF) method** (Healy & Cook, 2002; CGWB GEC-2015):

```text
Mean_DTW(t, s) = (1 / n_t,s) * sum(DTW_i,t,s)
Delta_h_obs(t) = Mean_DTW_May(t) - Mean_DTW_OctNov(t)
Delta_S_obs(t) = Sy * Delta_h_obs(t) * 1000 = R_base(t) - D_base(t)
Delta_h_sim(t) = [ (1 + alpha_MAR) * R_base(t) - (1 - beta_dem) * D_base(t) ] / (1000 * Sy)
DTW_OctNov_sim(t) = Mean_DTW_May(t) - Delta_h_sim(t)
```

- **Uncertainties ($X$)**: Annual rainfall $P_t \in [215.29, 582.30]\text{ mm}$ and unconfined fractured basalt specific yield $S_y \in \{0.015, 0.020, 0.025\}$ (reference $S_y = 0.020$, gross recharge factor $f_r = 0.22$).
- **Policy Levers ($L$)**:
  - **$L_0$ (Baseline BAU)**: $\alpha_{\text{MAR}} = 0.00$, $\beta_{\text{dem}} = 0.00$
  - **$L_1$ (Supply-Side MAR)**: $\alpha_{\text{MAR}} = 0.20$ (+20% recharge via check dams/percolation tanks), $\beta_{\text{dem}} = 0.00$
  - **$L_2$ (Demand-Side Management)**: $\alpha_{\text{MAR}} = 0.00$, $\beta_{\text{dem}} = 0.25$ (-25% monsoon draft via drip irrigation & crop shift)
  - **$L_3$ (Integrated Management)**: $\alpha_{\text{MAR}} = 0.20$, $\beta_{\text{dem}} = 0.25$
- **Measures ($M$)**: Post-monsoon depth-to-water ($\text{DTW}_{\text{Oct/Nov, sim}}$, m bgl), net seasonal aquifer storage recovery ($\Delta S_{\text{sim}}$, mm), and 2018 dry-year stress resilience.

---

## 📚 Primary References & Data Sources

1. **Ground Water Surveys and Development Agency (GSDA), 2020** — *Atal Bhujal Yojana Hydrogeological Report: Malshiras Taluka, Solapur District*, Table 02 ([PDF Link](https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf)).
2. **Solapur District Administration, 2020** — *Official Taluka-wise Annual Rainfall Records* ([Portal Link](https://solapur.gov.in/en/rainfall/)).
3. **Healy, R. W., & Cook, P. G. (2002)** — *Using groundwater levels to estimate recharge*, Hydrogeology Journal, 10(1), 91–109; alongside **CGWB (2017)** *Ground Water Resource Estimation Committee (GEC-2015) Report*.
