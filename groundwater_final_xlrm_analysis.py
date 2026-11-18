"""CE766 Final Project Analysis: XLRM Groundwater Management Simulation for Malshiras Taluka (2015-2019).

Builds directly upon the preliminary baseline seasonal depth-to-water (DTW) analysis
(well_level_groundwater_2015_2019.csv and annual_rainfall_2015_2019.csv) using the
Water Table Fluctuation (WTF) method (Healy & Cook, 2002; CGWB GEC-2015) within an
XLRM (Uncertainties, Levers, Relationships, Measures) decision-making framework.

Outputs saved to final_submission/:
  1. Figure_1_Baseline_Seasonal_DTW.png
  2. Figure_2_XLRM_Management_Scenarios.png
  3. xlrm_scenario_summary_2015_2019.csv
"""
from __future__ import annotations

from pathlib import Path
import csv
import math
import sys
import textwrap

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as exc:
    raise SystemExit("Install matplotlib and numpy first: python -m pip install matplotlib numpy") from exc

BASE = Path(__file__).resolve().parent
WELL_CSV = BASE / "well_level_groundwater_2015_2019.csv"
RAINFALL_CSV = BASE / "annual_rainfall_2015_2019.csv"
FINAL_DIR = BASE / "final_submission"

FIG1_PNG = FINAL_DIR / "Figure_1_Baseline_Seasonal_DTW.png"
FIG2_PNG = FINAL_DIR / "Figure_2_XLRM_Management_Scenarios.png"
XLRM_CSV = FINAL_DIR / "xlrm_scenario_summary_2015_2019.csv"

YEARS = [2015, 2016, 2017, 2018, 2019]

# Reference hydrogeological parameters for Deccan Trap basalt (CGWB GEC-2015 norms)
SY_REF = 0.020          # Specific yield (dimensionless: 2.0% effective storage porosity)
SY_LOW = 0.015          # Lower bound specific yield (1.5% for tighter fractured basalt)
SY_HIGH = 0.025         # Upper bound specific yield (2.5% for weathered vesicular basalt)
FR_REF = 0.22           # Gross monsoon recharge factor (rainfall infiltration + surface/canal seepage)

