"""Generate a natural, human-written, well-spaced Google-Docs-style Final Project Report PDF."""
from __future__ import annotations

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

BASE = Path(__file__).resolve().parent
FINAL_DIR = BASE / "final_submission"
PDF_OUT = FINAL_DIR / "Final_Project_Report.pdf"

# Register system Arial fonts (standard Google Docs font)
FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "Arial Italic.ttf")))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", str(FONT_DIR / "Arial Bold Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Arial",
    normal="Arial",
    bold="Arial-Bold",
    italic="Arial-Italic",
    boldItalic="Arial-BoldItalic",
)

# ---------------------------------------------------------------------------
# NATURAL, HUMAN-WRITTEN SECTIONS (Strictly within Moodle word limits)
# ---------------------------------------------------------------------------

SECTION_1_PROBLEM = [
    (
        "Malshiras Taluka in Solapur District, Maharashtra, is a semi-arid, drought-prone basalt region in "
        "the Bhima River basin. Between 2015 and 2019, heavy groundwater pumping for water-intensive crops "
        "like sugarcane, combined with erratic monsoon rainfall (215.29 to 582.30 mm per year), caused "
        "recurring pre-monsoon water table depletion. In 2018, the taluka received 332.50 mm of rainfall, "
        "yet the average water table rose by only 0.15 m after the monsoon (from 6.02 to 5.87 m below ground "
        "level), compared to a 1.32 m rise in 2015 under just 215.29 mm of rainfall."
    ),
    (
        "This issue directly affects local farmers, Gram Panchayats, Water User Associations, the Groundwater "
        "Surveys and Development Agency (GSDA), the Central Ground Water Board (CGWB), and district planners "
        "under the Atal Bhujal Yojana scheme. In response to our preliminary report feedback—which noted that "
        "a water-budget-level analysis was needed to show how observed well data help in designing "
        "interventions—this final report converts the 2015–2019 well observations into a seasonal aquifer "
        "water budget (quantifying gross monsoon recharge, groundwater draft, and net storage change in mm) "
        "within an XLRM framework. This directly links the observed water-table fluctuations to the design "
        "and comparison of supply-side recharge structures (check dams, percolation tanks) and demand-side "
        "measures (micro-irrigation, crop water budgeting) under rainfall and aquifer parameter uncertainties."
    ),
]

SECTION_2_DATA = [
    (
        "Groundwater level observations for 2015–2019 were transcribed from Table 02 of the GSDA (2020) Atal "
        "Bhujal Yojana hydrogeological report for Malshiras Taluka. The dataset covers 22 monitoring wells "
        "across the taluka (14 monitored by SGWD/GSDA and 8 by CGWB), which are averaged to provide a lumped "
        "taluka-level spatial representation. Temporally, the observations consist of two seasonal readings per "
        "year: pre-monsoon (May) and post-monsoon (October/November). Missing measurements were left blank rather "
        "than set to zero, leaving 19 to 20 valid wells in May and 20 to 21 valid wells in October/November."
    ),
    (
        "Annual rainfall totals for 2015–2019 were taken from official Solapur District Administration rainfall "
        "records. Unconfined Deccan basalt specific yield values (Sy between 0.015 and 0.025, with 0.020 as the "
        "baseline) and the monsoon recharge factor (fr = 0.22) were adopted from CGWB GEC-2015 norms."
    ),
]

SECTION_3_METHODOLOGY = [
    (
        "We structured the groundwater management analysis using the XLRM framework and the Water Table "
        "Fluctuation (WTF) method (Healy and Cook, 2002; CGWB, 2017)."
    ),
    (
        "Uncertainties (X): We consider two main uncertainties: (1) annual rainfall P across the observed "
        "2015–2019 range of 215.29 to 582.30 mm, and (2) specific yield Sy of the fractured basalt aquifer, "
        "tested across 0.015, 0.020, and 0.025 (dimensionless), with a baseline monsoon recharge factor fr = 0.22."
    ),
    (
        "Policy Levers (L): We evaluate four management options defined by a supply-side recharge gain factor (a) "
        "and a demand-side pumping reduction factor (b):"
    ),
    (
        "• L0 (Baseline): no new intervention (a = 0, b = 0)."
    ),
    (
        "• L1 (Supply-Side MAR): check dams and percolation tanks increasing monsoon recharge by 20% (a = 0.20, b = 0)."
    ),
    (
        "• L2 (Demand-Side Management): micro-irrigation and crop shifts cutting seasonal draft by 25% (a = 0, b = 0.25)."
    ),
    (
        "• L3 (Integrated Management): combining both 20% recharge augmentation and 25% draft reduction (a = 0.20, b = 0.25)."
    ),
    (
        "Relationships (R) and Main Equations (Healy and Cook, 2002; CGWB, 2017):"
    ),
    (
        "Mean DTW(year, season) = sum of valid well depth-to-water readings / n"
    ),
    (
        "Seasonal Rise dh = Mean DTW May - Mean DTW OctNov"
    ),
    (
        "Baseline Storage Change dS = Sy * dh * 1000 = R - D"
    ),
    (
        "Simulated Rise dhsim = [ (1 + a) * R - (1 - b) * D ] / (1000 * Sy)"
    ),
    (
        "Simulated OctNov DTW = Mean DTW May - dhsim"
    ),
    (
        "Where n is the number of valid wells in that season; dh and dhsim are the observed and simulated seasonal "
        "water-table rises (m); dS is the net seasonal groundwater storage change (mm of water); R = fr * P is "
        "baseline gross monsoon recharge (mm); D is implied baseline seasonal net draft and discharge (mm); and "
        "Simulated OctNov DTW is the resulting post-monsoon depth-to-water (m below ground level)."
    ),
    (
        "Measures (M): Performance is evaluated using (1) post-monsoon depth-to-water (m bgl) relative to a 3.50 m "
        "bgl sustainability target, (2) net seasonal storage recovery dS (mm), and (3) water-table recovery during "
        "the 2018 dry-spell stress year."
    ),
]

