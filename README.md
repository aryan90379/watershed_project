# Groundwater Level & XLRM Water-Budget Analysis: Malshiras Taluka (2015–2019)

This repository contains the complete datasets, reproducible Python analysis pipeline, generated summary tables, high-resolution visualizations, and final project report for the **Malshiras Taluka (Solapur District, Maharashtra)** groundwater management study (2015–2019).

Building upon the preliminary seasonal depth-to-water (DTW) baseline across 22 government monitoring wells (14 SGWD/GSDA and 8 CGWB), the final analysis converts observed water-table fluctuations into a **seasonal aquifer water budget** (quantifying gross monsoon recharge, seasonal pumping draft, and net storage change in mm) within an **XLRM (Uncertainties, Levers, Relationships, Measures)** framework. This links empirical well observations directly to the design and evaluation of supply-side Managed Aquifer Recharge (MAR) structures and demand-side irrigation interventions.

---

## 1. Repository & Folder Structure

```text
watershed_project/
├── final_submission/
│   ├── Final_Project_Report.pdf                      # Complete standalone Final Project Report (with embedded Figures 1 & 2)
│   └── code_analysis/                                # Clean, self-contained code, datasets, outputs, and figures
│       ├── README.md                                 # Detailed documentation of the code_analysis package
│       ├── well_level_groundwater_2015_2019.csv      # Input dataset 1: Seasonal DTW observations across 22 wells (m bgl)
│       ├── annual_rainfall_2015_2019.csv             # Input dataset 2: Official Malshiras Taluka annual rainfall (mm)
│       ├── groundwater_preliminary_analysis.py       # Script 1: Baseline seasonal DTW means, valid well counts, and Figure 1
│       ├── groundwater_final_xlrm_analysis.py        # Script 2: XLRM water-budget simulation, sensitivity analysis, and Figures 1 & 2
│       ├── calculated_seasonal_summary.csv           # Output CSV 1: Baseline seasonal DTW statistics (2015–2019)
│       ├── xlrm_scenario_summary_2015_2019.csv       # Output CSV 2: Full XLRM water-budget & policy scenario outputs
│       ├── Figure_1_Baseline_Seasonal_DTW.png        # Output Visual 1: Baseline May vs. Oct/Nov mean DTW (2015–2019)
│       ├── Figure_2_XLRM_Management_Scenarios.png    # Output Visual 2: XLRM Post-Monsoon DTW & Storage Recovery dS
│       └── requirements.txt                          # Python package dependencies
├── well_level_groundwater_2015_2019.csv              # Root copy of well-level input CSV
├── annual_rainfall_2015_2019.csv                     # Root copy of annual rainfall input CSV
├── groundwater_preliminary_analysis.py               # Root copy of preliminary analysis script
├── groundwater_final_xlrm_analysis.py                # Root copy of final XLRM analysis script
├── calculated_seasonal_summary.csv                   # Root copy of baseline summary table
├── groundwater_preliminary_results.png               # Baseline figure output
├── requirements.txt                                  # Python dependencies
└── README.md                                         # Main repository documentation
```

---

## 2. Detailed Guide to Files in `final_submission/code_analysis/`

### A. Input Datasets

1. **[`well_level_groundwater_2015_2019.csv`](final_submission/code_analysis/well_level_groundwater_2015_2019.csv)**
   - **Source:** Transcribed from Table 02 of the GSDA (2020) *Atal Bhujal Yojana Hydrogeological Report: Malshiras Taluka, Solapur District*.
   - **Spatial Coverage:** 22 monitoring wells distributed across Malshiras Taluka (`14` monitored by `SGWD/GSDA` and `8` by `CGWB`).
   - **Temporal Coverage:** Pre-monsoon (`May`) and post-monsoon (`October/November`) depth-to-water readings for five consecutive years (`2015–2019`).
   - **Units & Schema:**
     - `well_name`: Village/location identifier of the monitoring well.
     - `agency`: Monitoring authority (`SGWD/GSDA` or `CGWB`).
     - `May_<YEAR>_m_bgl`: Pre-monsoon depth-to-water in metres below ground level (m bgl).
     - `Post_<YEAR>_m_bgl`: Post-monsoon (October/November) depth-to-water in metres below ground level (m bgl).
   - **Missing Value Handling:** Unrecorded seasons are stored as blank cells (null) and excluded from that season's average rather than replaced with zero (since `0 m bgl` would falsely represent water at the ground surface).

