# Watershed Project: Groundwater Preliminary Analysis (CE766)

Preliminary groundwater statistics, seasonal water level analysis, and visualization for Malshiras Taluka (Solapur District, Maharashtra, India) for 2015–2019.

---

## 📁 Repository Contents

| File | Description |
| :--- | :--- |
| [`well_level_groundwater_2015_2019.csv`](well_level_groundwater_2015_2019.csv) | Seasonal well-level measurements (in meters below ground level, m bgl) manually transcribed from Table 02 of the GSDA Malshiras report. |
| [`annual_rainfall_2015_2019.csv`](annual_rainfall_2015_2019.csv) | Annual rainfall records for Malshiras Taluka (2015–2019). |
| [`groundwater_preliminary_analysis.py`](groundwater_preliminary_analysis.py) | Python script computing seasonal means, sample counts, seasonal differences, summary CSV, and visualization. |
| [`calculated_seasonal_summary.csv`](calculated_seasonal_summary.csv) | Generated seasonal summary with pre- and post-monsoon DTW means and seasonal rise. |
| [`groundwater_preliminary_results.png`](groundwater_preliminary_results.png) | High-resolution plot showing pre- vs. post-monsoon depth-to-water levels. |
| [`requirements.txt`](requirements.txt) | Python dependencies required to run the analysis. |

---

## ⚙️ Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/aryan90379/watershed_project.git
cd watershed_project
```

### 2. Set up a virtual environment (Recommended)
```bash
# Using Homebrew Python or system Python 3
python3 -m venv .venv

# Activate the virtual environment
# On macOS / Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Analysis

Once your environment is active, run:
```bash
python groundwater_preliminary_analysis.py
```

This will:
1. Parse well and rainfall observations.
2. Calculate pre-monsoon (May) and post-monsoon (October/November) mean depth to groundwater.
3. Compute the seasonal water table rise.
4. Output `calculated_seasonal_summary.csv` and generate `groundwater_preliminary_results.png`.

---

## 📊 Analytical Methodology

$$\text{Mean DTW}(\text{year}, \text{season}) = \frac{\sum \text{valid well DTW measurements}}{\text{number of valid wells}}$$

$$\text{Seasonal Difference (m)} = \text{Mean DTW}_{\text{May}} - \text{Mean DTW}_{\text{Post-monsoon}}$$

> **Interpretation Note:** A positive seasonal difference indicates that the post-monsoon depth-to-water is lower (the water table has risen closer to the surface compared to May). Depth-to-water is not a direct measurement of total groundwater storage.

---

## 📚 Data Sources

1. **Ground Water Surveys and Development Agency (GSDA), 2020**  
   *Atal Bhujal Yojana Hydrogeological Report: Malshiras Taluka, Solapur District*, Table 02:  
   [GSDA Report PDF](https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf)

2. **Solapur District Administration**  
   *Rainfall Records*:  
   [Solapur District Rainfall Portal](https://solapur.gov.in/en/rainfall/)