SECTION_4_RESULTS = [
    (
        "Figure 1 shows the observed pre-monsoon (May) and post-monsoon (October/November) mean depth-to-water "
        "across Malshiras Taluka from 2015 to 2019. In all five years, the post-monsoon depth-to-water was lower "
        "than the pre-monsoon depth, indicating a seasonal rise in the water table. The pre-monsoon and "
        "post-monsoon means (in m bgl) were 6.46 and 5.14 in 2015 (rise dh = 1.32 m), 7.17 and 3.04 in 2016 "
        "(4.13 m), 6.86 and 2.78 in 2017 (4.08 m), 6.02 and 5.87 in 2018 (0.15 m), and 8.07 and 3.63 in 2019 "
        "(4.44 m). Figure 1 clearly highlights the 2018 anomaly: even though 2018 had 332.50 mm of rainfall "
        "(more than 2015), the water table barely recovered (0.15 m), which pushed May 2019 to the deepest "
        "pre-monsoon level of the five-year period (8.07 m bgl)."
    ),
    (
        "Figure 2 compares the simulated post-monsoon depth-to-water (Figure 2a) and net seasonal aquifer storage "
        "recovery dS (Figure 2b) across the four management scenarios (L0 to L3). Breaking down the baseline water "
        "balance (at Sy = 0.020, fr = 0.22) shows that seasonal groundwater draft D jumped to 70.15 mm in 2018, "
        "consuming 96% of the 73.15 mm gross recharge and leaving only 3.0 mm of net storage gain, compared to "
        "13.47–39.31 mm of draft in other years."
    ),
    (
        "Because of this difference, Supply-Side MAR (L1) gives larger gains than Demand-Side Management (L2) in "
        "wet years like 2016, 2017, and 2019 (boosting 2019 storage recovery from 88.8 mm to 114.4 mm under L1, "
        "versus 98.6 mm under L2). However, in the 2018 stress year, Demand-Side Management (L2: post-monsoon "
        "DTW = 4.99 m bgl, dS = 20.5 mm) outperforms Supply-Side MAR (L1: 5.14 m bgl, dS = 17.6 mm) because heavy "
        "pumping was the main driver of depletion. Integrated Management (L3) performs best overall, bringing the "
        "five-year mean post-monsoon DTW from 4.09 m down to 2.72 m bgl (ranging from 2.27 to 3.00 m bgl across "
        "the Sy uncertainty band), improving 2018 post-monsoon DTW to 4.26 m bgl, and increasing average seasonal "
        "storage recovery from 56.5 to 83.9 mm per year."
    ),
]

SECTION_5_DISCUSSION = [
    (
        "The simulation results show that seasonal groundwater recovery in Malshiras Taluka depends on the balance "
        "between monsoon recharge and agricultural pumping, rather than total annual rainfall alone. In our water "
        "balance model, separating net storage change (dS) into gross recharge (R) and seasonal draft (D) explains "
        "why 2018 saw almost no recovery: uneven rainfall during the monsoon forced farmers to pump heavily for "
        "protective irrigation (D = 70.15 mm), which cancelled out most of the natural recharge."
    ),
    (
        "This creates a clear difference in how policy levers behave. Supply-side structures (L1) scale with "
        "available rainfall and work very well in normal or wet years (2016, 2017, and 2019), but offer limited "
        "protection when pumping spikes during dry spells. In contrast, demand-side measures (L2) directly reduce "
        "seasonal extraction and provide better protection during stress years like 2018. Combining both approaches "
        "(L3) is the only strategy that keeps post-monsoon water levels above the 3.50 m bgl threshold in three out "
        "of five years while cutting the 2018 deficit by 1.61 m. Sensitivity testing across Sy (0.015 to 0.025) "
        "also shows that lower specific yield causes larger water-table swings for the same volume of extraction."
    ),
    (
        "For watershed decision-making under Atal Bhujal Yojana, these results show that building check dams and "
        "percolation tanks must be paired with demand-side crop and irrigation management. However, because our "
        "model uses lumped taluka-level averages, the numbers cannot be used directly to size or locate individual "
        "structures on the ground. Making this analysis ready for field implementation would require: (1) delineating "
        "exact sub-watershed boundaries using a Digital Elevation Model (DEM) instead of administrative taluka borders, "
        "(2) collecting monthly or daily rainfall and water-level data to track within-monsoon recharge and summer "
        "drawdown separately, (3) gathering village-level crop area, canal seepage, and electricity or pump-metering "
        "records to measure draft directly, and (4) conducting pumping tests to calibrate spatially varying specific "
        "yield and transmissivity in a distributed groundwater model such as MODFLOW."
    ),
]