2. **[`annual_rainfall_2015_2019.csv`](final_submission/code_analysis/annual_rainfall_2015_2019.csv)**
   - **Source:** Official Solapur District Administration taluka-wise rainfall records.
   - **Schema:**
     - `year`: Calendar year (`2015` to `2019`).
     - `annual_rainfall_mm`: Total annual rainfall in millimetres (`215.29` to `582.30` mm).

---

### B. Python Analysis Scripts (How the Code Works)

#### 1. [`groundwater_preliminary_analysis.py`](final_submission/code_analysis/groundwater_preliminary_analysis.py) — *Baseline Empirical Analysis*
This script establishes the historical baseline from the raw well and rainfall CSV files:
- **`read_csv(path)` & `number_or_none(value)`**: Safely parses UTF-8 CSV files, stripping whitespace and converting blank entries to `None` while validating finite floating-point readings.
- **Seasonal Aggregation Loop (`main()`)**:
  - Iterates through `YEARS = [2015, 2016, 2017, 2018, 2019]`.
  - Filters valid readings for `May_<year>_m_bgl` and `Post_<year>_m_bgl`, recording the active sample count (`n_may` = 19–20, `n_oct_nov` = 20–21).
  - Computes arithmetic seasonal means (`mean_may_dtw_m_bgl` and `mean_oct_nov_dtw_m_bgl`) rounded to 2 decimal places.
  - Computes the observed seasonal water-table rise (`seasonal_rise_m = mean_may_dtw_m_bgl - mean_oct_nov_dtw_m_bgl`).
- **Outputs**:
  - Writes [`calculated_seasonal_summary.csv`](final_submission/code_analysis/calculated_seasonal_summary.csv).
  - Renders the baseline comparative time-series plot (`groundwater_preliminary_results.png` / `Figure_1_Baseline_Seasonal_DTW.png`) with sample counts (`n`) annotated on every data point.

#### 2. [`groundwater_final_xlrm_analysis.py`](final_submission/code_analysis/groundwater_final_xlrm_analysis.py) — *XLRM Water-Budget & Policy Scenario Simulation*
This script extends the baseline observations into an XLRM decision-analysis model using the **Water Table Fluctuation (WTF) method** (Healy & Cook, 2002; CGWB GEC-2015):

- **Hydrogeological Parameterization**:
  - `SY_REF = 0.020`: Reference specific yield (2.0% effective storage porosity) for unconfined fractured/weathered Deccan Trap basalt per CGWB GEC-2015 norms.
  - `SY_LOW = 0.015`, `SY_HIGH = 0.025`: Lower and upper specific yield uncertainty bounds (1.5% to 2.5%).
  - `FR_REF = 0.22`: Gross monsoon recharge coefficient capturing direct rainfall infiltration plus surface/canal seepage across the command area.

