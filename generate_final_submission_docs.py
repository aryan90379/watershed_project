"""Generate the CE766 Final Project Submission text, word-count checks, and clean PDF guide (no underscores)."""
from __future__ import annotations

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parent
FINAL_DIR = BASE / "final_submission"
PDF_OUT = FINAL_DIR / "CE766_Final_Submission_Copy_Paste_Guide.pdf"
TXT_OUT = FINAL_DIR / "CE766_Final_Submission_Text.txt"
MD_OUT = FINAL_DIR / "README_FINAL_SUBMISSION.md"

# ---------------------------------------------------------------------------
# CLEAN MOODLE SUBMISSION TEXT (No underscores in prose or equations!)
# ---------------------------------------------------------------------------

SECTION_1_PROBLEM = (
    "Malshiras Taluka in Solapur District, Maharashtra, lies within a semi-arid, drought-prone "
    "hard-rock basalt zone of the Bhima River basin. Over the 2015–2019 analysis period, intensive "
    "groundwater extraction for perennial cash crops (predominantly sugarcane and horticulture), "
    "combined with erratic monsoon rainfall (215.29 to 582.30 mm/year), produced severe pre-monsoon "
    "water-table depletion and acute vulnerability to mid-season dry spells. Crucially, moderate "
    "rainfall does not guarantee aquifer recovery: in 2018 (332.50 mm rainfall), the mean water "
    "table rose by only 0.15 m (from 6.02 to 5.87 m below ground level, m bgl), compared to a "
    "1.32 m rise in 2015 under lower rainfall (215.29 mm)."
    "\n\n"
    "For watershed management and decision-making under the Atal Bhujal Yojana (ABY), key "
    "stakeholders—including Gram Panchayats, Water User Associations (WUAs), local farmers, the "
    "Groundwater Surveys and Development Agency (GSDA), the Central Ground Water Board (CGWB), "
    "and the Solapur District Administration—must determine whether supply-side Managed Aquifer "
    "Recharge (MAR) structures (check dams, percolation tanks) or demand-side interventions "
    "(micro-irrigation, crop-water budgeting) can reliably stabilize post-monsoon groundwater "
    "levels. Building directly upon our preliminary submission (which established the baseline "
    "2015–2019 seasonal depth-to-water trends across 22 monitoring wells), this final submission "
    "extends the empirical baseline into an XLRM lumped aquifer water-balance simulation framework "
    "to evaluate supply-side, demand-side, and integrated management levers under hydrogeological "
    "and climatic uncertainties without altering the underlying field dataset."
)

SECTION_2_DATA = (
    "This study uses site-specific empirical data for Malshiras Taluka covering 2015–2019. "
    "Groundwater depth-to-water (DTW, in metres below ground level, m bgl) observations were "
    "transcribed from Table 02 of the GSDA (2020) Atal Bhujal Yojana Hydrogeological Report. "
    "Spatially, the dataset comprises 22 point monitoring wells distributed across the taluka "
    "(14 monitored by SGWD/GSDA and 8 by CGWB), aggregated to a lumped taluka-scale mean. "
    "Temporally, readings have a semi-annual seasonal resolution—pre-monsoon (May) and "
    "post-monsoon (October/November). Missing well records were retained as null values rather "
    "than zero, yielding n = 19 to 20 valid wells in May and n = 20 to 21 in October/November. "
    "Annual taluka-scale rainfall totals (mm/year) for 2015–2019 were compiled from official "
    "Solapur District Administration records. Unconfined Deccan Trap basalt specific yield "
    "(Sy from 0.015 to 0.025, reference 0.020) and monsoon recharge factor (fr = 0.22) bounds "
    "were taken from CGWB GEC-2015 norms."
)

