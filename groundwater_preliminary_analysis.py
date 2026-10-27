"""Reproduce the CE766 preliminary groundwater statistics and figure.

The well-level readings in well_level_groundwater_2015_2019.csv are a manual
transcription of Table 02 in the GSDA Malshiras hydrogeological report. Missing
measurements are blank and are treated as missing, not zero. Please spot-check
this transcription against the source PDF before public submission.

This script computes each seasonal mean from the available well records,
reports the number of valid wells, computes the difference in mean depth-to-water,
and produces a chart and summary CSV.

Dependencies: Python 3.9+ and matplotlib
Install: python -m pip install matplotlib
Run:     python groundwater_preliminary_analysis.py

Sources:
GSDA (2020), Atal Bhujal Yojana Hydrogeological Report: Malshiras Taluka,
Table 02: https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf
Solapur District Administration rainfall records:
https://solapur.gov.in/en/rainfall/
"""
from __future__ import annotations

from pathlib import Path
import csv
import math
import sys
import textwrap

try:
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit("Install matplotlib first: python -m pip install matplotlib") from exc

BASE = Path(__file__).resolve().parent
WELL_CSV = BASE / "well_level_groundwater_2015_2019.csv"
RAINFALL_CSV = BASE / "annual_rainfall_2015_2019.csv"
SUMMARY_CSV = BASE / "calculated_seasonal_summary.csv"
FIGURE_PNG = BASE / "groundwater_preliminary_results.png"
YEARS = [2015, 2016, 2017, 2018, 2019]


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


def main() -> None:
    wells = read_csv(WELL_CSV)
    rainfall_rows = read_csv(RAINFALL_CSV)
    rainfall = {int(r["year"]): float(r["annual_rainfall_mm"]) for r in rainfall_rows}

    summaries = []
    for year in YEARS:
        pre_col = f"May_{year}_m_bgl"
        post_col = f"Post_{year}_m_bgl"
        pre_vals = [number_or_none(r.get(pre_col)) for r in wells]
        post_vals = [number_or_none(r.get(post_col)) for r in wells]
        pre_vals = [v for v in pre_vals if v is not None]
        post_vals = [v for v in post_vals if v is not None]
        if not pre_vals or not post_vals:
            raise ValueError(f"No valid groundwater observations for {year} in one or both seasons")
        pre_mean = sum(pre_vals) / len(pre_vals)
        post_mean = sum(post_vals) / len(post_vals)
        summaries.append({
            "year": year,
            "annual_rainfall_mm": rainfall[year],
            "mean_may_dtw_m_bgl": round(pre_mean, 2),
            "n_may": len(pre_vals),
            "mean_oct_nov_dtw_m_bgl": round(post_mean, 2),
            "n_oct_nov": len(post_vals),
            "seasonal_rise_m": round(round(pre_mean, 2) - round(post_mean, 2), 2),
        })

    fields = ["year", "annual_rainfall_mm", "mean_may_dtw_m_bgl", "n_may",
              "mean_oct_nov_dtw_m_bgl", "n_oct_nov", "seasonal_rise_m"]
    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)

    years = [r["year"] for r in summaries]
    pre = [r["mean_may_dtw_m_bgl"] for r in summaries]
    post = [r["mean_oct_nov_dtw_m_bgl"] for r in summaries]
    n_pre = [r["n_may"] for r in summaries]
    n_post = [r["n_oct_nov"] for r in summaries]

    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    ax.plot(years, pre, marker="o", linewidth=2.2, color="#1f77b4", label="May (pre-monsoon)")
    ax.plot(years, post, marker="s", linewidth=2.2, color="#ff7f0e", label="October/November (post-monsoon)")

    for x, y, n in zip(years, pre, n_pre):
        offset = (0, 9)
        if x == 2018:
            offset = (-16, 12)
        ax.annotate(f"{y:.2f} (n={n})", (x, y), xytext=offset,
                    textcoords="offset points", ha="center", fontsize=8.5)
    for x, y, n in zip(years, post, n_post):
        offset = (0, -16)
        if x == 2018:
            offset = (16, -16)
        ax.annotate(f"{y:.2f} (n={n})", (x, y), xytext=offset,
                    textcoords="offset points", ha="center", fontsize=8.5)

    ax.set_title("Mean Groundwater Depth in Malshiras Taluka (2015–2019)", pad=14, weight="bold", fontsize=12)
    ax.set_xlabel("Year", fontsize=10.5, labelpad=8)
    ax.set_ylabel("Mean depth to groundwater (m below ground level)", fontsize=10.5, labelpad=8)
    ax.set_xticks(years)
    ax.set_ylim(0, 9)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    # Put legend in lower-left where it does not collide with data labels.
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
    fig.savefig(FIGURE_PNG, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print("Calculated summary (groundwater means and n computed from well-level CSV):")
    print("Year | Rainfall (mm) | May DTW (m bgl; n) | Oct/Nov DTW (m bgl; n) | Difference (m)")
    for r in summaries:
        print(f"{r['year']} | {r['annual_rainfall_mm']:.2f} | "
              f"{r['mean_may_dtw_m_bgl']:.2f} (n={r['n_may']}) | "
              f"{r['mean_oct_nov_dtw_m_bgl']:.2f} (n={r['n_oct_nov']}) | {r['seasonal_rise_m']:.2f}")
    print(f"\nWrote: {SUMMARY_CSV.name}\nWrote: {FIGURE_PNG.name}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
