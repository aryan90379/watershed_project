CE766 - Groundwater Preliminary Analysis
========================================

Contents
--------
well_level_groundwater_2015_2019.csv
    Well-level seasonal measurements manually transcribed from Table 02 of the
    GSDA Malshiras hydrogeological report. Blank cells represent missing records.
    Please spot-check the transcription against the original source PDF.

annual_rainfall_2015_2019.csv
    Official Malshiras Taluka annual rainfall totals used in the preliminary report.

groundwater_preliminary_analysis.py
    Code to read the well-level observations, calculate seasonal means and valid
    sample counts, calculate May mean DTW minus post-monsoon mean DTW, and create
    the figure and calculated_seasonal_summary.csv.

calculated_seasonal_summary.csv
    Generated seasonal means, sample counts, annual rainfall and seasonal differences.

groundwater_preliminary_results.png
    Figure produced by the script, suitable as the single figure for Moodle.

How to run
----------
Install Python 3.9+ and matplotlib:
    python -m pip install matplotlib
Then run:
    python groundwater_preliminary_analysis.py

Equations used
--------------
Mean_DTW(year, season) = sum of valid well DTW measurements / number of valid wells
Seasonal_difference_m = mean_DTW_May - mean_DTW_October_or_November

Interpretation: positive seasonal difference means post-monsoon depth-to-water is
lower (the water table is shallower) than in May. Depth-to-water is not a direct
measurement of groundwater storage.

Sources
-------
1. Ground Water Surveys and Development Agency (GSDA), 2020. Atal Bhujal Yojana
   Hydrogeological Report: Malshiras Taluka, Solapur District, Table 02:
   https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf
2. Solapur District Administration, rainfall records:
   https://solapur.gov.in/en/rainfall/

Reproducibility note
--------------------
The groundwater values are a manual transcription of the published GSDA table,
not a downloaded machine-readable dataset. The script calculates the displayed
seasonal means from that transcription. It does not calibrate a groundwater model
or run management scenarios; those remain future work.