SECTION_6_REFERENCES = [
    (
        "1. Ground Water Surveys and Development Agency (GSDA) (2020). Atal Bhujal Yojana Hydrogeological Report: "
        "Malshiras Taluka, Solapur District, Maharashtra (Table 02: Historical Pre- and Post-Monsoon Groundwater "
        "Level Monitoring Data, 2015–2019). Water Supply and Sanitation Department, Government of Maharashtra.<br/>"
        "<a href='https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf' color='#1155CC'>"
        "https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf</a>"
    ),
    (
        "2. Solapur District Administration (2020). Official Taluka-wise Annual Rainfall Records (Malshiras "
        "Taluka, 2015–2019). Revenue and Forest Department, Government of Maharashtra.<br/>"
        "<a href='https://solapur.gov.in/en/rainfall/' color='#1155CC'>"
        "https://solapur.gov.in/en/rainfall/</a>"
    ),
    (
        "3. Healy, R. W., and Cook, P. G. (2002). Using groundwater levels to estimate recharge. Hydrogeology "
        "Journal, 10(1), 91–109; along with Central Ground Water Board (CGWB) (2017), Report of the Ground "
        "Water Resource Estimation Committee (GEC-2015), Ministry of Water Resources, Government of India."
    ),
    (
        "Data and Code Repository:<br/>"
        "<a href='https://github.com/aryan90379/watershed_project' color='#1155CC'>"
        "https://github.com/aryan90379/watershed_project</a>"
    ),
]


def word_count(paragraphs: list[str]) -> int:
    joined = " ".join(p.replace("<br/>", " ") for p in paragraphs)
    return len(joined.split())


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    checks = [
        ("1. Problem Statement", SECTION_1_PROBLEM, 250),
        ("2. Data", SECTION_2_DATA, 150),
        ("3. Methodology", SECTION_3_METHODOLOGY, 400),
        ("4. Results", SECTION_4_RESULTS, 400),
        ("5. Discussion", SECTION_5_DISCUSSION, 400),
        ("6. References and Data/Code Repository", SECTION_6_REFERENCES, 500),
    ]
    for title, paras, limit in checks:
        wc = word_count(paras)
        print(f"{title}: {wc} / {limit} words")
        assert wc <= limit, f"{title} over limit: {wc} > {limit}"

    # Airy, natural Google Docs layout: Letter paper, 1-inch margins
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    title_style = ParagraphStyle(
        "GDocTitle",
        fontName="Arial-Bold",
        fontSize=15,
        leading=21,
        textColor=colors.black,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "GDocHeading",
        fontName="Arial-Bold",
        fontSize=12,
        leading=16.5,
        textColor=colors.black,
        spaceBefore=15,
        spaceAfter=7,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "GDocBody",
        fontName="Arial",
        fontSize=11,
        leading=15.8,
        textColor=colors.black,
        spaceAfter=10,
    )

    bullet_style = ParagraphStyle(
        "GDocBullet",
        fontName="Arial",
        fontSize=11,
        leading=15.5,
        leftIndent=14,
        textColor=colors.black,
        spaceAfter=5,
    )

    eq_style = ParagraphStyle(
        "GDocEquation",
        fontName="Arial",
        fontSize=11,
        leading=15.8,
        leftIndent=18,
        textColor=colors.black,
        spaceBefore=2,
        spaceAfter=7,
    )

    story = []

    story.append(
        Paragraph("Groundwater Level and XLRM Management Analysis: Malshiras Taluka (2015–2019)", title_style)
    )

    for heading, paragraphs, _ in checks:
        story.append(Paragraph(heading, heading_style))
        for p in paragraphs:
            if p.startswith("• "):
                story.append(Paragraph(p, bullet_style))
            elif any(p.startswith(prefix) for prefix in (
                "Mean DTW(year, season) =",
                "Seasonal Rise dh =",
                "Baseline Storage Change dS =",
                "Simulated Rise dhsim =",
                "Simulated OctNov DTW =",
            )):
                story.append(Paragraph(p, eq_style))
            else:
                story.append(Paragraph(p, body_style))

    doc.build(story)
    print(f"Wrote PDF: {PDF_OUT.relative_to(BASE)}")


if __name__ == "__main__":
    main()