- **`compute_baseline_and_xlrm()` — Water Budget Decomposition & Scenario Engine**:
  1. **Observed Seasonal Storage Change (`dS_obs_mm`)**:
     Converts each year's observed water-table rise (`dh_obs_m`) into volumetric water depth (in mm of water equivalent):
     ```text
     dS_obs_mm = SY_REF * dh_obs_m * 1000.0
     ```
  2. **Baseline Recharge & Implied Seasonal Draft (`R_base_mm` & `D_base_mm`)**:
     Separates observed net storage change into gross monsoon recharge and implied seasonal net draft/extraction:
     ```text
     R_base_mm = FR_REF * annual_rainfall_mm
     D_base_mm = R_base_mm - dS_obs_mm
     ```
     *Key Insight Revealed by the Code:* In 2018 (`P = 332.50 mm`), gross recharge was `73.15 mm`, but net storage gain was only `3.00 mm` (`dh = 0.15 m`), revealing that seasonal draft surged to `70.15 mm` (consuming 96% of recharge due to protective irrigation pumping during monsoon dry spells).
  3. **Policy Lever Simulation (`LEVERS`: `L0`, `L1`, `L2`, `L3`)**:
     Evaluates four management portfolios parameterized by supply-side MAR recharge enhancement (`alpha_MAR`) and demand-side draft reduction (`beta_dem`):
     - **`L0` (Baseline BAU):** `alpha_MAR = 0.00`, `beta_dem = 0.00`
     - **`L1` (Supply-Side MAR — check dams, nala bunds, percolation tanks):** `alpha_MAR = 0.20` (+20% recharge), `beta_dem = 0.00`
     - **`L2` (Demand-Side Management — drip irrigation, crop shift):** `alpha_MAR = 0.00`, `beta_dem = 0.25` (-25% seasonal draft)
     - **`L3` (Integrated Management — combined supply + demand):** `alpha_MAR = 0.20`, `beta_dem = 0.25`
     For each lever, the code computes simulated storage recovery (`dS_sim_mm`), simulated water-table rise (`dh_sim_m`), and simulated post-monsoon depth-to-water (`dtw_sim_m`):
     ```text
     R_sim_mm = (1.0 + alpha_MAR) * R_base_mm
     D_sim_mm = (1.0 - beta_dem) * D_base_mm
     dS_sim_mm = R_sim_mm - D_sim_mm
     dh_sim_m = (dS_sim_mm / 1000.0) / SY_REF
     dtw_sim_m = pre_mean - dh_sim_m
     ```
  4. **Aquifer Specific Yield Uncertainty Propagation (`[SY_LOW, SY_HIGH]`)**:
     Computes how the water-table depth response varies across `Sy in [0.015, 0.025]`, generating the shaded uncertainty envelope (`L3_post_dtw_sy015_m` to `L3_post_dtw_sy025_m`).

- **`plot_figure_1(rows)` & `plot_figure_2(rows)`**:
  - `plot_figure_1`: Generates [`Figure_1_Baseline_Seasonal_DTW.png`](final_submission/code_analysis/Figure_1_Baseline_Seasonal_DTW.png) (220 DPI) comparing observed May and October/November DTW with embedded caption.
  - `plot_figure_2`: Generates [`Figure_2_XLRM_Management_Scenarios.png`](final_submission/code_analysis/Figure_2_XLRM_Management_Scenarios.png) (220 DPI), a two-panel figure showing:
    - **Panel (a):** Simulated post-monsoon DTW (m bgl) across 2015–2019 for `L0–L3`, the `L3` specific yield uncertainty band (`Sy in [0.015, 0.025]`), the `3.50 m bgl` sustainability target line, and a callout highlighting why `L2` outperforms `L1` in the 2018 stress year.
    - **Panel (b):** Grouped bar chart of net seasonal aquifer storage recovery (`dS` in mm) across all years and levers.

---

### C. Generated Output Tables & Figures

1. **[`calculated_seasonal_summary.csv`](final_submission/code_analysis/calculated_seasonal_summary.csv)** — Baseline Summary Table:

| Year | Annual Rainfall (mm) | Mean May DTW (m bgl) | Valid May Wells ($n$) | Mean Oct/Nov DTW (m bgl) | Valid Oct/Nov Wells ($n$) | Observed Seasonal Rise `dh` (m) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2015** | 215.29 | 6.46 | 19 | 5.14 | 20 | **1.32** |
| **2016** | 436.70 | 7.17 | 20 | 3.04 | 20 | **4.13** |
| **2017** | 530.52 | 6.86 | 20 | 2.78 | 20 | **4.08** |
| **2018** | 332.50 | 6.02 | 20 | 5.87 | 20 | **0.15** |
| **2019** | 582.30 | 8.07 | 20 | 3.63 | 21 | **4.44** |

2. **[`xlrm_scenario_summary_2015_2019.csv`](final_submission/code_analysis/xlrm_scenario_summary_2015_2019.csv)** — XLRM Water-Budget & Scenario Results (at reference `Sy = 0.020`, `fr = 0.22`):

| Year | Gross Recharge `R` (mm) | Implied Draft `D` (mm) | `L0` Baseline Post-DTW (m) [`dS` mm] | `L1` Supply (+20% MAR) Post-DTW (m) [`dS` mm] | `L2` Demand (-25% Draft) Post-DTW (m) [`dS` mm] | `L3` Integrated Post-DTW (m) [`dS` mm] | `L3` Post-DTW Uncertainty Band (`Sy` 0.015–0.025) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2015** | 47.36 | 20.96 | 5.14 [26.4] | 4.67 [35.9] | 4.88 [31.6] | **4.40** [41.1] | 4.16 – 4.55 m |
| **2016** | 96.07 | 13.47 | 3.04 [82.6] | 2.08 [101.8] | 2.87 [86.0] | **1.91** [105.2] | 1.53 – 2.14 m |
| **2017** | 116.71 | 35.11 | 2.78 [81.6] | 1.61 [104.9] | 2.34 [90.4] | **1.17** [113.7] | 0.64 – 1.49 m |
| **2018** | 73.15 | **70.15** | 5.87 [3.0] | 5.14 [17.6] | **4.99** [20.5] | **4.26** [35.2] | 3.73 – 4.58 m |
| **2019** | 128.11 | 39.31 | 3.63 [88.8] | 2.35 [114.4] | 3.14 [98.6] | **1.86** [124.2] | 1.27 – 2.21 m |
| **5-Yr Mean** | **92.28** | **35.80** | **4.09 m** [56.5] | **3.17 m** [74.9] | **3.64 m** [65.4] | **2.72 m** [83.9] | **2.27 – 3.00 m** |

---

## 3. How to Run the Code

You can run the scripts either from the repository root or directly inside `final_submission/code_analysis/`:

```bash
# 1. Create and activate a Python virtual environment (if not already active)
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies (matplotlib & numpy)
pip install -r final_submission/code_analysis/requirements.txt

# 3. Run the preliminary baseline analysis
python final_submission/code_analysis/groundwater_preliminary_analysis.py

# 4. Run the final XLRM water-budget & scenario analysis
python final_submission/code_analysis/groundwater_final_xlrm_analysis.py
```

---

## 4. Primary References & Data Sources

1. **Ground Water Surveys and Development Agency (GSDA) (2020).** *Atal Bhujal Yojana Hydrogeological Report: Malshiras Taluka, Solapur District, Maharashtra* (Table 02: Historical Pre- and Post-Monsoon Groundwater Level Monitoring Data, 2015–2019). Water Supply and Sanitation Department, Government of Maharashtra.  
   URL: https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf
2. **Solapur District Administration (2020).** *Official Taluka-wise Annual Rainfall Records (Malshiras Taluka, 2015–2019)*. Revenue and Forest Department, Government of Maharashtra.  
   URL: https://solapur.gov.in/en/rainfall/
3. **Healy, R. W., and Cook, P. G. (2002).** Using groundwater levels to estimate recharge. *Hydrogeology Journal*, 10(1), 91–109; along with **Central Ground Water Board (CGWB) (2017)**, *Report of the Ground Water Resource Estimation Committee (GEC-2015)*, Ministry of Water Resources, Government of India.