# Policy Levers (L0 to L3): (id, label, short_label, alpha_MAR, beta_dem, color, marker, linestyle)
LEVERS = [
    ("L0", "L0: Baseline (Historical BAU)", "L0: Baseline", 0.00, 0.00, "#1f77b4", "o", "-"),
    ("L1", "L1: Supply-Side MAR (+20% Recharge)", "L1: Supply (+20% MAR)", 0.20, 0.00, "#2ca02c", "^", "--"),
    ("L2", "L2: Demand-Side Management (-25% Draft)", "L2: Demand (-25% Draft)", 0.00, 0.25, "#ff7f0e", "s", "-."),
    ("L3", "L3: Integrated Management (+20% MAR, -25% Draft)", "L3: Integrated (+20% MAR, -25% Draft)", 0.20, 0.25, "#d62728", "D", "-"),
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path.name}")
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def number_or_none(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        v = float(value)
    except ValueError as exc:
        raise ValueError(f"Not a number: {value!r}") from exc
    if not math.isfinite(v):
        return None
    return v


def compute_baseline_and_xlrm() -> tuple[list[dict], dict]:
    wells = read_csv(WELL_CSV)
    rainfall_rows = read_csv(RAINFALL_CSV)
    rainfall = {int(r["year"]): float(r["annual_rainfall_mm"]) for r in rainfall_rows}

    baseline_rows = []
    for year in YEARS:
        pre_col = f"May_{year}_m_bgl"
        post_col = f"Post_{year}_m_bgl"
        pre_vals = [number_or_none(r.get(pre_col)) for r in wells]
        post_vals = [number_or_none(r.get(post_col)) for r in wells]
        pre_vals = [v for v in pre_vals if v is not None]
        post_vals = [v for v in post_vals if v is not None]

        pre_mean = round(sum(pre_vals) / len(pre_vals), 2)
        post_mean = round(sum(post_vals) / len(post_vals), 2)
        dh_obs = round(pre_mean - post_mean, 2)
        p_mm = rainfall[year]

        # Water balance components in mm water equivalent at reference Sy = 0.020, fr = 0.22
        dS_obs_mm = round(SY_REF * dh_obs * 1000.0, 2)
        R_base_mm = round(FR_REF * p_mm, 2)
        D_base_mm = round(R_base_mm - dS_obs_mm, 2)

        row = {
            "year": year,
            "annual_rainfall_mm": p_mm,
            "mean_may_dtw_m_bgl": pre_mean,
            "n_may": len(pre_vals),
            "mean_oct_nov_dtw_m_bgl": post_mean,
            "n_oct_nov": len(post_vals),
            "dh_obs_m": dh_obs,
            "dS_obs_mm": dS_obs_mm,
            "R_base_mm": R_base_mm,
            "D_base_mm": D_base_mm,
        }

        # Simulate each policy lever
        for lid, _, _, alpha, beta, _, _, _ in LEVERS:
            R_sim_mm = (1.0 + alpha) * R_base_mm
            D_sim_mm = (1.0 - beta) * D_base_mm
            dS_sim_mm = round(R_sim_mm - D_sim_mm, 2)

            # Reference Sy = 0.020
            dh_sim_m = round((dS_sim_mm / 1000.0) / SY_REF, 2)
            dtw_sim_m = round(pre_mean - dh_sim_m, 2)

            # Uncertainty bounds on additional storage gain (delta_dS = alpha*R_base + beta*D_base)
            delta_dS_mm = alpha * R_base_mm + beta * D_base_mm
            dh_gain_low_Sy = (delta_dS_mm / 1000.0) / SY_LOW    # Larger rise when Sy is smaller (0.015)
            dh_gain_high_Sy = (delta_dS_mm / 1000.0) / SY_HIGH  # Smaller rise when Sy is larger (0.025)

            dtw_sim_sy_low = round(post_mean - dh_gain_low_Sy, 2)   # Shallower DTW bound
            dtw_sim_sy_high = round(post_mean - dh_gain_high_Sy, 2) # Deeper DTW bound

            row[f"{lid}_dS_mm"] = dS_sim_mm
            row[f"{lid}_dh_m"] = dh_sim_m
            row[f"{lid}_post_dtw_m"] = dtw_sim_m
            row[f"{lid}_post_dtw_sy015_m"] = dtw_sim_sy_low
            row[f"{lid}_post_dtw_sy025_m"] = dtw_sim_sy_high

        baseline_rows.append(row)

    return baseline_rows, rainfall


def plot_figure_1(rows: list[dict]) -> None:
    years = [r["year"] for r in rows]
    pre = [r["mean_may_dtw_m_bgl"] for r in rows]
    post = [r["mean_oct_nov_dtw_m_bgl"] for r in rows]
    n_pre = [r["n_may"] for r in rows]
    n_post = [r["n_oct_nov"] for r in rows]

    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    ax.plot(years, pre, marker="o", linewidth=2.2, color="#1f77b4", label="May (pre-monsoon)")
    ax.plot(years, post, marker="s", linewidth=2.2, color="#ff7f0e", label="October/November (post-monsoon)")

    for x, y, n in zip(years, pre, n_pre):
        offset = (0, 9)
        if x == 2018:
            offset = (0, 11)
        ax.annotate(f"{y:.2f} (n={n})", (x, y), xytext=offset,
                    textcoords="offset points", ha="center", fontsize=8.5)
    for x, y, n in zip(years, post, n_post):
        offset = (0, -16)
        if x == 2018:
            offset = (0, -18)
        ax.annotate(f"{y:.2f} (n={n})", (x, y), xytext=offset,
                    textcoords="offset points", ha="center", fontsize=8.5)

    ax.set_title("Mean Groundwater Depth in Malshiras Taluka (2015-2019)", pad=14, weight="bold", fontsize=12)
    ax.set_xlabel("Year", fontsize=10.5, labelpad=8)
    ax.set_ylabel("Mean depth to groundwater (m below ground level)", fontsize=10.5, labelpad=8)
    ax.set_xticks(years)
    ax.set_ylim(0, 9)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.legend(frameon=False, loc="lower left", fontsize=9.5)

    caption = (
        "Figure 1. Mean pre-monsoon (May) and post-monsoon (October/November) depth-to-water in Malshiras Taluka, 2015–2019. "
        "Values are in metres below ground level (m bgl); n indicates the number of valid well observations used to calculate "
        "each seasonal mean. Lower depth-to-water values indicate a shallower water table. "
        "Source: GSDA, Atal Bhujal Yojana Hydrogeological Report, Malshiras Taluka, Table 02."
    )
    wrapped_caption = textwrap.fill(caption, width=118)
    fig.text(
        0.06, 0.02,
        wrapped_caption,
        ha="left", va="bottom", fontsize=8.8, linespacing=1.35
    )
    fig.tight_layout(rect=(0.04, 0.12, 0.98, 0.98))
    fig.savefig(FIG1_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_figure_2(rows: list[dict]) -> None:
    years = [r["year"] for r in rows]
    x_idx = np.arange(len(years))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 6.8), gridspec_kw={"width_ratios": [1.15, 1.0]})

    # --- Panel (a): Post-Monsoon DTW under Levers L0-L3 + Sy Uncertainty Band ---
    for lid, label, short_label, _, _, color, marker, ls in LEVERS:
        y_vals = [r[f"{lid}_post_dtw_m"] for r in rows]
        ax1.plot(years, y_vals, marker=marker, linewidth=2.2, linestyle=ls, color=color, label=short_label, zorder=4)

    # Shaded uncertainty band for L3 across Sy in [0.015, 0.025]
    l3_low = [r["L3_post_dtw_sy015_m"] for r in rows]
    l3_high = [r["L3_post_dtw_sy025_m"] for r in rows]
    ax1.fill_between(
        years, l3_low, l3_high, color="#d62728", alpha=0.14,
        label="L3 Uncertainty Band (Sy in [0.015, 0.025])", zorder=2
    )

    # Sustainable post-monsoon target line (3.50 m bgl)
    ax1.axhline(3.50, color="#4a5568", linestyle=":", linewidth=1.4, label="Target Post-Monsoon Threshold (3.50 m bgl)", zorder=3)

    # Annotate L0 and L3 data points clearly
    for r in rows:
        yr = r["year"]
        v_l0 = r["L0_post_dtw_m"]
        v_l3 = r["L3_post_dtw_m"]
        l0_offset = (0, 8)
        l3_offset = (0, -15)
        if yr == 2015:
            l3_offset = (-18, -12)
        elif yr == 2018:
            l3_offset = (0, -16)
        ax1.annotate(f"{v_l0:.2f}", (yr, v_l0), xytext=l0_offset, textcoords="offset points",
                     ha="center", fontsize=8.2, color="#1f77b4", weight="bold")
        ax1.annotate(f"{v_l3:.2f}", (yr, v_l3), xytext=l3_offset, textcoords="offset points",
                     ha="center", fontsize=8.2, color="#b81d1d", weight="bold")

    # Annotate 2018 L1 vs L2 comparison
    r2018 = [r for r in rows if r["year"] == 2018][0]
    ax1.annotate(f"2018 Stress Year:\nL1 (MAR): {r2018['L1_post_dtw_m']:.2f} m\nL2 (Demand): {r2018['L2_post_dtw_m']:.2f} m",
                 xy=(2018, r2018["L2_post_dtw_m"]), xytext=(2016.85, 5.15),
                 arrowprops=dict(arrowstyle="->", color="#4a5568", lw=0.9),
                 ha="center", va="center", fontsize=7.8, color="#2d3748",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fffaf0", edgecolor="#cbd5e0", lw=0.8))

    ax1.set_title("(a) Simulated Post-Monsoon Depth-to-Water (2015-2019)", pad=10, weight="bold", fontsize=11)
    ax1.set_xlabel("Year", fontsize=10, labelpad=6)
    ax1.set_ylabel("Post-monsoon DTW (m below ground level)", fontsize=10, labelpad=6)
    ax1.set_xticks(years)
    ax1.set_ylim(0.3, 7.5)
    ax1.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax1.legend(frameon=True, facecolor="white", framealpha=0.95, edgecolor="#e2e8f0", loc="upper left", fontsize=8.0)

    # --- Panel (b): Seasonal Net Aquifer Storage Recovery (dS in mm) across Scenarios ---
    bar_width = 0.19
    offsets = [-1.5 * bar_width, -0.5 * bar_width, 0.5 * bar_width, 1.5 * bar_width]
    for offset, (lid, _, short_label, _, _, color, _, _) in zip(offsets, LEVERS):
        dS_vals = [r[f"{lid}_dS_mm"] for r in rows]
        ax2.bar(x_idx + offset, dS_vals, width=bar_width, color=color, alpha=0.88, label=short_label)
        for i, (yr, val) in enumerate(zip(years, dS_vals)):
            ax2.annotate(f"{val:.0f}" if val >= 10 else f"{val:.1f}",
                         (x_idx[i] + offset, val), xytext=(0, 3),
                         textcoords="offset points", ha="center", va="bottom", fontsize=7.0)

    ax2.set_title("(b) Net Seasonal Aquifer Storage Recovery dS (mm)", pad=10, weight="bold", fontsize=11)
    ax2.set_xlabel("Year (with Annual Rainfall P in mm)", fontsize=10, labelpad=6)
    ax2.set_ylabel("Seasonal groundwater storage gain dS (mm)", fontsize=10, labelpad=6)
    ax2.set_xticks(x_idx)
    ax2.set_xticklabels([f"{r['year']}\n({r['annual_rainfall_mm']:.0f} mm)" for r in rows], fontsize=8.5)
    ax2.set_ylim(0, 140)
    ax2.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax2.legend(frameon=True, facecolor="white", edgecolor="#e2e8f0", loc="upper left", fontsize=8.0)

    caption2 = (
        "Figure 2. XLRM scenario analysis of groundwater management interventions in Malshiras Taluka (2015–2019): "
        "(a) Post-monsoon depth-to-water (m bgl) under Baseline (L0), Supply-Side MAR (+20% recharge, L1), Demand-Side Management "
        "(-25% draft, L2), and Integrated Management (L3), with the L3 uncertainty band across specific yield Sy in [0.015, 0.025]; "
        "(b) Net seasonal aquifer storage recovery dS (mm water equivalent) at reference Sy = 0.020, fr = 0.22."
    )
    wrapped_caption2 = textwrap.fill(caption2, width=155)
    fig.text(
        0.04, 0.015,
        wrapped_caption2,
        ha="left", va="bottom", fontsize=8.6, linespacing=1.32
    )
    fig.tight_layout(rect=(0.02, 0.11, 0.99, 0.98))
    fig.savefig(FIG2_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    rows, _ = compute_baseline_and_xlrm()

    # Save CSV
    fields = list(rows[0].keys())
    with XLRM_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    plot_figure_1(rows)
    plot_figure_2(rows)

    print(f"Generated: {FIG1_PNG.relative_to(BASE)}")
    print(f"Generated: {FIG2_PNG.relative_to(BASE)}")
    print(f"Generated: {XLRM_CSV.relative_to(BASE)}")


if __name__ == "__main__":
    main()
