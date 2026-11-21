# Code & Analysis Package (`code_analysis/`) — Malshiras Taluka Groundwater & XLRM Water-Budget Study (2015–2019)

This folder contains the complete, self-contained datasets, Python analysis scripts, generated summary tables, and high-resolution figures for the **Malshiras Taluka (Solapur District, Maharashtra)** groundwater management study (`2015–2019`). The standalone final project report (with Figures 1 and 2 embedded inline) is located in the parent folder at [`../Final_Project_Report.pdf`](../Final_Project_Report.pdf).

---

## 1. Files Included in `code_analysis/`

| File | Type | Description |
| :--- | :---: | :--- |
| [`well_level_groundwater_2015_2019.csv`](well_level_groundwater_2015_2019.csv) | Input Data | Pre-monsoon (May) and post-monsoon (October/November) depth-to-water (m bgl) across 22 monitoring wells (14 SGWD/GSDA, 8 CGWB) from GSDA (2020) Table 02. |
| [`annual_rainfall_2015_2019.csv`](annual_rainfall_2015_2019.csv) | Input Data | Official Malshiras Taluka annual rainfall totals (mm/year) for 2015–2019 from Solapur District Administration records. |
| [`groundwater_preliminary_analysis.py`](groundwater_preliminary_analysis.py) | Python Script | Computes baseline seasonal mean DTW, valid well counts (`n`), observed seasonal water-table rise (`dh`), and baseline Figure 1. |
| [`groundwater_final_xlrm_analysis.py`](groundwater_final_xlrm_analysis.py) | Python Script | Implements the Water Table Fluctuation (WTF) seasonal water-budget model and XLRM policy scenario simulation across levers `L0–L3` and specific yield uncertainty `Sy in [0.015, 0.025]`. |
| [`calculated_seasonal_summary.csv`](calculated_seasonal_summary.csv) | Output Table | Generated baseline seasonal DTW means, valid sample counts, and seasonal water-table rise (`2015–2019`). |
| [`xlrm_scenario_summary_2015_2019.csv`](xlrm_scenario_summary_2015_2019.csv) | Output Table | Complete XLRM water-budget components (`R`, `D`, `dS`) and simulated post-monsoon DTW across all policy levers and `Sy` bounds. |
| [`Figure_1_Baseline_Seasonal_DTW.png`](Figure_1_Baseline_Seasonal_DTW.png) | Output Visual 1 | High-resolution (`220 DPI`) plot of observed May vs. October/November mean DTW (`2015–2019`) with valid well counts (`n`). |
| [`Figure_2_XLRM_Management_Scenarios.png`](Figure_2_XLRM_Management_Scenarios.png) | Output Visual 2 | High-resolution (`220 DPI`) two-panel figure showing (a) simulated post-monsoon DTW under `L0–L3` with `Sy` uncertainty band, and (b) net seasonal storage recovery `dS` (mm). |
| [`requirements.txt`](requirements.txt) | Config | Python dependencies required to run the scripts (`matplotlib>=3.9.0`). |

---

## 2. Architecture & Walkthrough of the Code

### A. Data Ingestion & Missing-Observation Handling
Both scripts use `read_csv(path)` and `number_or_none(value)` to parse `well_level_groundwater_2015_2019.csv` and `annual_rainfall_2015_2019.csv`:
- **Why blank cells are not converted to zero:** In government hydrogeological monitoring tables, missing cells occur when a well is temporarily unmonitored or inaccessible. Replacing a missing reading with `0` would represent a water level at `0 m below ground level` (ground-surface saturation/waterlogging), severely biasing the taluka mean.
- The code converts blank cells to `None` and filters them out per season, dynamically computing the valid well sample count `n` (`n = 19–20` in May; `n = 20–21` in October/November):
  ```text
  Mean DTW(year, season) = sum of valid well depth-to-water readings / n
  Seasonal Rise dh = Mean DTW May - Mean DTW OctNov
  ```