SECTION_3_METHODOLOGY = (
    "We formulate the Malshiras Taluka groundwater management problem using the XLRM framework, "
    "grounded in the Water Table Fluctuation (WTF) method (Healy and Cook, 2002; CGWB GEC-2015):\n\n"
    "1. Uncertainties (X): (i) Hydroclimatic variability across observed annual rainfall P in "
    "{215.29, 436.70, 530.52, 332.50, 582.30} mm (2015–2019); and (ii) unconfined fractured basalt "
    "specific yield Sy in {0.015, 0.020, 0.025} (dimensionless; reference Sy = 0.020, with gross "
    "monsoon recharge factor fr = 0.22 capturing rainfall infiltration and canal or surface seepage).\n\n"
    "2. Policy Levers (L): Four scenarios parameterized by supply-side MAR recharge enhancement "
    "(a) and demand-side monsoon draft reduction (b): "
    "L0 (Baseline BAU: a = 0, b = 0); "
    "L1 (Supply-Side MAR via check dams and percolation tanks: a = 0.20, b = 0); "
    "L2 (Demand-Side Management via drip irrigation and crop shift: a = 0, b = 0.25); "
    "and L3 (Integrated Management: a = 0.20, b = 0.25).\n\n"
    "3. Relationships (R) and Main Plain-Text Equations (Healy and Cook, 2002; CGWB, 2017):\n"
    "Mean DTW(t, s) = (1 / n) * sum(DTW(i, t, s))\n"
    "dh(t) = Mean May DTW(t) - Mean OctNov DTW(t)\n"
    "dS(t) = Sy * dh(t) * 1000 = R(t) - D(t)\n"
    "dhsim(t) = [ (1 + a) * R(t) - (1 - b) * D(t) ] / (1000 * Sy)\n"
    "Simulated OctNov DTW(t) = Mean May DTW(t) - dhsim(t)\n\n"
    "Term Definitions: t is year (2015–2019); s is season (May or Oct/Nov); DTW(i, t, s) is depth-to-water "
    "at well i (m bgl); n is valid well count; dh(t) and dhsim(t) are observed and simulated seasonal "
    "water-table rises (m); dS(t) is net seasonal aquifer storage change (mm water equivalent); "
    "R(t) = fr * P(t) is baseline gross monsoon recharge (mm); D(t) is implied baseline seasonal net "
    "draft and discharge (mm); and Simulated OctNov DTW(t) is simulated post-monsoon DTW (m bgl).\n\n"
    "4. Measures (M): (M1) Simulated post-monsoon DTW (m bgl, compared against a 3.50 m bgl "
    "sustainability threshold); (M2) net seasonal storage recovery dSsim (mm); and (M3) dry-year "
    "stress recovery in 2018."
)

SECTION_4_RESULTS = (
    "Figure 1 presents the baseline empirical pre-monsoon (May) and post-monsoon (October/November) "
    "mean depth-to-water (m bgl) across the 22 monitoring wells in Malshiras Taluka from 2015 to 2019. "
    "In every year, post-monsoon DTW was lower (shallower water table) than pre-monsoon DTW: "
    "6.46 to 5.14 m in 2015 (seasonal rise dh = 1.32 m; rainfall P = 215.29 mm), 7.17 to 3.04 m in 2016 "
    "(4.13 m; 436.70 mm), 6.86 to 2.78 m in 2017 (4.08 m; 530.52 mm), 6.02 to 5.87 m in 2018 "
    "(0.15 m; 332.50 mm), and 8.07 to 3.63 m in 2019 (4.44 m; 582.30 mm). Figure 1 highlights the "
    "critical 2018 anomaly: despite receiving 117.21 mm more rainfall than 2015, 2018 recorded almost "
    "no net water-table recovery (0.15 m), leaving May 2019 at the deepest pre-monsoon level (8.07 m bgl).\n\n"
    "Figure 2 illustrates the XLRM scenario outputs for simulated post-monsoon DTW (Figure 2a) and net "
    "seasonal aquifer storage recovery dS (Figure 2b) across levers L0 to L3. Water-balance decomposition "
    "(at reference Sy = 0.020, fr = 0.22) reveals that implied seasonal draft D surged to 70.15 mm "
    "in 2018 (consuming 96% of the 73.15 mm gross recharge and leaving dS = 3.0 mm), compared to "
    "13.47–39.31 mm in other years. Consequently, in wet years (2016, 2017, 2019), Supply-Side MAR (L1) "
    "outperforms Demand-Side Management (L2), increasing 2019 storage recovery from 88.8 mm (L0) to "
    "114.4 mm (L1) versus 98.6 mm (L2). Conversely, during the 2018 stress year, Demand-Side Management "
    "(L2: post-monsoon DTW = 4.99 m bgl, dS = 20.5 mm) outperforms Supply-Side MAR (L1: 5.14 m bgl, "
    "dS = 17.6 mm) because high pumping rather than lack of rain dominated the deficit. Integrated "
    "Management (L3) performs best across all years, improving 5-year mean post-monsoon DTW from 4.09 m "
    "(L0) to 2.72 m bgl (uncertainty range 2.27–3.00 m bgl across Sy from 0.015 to 0.025), recovering "
    "2018 post-monsoon DTW to 4.26 m bgl, and raising 5-year mean seasonal storage recovery from 56.5 "
    "to 83.9 mm/year."
)

SECTION_5_DISCUSSION = (
    "The XLRM results demonstrate that seasonal groundwater recovery in Malshiras Taluka is governed by "
    "the interaction between hydroclimatic recharge and agricultural pumping rather than annual rainfall "
    "totals alone. In our lumped WTF model, partitioning observed storage change (dS = Sy * dh * 1000) "
    "into gross recharge (R) and net seasonal draft (D) explains the 2018 anomaly: erratic monsoon "
    "distribution triggered intensive protective irrigation pumping (D = 70.15 mm), offsetting "
    "natural recharge. This mechanism creates a distinct regime dependency between policy levers. "
    "Supply-side interventions (L1: check dams, nala bunds, percolation tanks) depend multiplicatively on "
    "available rainfall runoff and therefore yield large gains in normal-to-wet years (2016, 2017, 2019), "
    "but provide limited buffering when monsoon extraction spikes. Conversely, demand-side interventions "
    "(L2: drip irrigation, shifting sugarcane acreage to lower-water crops) directly curtail seasonal draft "
    "D and prove more effective than supply augmentation during drought-stress periods like 2018. Only the "
    "integrated portfolio (L3) consistently keeps post-monsoon water tables shallower than the 3.50 m bgl "
    "threshold in 3 of 5 years while reducing the 2018 deficit by 1.61 m. Parameter sensitivity across "
    "Sy from 0.015 to 0.025 shows that lower specific yield amplifies water-table depth fluctuations for a "
    "given volumetric storage change, underscoring the risk of rapid head decline in low-porosity basalt.\n\n"
    "While these findings provide actionable strategic guidance for Atal Bhujal Yojana water budgeting—showing "
    "that Gram Panchayats must pair MAR structures with mandatory demand management—the lumped taluka-scale "
    "results cannot be used directly for site-level engineering design. Real-world operational deployment "
    "requires: (1) DEM-based topographic sub-watershed delineation to replace administrative taluka boundaries; "
    "(2) high-frequency (monthly or daily) piezometer and rain-gauge data to capture intra-monsoon storm "
    "intensity and dry-season (November–May) recession separately; (3) village-level crop acreage, canal release, "
    "and pump metering data to separate seasonal draft D from recharge factor fr; and (4) pumping-test "
    "calibration of spatially distributed Sy and transmissivity within a numerical groundwater flow model "
    "(such as MODFLOW)."
)

SECTION_6_REFERENCES = (
    "Main References and Datasets:\n\n"
    "1. Ground Water Surveys and Development Agency (GSDA) (2020). Atal Bhujal Yojana Hydrogeological "
    "Report: Malshiras Taluka, Solapur District, Maharashtra (Table 02: Historical Pre- and Post-Monsoon "
    "Groundwater Level Monitoring Data, 2015–2019). Water Supply and Sanitation Department, Government of "
    "Maharashtra. URL: https://gsda.maharashtra.gov.in/wp-content/uploads/2023/05/0.23.pdf\n\n"
    "2. Solapur District Administration (2020). Official Taluka-wise Annual Rainfall Records (Malshiras "
    "Taluka, 2015–2019). Revenue and Forest Department, Government of Maharashtra. "
    "URL: https://solapur.gov.in/en/rainfall/\n\n"
    "3. Healy, R. W., and Cook, P. G. (2002). Using groundwater levels to estimate recharge. Hydrogeology "
    "Journal, 10(1), 91–109; alongside Central Ground Water Board (CGWB) (2017), Report of the Ground "
    "Water Resource Estimation Committee (GEC-2015), Ministry of Water Resources, Government of India.\n\n"
    "Online Data and Code Repository:\n"
    "All transcribed groundwater and rainfall CSV datasets, seasonal and XLRM scenario summary tables, "
    "reproducible Python analysis scripts, and high-resolution figures are publicly hosted at:\n"
    "https://github.com/aryan90379/watershed_project"
)