### B. Seasonal Water Budget Decomposition (`groundwater_final_xlrm_analysis.py`)
To link observed well depth fluctuations directly to watershed intervention design, `compute_baseline_and_xlrm()` applies the **Water Table Fluctuation (WTF) method** (Healy & Cook, 2002; CGWB GEC-2015):
1. **Net Seasonal Storage Change (`dS_obs_mm`)**:
   Converts the observed seasonal rise `dh` (in metres) into volumetric water depth (in mm of water equivalent) using reference specific yield `Sy = 0.020` (2.0% effective porosity for fractured Deccan basalt):
   ```text
   Baseline Storage Change dS = Sy * dh * 1000 = R - D
   ```
2. **Gross Monsoon Recharge (`R_base_mm`) & Implied Seasonal Draft (`D_base_mm`)**:
   Using the reference monsoon recharge factor `fr = 0.22` (capturing direct rainfall infiltration plus surface/canal seepage across the command area):
   ```text
   R = fr * P
   D = R - dS
   ```
   This decomposition explains the **2018 anomaly**: in 2018 (`P = 332.50 mm`), gross monsoon recharge was `73.15 mm`, yet net storage rose by only `3.00 mm` (`dh = 0.15 m`), demonstrating that seasonal pumping draft surged to `D = 70.15 mm` (consuming 96% of monsoon recharge during mid-season dry spells).

### C. XLRM Scenario Simulation (`L0` to `L3`) & Parameter Sensitivity (`Sy`)
The script evaluates four management levers defined by supply-side recharge augmentation (`a`) and demand-side seasonal draft reduction (`b`):
- **`L0` (Baseline):** `a = 0.00`, `b = 0.00` (historical conditions)
- **`L1` (Supply-Side MAR):** `a = 0.20`, `b = 0.00` (+20% monsoon recharge via check dams, nala bunds, and percolation tanks)
- **`L2` (Demand-Side Management):** `a = 0.00`, `b = 0.25` (-25% seasonal draft via drip irrigation and shifting sugarcane to low-water crops)
- **`L3` (Integrated Management):** `a = 0.20`, `b = 0.25` (combining both +20% MAR and -25% draft reduction)

For each policy lever and each specific yield value `Sy in {0.015, 0.020, 0.025}`, the script calculates:
```text
Simulated Storage Recovery dSsim = (1 + a) * R - (1 - b) * D
Simulated Rise dhsim = dSsim / (1000 * Sy)
Simulated OctNov DTW = Mean DTW May - dhsim
```

---

## 3. Summary of Quantitative Outputs

| Year | Rainfall `P` (mm) | May DTW (m bgl) | Observed Oct/Nov DTW `L0` (m bgl) | Observed Rise `dh` (m) | Gross Recharge `R` (mm) | Implied Draft `D` (mm) | `L1` (+20% MAR) Post-DTW (m) | `L2` (-25% Draft) Post-DTW (m) | `L3` (Integrated) Post-DTW (m) | `L3` Storage Gain `dS` (mm) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2015** | 215.29 | 6.46 | 5.14 | 1.32 | 47.36 | 20.96 | 4.67 | 4.88 | **4.40** | 41.1 |
| **2016** | 436.70 | 7.17 | 3.04 | 4.13 | 96.07 | 13.47 | 2.08 | 2.87 | **1.91** | 105.2 |
| **2017** | 530.52 | 6.86 | 2.78 | 4.08 | 116.71 | 35.11 | 1.61 | 2.34 | **1.17** | 113.7 |
| **2018** | 332.50 | 6.02 | 5.87 | 0.15 | 73.15 | **70.15** | 5.14 | **4.99** | **4.26** | 35.2 |
| **2019** | 582.30 | 8.07 | 3.63 | 4.44 | 128.11 | 39.31 | 2.35 | 3.14 | **1.86** | 124.2 |
| **Mean** | **419.46** | **6.92** | **4.09** | **2.82** | **92.28** | **35.80** | **3.17** | **3.64** | **2.72** | **83.9** |

---

## 4. Reproducing the Outputs

From inside this `code_analysis/` directory (or from the repository root):

```bash
pip install -r requirements.txt
python groundwater_preliminary_analysis.py
python groundwater_final_xlrm_analysis.py
```