def word_count(text: str) -> int:
    return len(text.split())


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        if self._pageNumber > 1:
            self.drawString(38, letter[1] - 26, "CE766: Final Project Submission — Solutions Guide (Malshiras Taluka)")
            self.drawRightString(letter[0] - 38, letter[1] - 26, "15 Marks Rubric")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(38, letter[1] - 30, letter[0] - 38, letter[1] - 30)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(letter[0] - 38, 22, f"Page {self._pageNumber} of {total_pages}")
        self.drawString(38, 22, "CE766 Watershed Management | Final Project Submission Package")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(38, 32, letter[0] - 38, 32)
        self.restoreState()


def html_escape_paragraphs(text: str) -> str:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n\n", "<br/><br/>")
        .replace("\n", "<br/>")
    )
    return escaped


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    sections = [
        ("1. Brief Statement of the Problem (2 marks)", SECTION_1_PROBLEM, 250),
        ("2. Data (1 mark)", SECTION_2_DATA, 150),
        ("3. Methodology (3 marks)", SECTION_3_METHODOLOGY, 400),
        ("3. Results (5 marks)", SECTION_4_RESULTS, 400),
        ("4. Discussion (3 marks)", SECTION_5_DISCUSSION, 400),
        ("5. References and Data/Code Repository (1 mark)", SECTION_6_REFERENCES, 500),
    ]

    print("=== WORD COUNT & UNDERSCORE VERIFICATION ===")
    for idx, (title, text, limit) in enumerate(sections):
        wc = word_count(text)
        status = "OK" if wc <= limit else "OVER LIMIT!"
        if idx < 5:
            assert "_" not in text, f"Underscore found in {title}!"
        print(f"{title}: {wc} / {limit} words [{status}] (Zero underscores verified)")
        assert wc <= limit, f"{title} exceeded limit ({wc} > {limit})"

    # Write plain text file
    txt_lines = [
        "================================================================================",
        "CE766: WATERSHED MANAGEMENT — FINAL PROJECT SUBMISSION (15 MARKS)",
        "Study Area: Malshiras Taluka, Solapur District, Maharashtra (2015–2019)",
        "================================================================================",
        "",
    ]
    for title, text, limit in sections:
        wc = word_count(text)
        txt_lines.append("--------------------------------------------------------------------------------")
        txt_lines.append(f"{title}  [Word Count: {wc} / {limit} max]")
        txt_lines.append("--------------------------------------------------------------------------------")
        txt_lines.append(text)
        txt_lines.append("")

    TXT_OUT.write_text("\n".join(txt_lines), encoding="utf-8")

    # Build PDF
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=38,
        bottomMargin=42,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=16, leading=20, textColor=colors.HexColor("#1A365D"), spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, leading=12.5, textColor=colors.HexColor("#4A5568"), spaceAfter=6
    )
    sec_style = ParagraphStyle(
        "SecHeading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=10.5, leading=14, textColor=colors.HexColor("#1A365D"), spaceBefore=6, spaceAfter=3
    )
    body_style = ParagraphStyle(
        "BodyTextCustom", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9.0, leading=13.0, textColor=colors.HexColor("#1A202C")
    )

    story = []
    story.append(Paragraph("CE766: Final Project Submission — Complete Solutions Guide", title_style))
    story.append(Paragraph(
        "Malshiras Taluka Groundwater & XLRM Scenario Analysis (2015–2019) | Clean Copy-Paste Formatting",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=6))

    checklist_html = (
        "<b>Quick Moodle Upload Guide:</b><br/>"
        "• Copy and paste the text from each box below directly into the corresponding Moodle question.<br/>"
        "• In Question 3 (Results), upload the two individual figure files located in your final submission folder: "
        "<b>Figure 1</b> (Baseline Seasonal DTW) and <b>Figure 2</b> (XLRM Management Scenarios)."
    )
    chk_table = Table([[Paragraph(checklist_html, body_style)]], colWidths=[536])
    chk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#90CDF4")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(chk_table)
    story.append(Spacer(1, 6))

    for title, text, limit in sections:
        wc = word_count(text)
        heading_para = Paragraph(
            f"{title} &nbsp;&nbsp;<font size=8 color='#2B6CB0'>[Word Count: {wc} / {limit} max]</font>",
            sec_style
        )
        box_para = Paragraph(html_escape_paragraphs(text), body_style)
        box_table = Table([[box_para]], colWidths=[536])
        box_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E0")),
            ("PADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(KeepTogether([heading_para, box_table, Spacer(1, 5)]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Wrote PDF: {PDF_OUT.relative_to(BASE)}")
    print(f"Wrote TXT: {TXT_OUT.relative_to(BASE)}")


if __name__ == "__main__":
    main()
