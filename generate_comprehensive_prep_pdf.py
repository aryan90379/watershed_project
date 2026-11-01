from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with Page X of Y on every page."""
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
        self.setFillColor(colors.HexColor('#4A5568'))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, letter[1] - 28, "CE766: WATERSHED MANAGEMENT & HYDROLOGY — GENERAL EXAM & QUIZ GUIDE")
            self.drawRightString(letter[0] - 40, letter[1] - 28, "MASTER CONCEPT SHEET")
            self.setStrokeColor(colors.HexColor('#CBD5E0'))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 32, letter[0] - 40, letter[1] - 32)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#718096'))
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(letter[0] - 40, 22, footer_text)
        self.drawString(40, 22, "CE766 Core Evaluation Rubric: Modeling, Equations, Interventions, Uncertainties & Methodology")
        self.setStrokeColor(colors.HexColor('#CBD5E0'))
        self.setLineWidth(0.5)
        self.line(40, 32, letter[0] - 40, 32)
        
        self.restoreState()


def build_pdf():
    pdf_path = Path("CE766_Master_Quiz_Preparation_Guide.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=38,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=6
    )

    h1_section_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=8,
        spaceAfter=4
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2D3748')
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1A202C')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#805AD5')
    )

    table_header_style = ParagraphStyle(
        'THeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1A365D')
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2C5282')
    )

    story = []

    # =========================================================================
    # PAGE 1: Course Rubric Overview & Model Identification / Equations
    # =========================================================================
    story.append(Paragraph("CE766: Watershed Management & Hydrology", title_style))
    story.append(Paragraph("Master Quiz & Evaluation Reference Guide — General Course Concepts & Rubric Answers", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=6))

    # Banner Explaining the Quiz Purpose
    rubric_intro = (
        "<b>How to use this guide:</b> The quiz tests your foundational grasp of <b>watershed hydrology concepts</b> "
        "and the <b>standard project evaluation rubric</b> (Model Identification, Governing Equations, Temporal/Spatial "
        "Resolution, Baseline vs. Interventions, Performance Measures, Uncertainties, and Implementation Challenges). "
        "Use these structured explanations to answer both general conceptual questions and site-specific queries."
    )
    intro_table = Table([[Paragraph(rubric_intro, body_style)]], colWidths=[536])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 6))

    # 1. MODEL IDENTIFICATION & RESOLUTION JUSTIFICATION
    story.append(Paragraph("1. Model Identification & Justification of Terms (Rubric Question 1)", h1_section_style))

    model_concepts = [
        [
            Paragraph("<b>Concept / Question</b>", table_header_style),
            Paragraph("<b>General Hydrological Justification & Core Principle</b>", table_header_style),
            Paragraph("<b>Project Example</b>", table_header_style)
        ],
        [
            Paragraph("<b>Model Type: Empirical / Statistical vs. Physical / Numerical</b>", bold_body),
            Paragraph("• <i>Empirical/Statistical:</i> Uses observed relationships (e.g., rainfall vs water level rise). Fast, data-driven, needs few spatial parameters.<br/>"
                      "• <i>Physical/Numerical:</i> Solves partial differential flow equations (e.g., Darcy's Law in MODFLOW). Simulates spatial flow gradients and boundary conditions.", body_style),
            Paragraph("Preliminary work uses statistical/water-table-fluctuation analysis. Full numerical modeling is future scope.", body_style)
        ],
        [
            Paragraph("<b>Choice of Spatial Resolution</b>", bold_body),
            Paragraph("• <i>Lumped:</i> Treats an entire catchment/taluka as a single homogeneous unit. Suitable for preliminary regional assessments.<br/>"
                      "• <i>Semi-Distributed / Distributed:</i> Divides watershed into sub-basins or grid cells based on DEM ridges, land use, and soil types.", body_style),
            Paragraph("Currently lumped at taluka level due to data availability; must transition to DEM-delineated sub-watersheds.", body_style)
        ],
        [
            Paragraph("<b>Choice of Temporal Resolution</b>", bold_body),
            Paragraph("• <i>Annual:</i> Hides all seasonal variability.<br/>"
                      "• <i>Seasonal (Pre vs Post Monsoon):</i> Standard in monsoon climates to isolate seasonal net recharge vs dry season extraction.<br/>"
                      "• <i>Daily/Monthly:</i> Needed for event-based flood routing or dynamic pumping simulations.", body_style),
            Paragraph("Seasonal resolution (May vs Oct/Nov) isolates the monsoon recharge signal from dry-season draft.", body_style)
        ]
    ]
    t_model = Table(model_concepts, colWidths=[120, 280, 136])
    t_model.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_model)
    story.append(Spacer(1, 6))

    # 2. GOVERNING HYDROLOGICAL & GROUNDWATER EQUATIONS
    story.append(Paragraph("2. Governing Equations: Hydrological & Groundwater Balance (Rubric Question 2)", h1_section_style))

    eq_intro = (
        "<b>A. General Watershed Water Balance (Catchment Scale):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P = Q + ET + ΔS_soil + ΔS_gw</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>P (Precipitation):</b> Total rainfall volume input.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Q (Surface Runoff / Streamflow):</b> Water exiting the watershed boundary via stream channels.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>ET (Evapotranspiration):</b> Water returned to the atmosphere from open water, soil, and plant transpiration.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>ΔS_soil & ΔS_gw:</b> Changes in soil moisture storage and saturated groundwater storage.<br/><br/>"
        "<b>B. Groundwater Balance / Water Table Fluctuation (WTF) Equation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Recharge - Draft = ΔS_gw = Area × Specific Yield (S_y) × Δh</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Recharge (Input):</b> Rainfall infiltration + irrigation return flows + canal seepage + recharge structures.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Draft (Output):</b> Agricultural tubewell pumping + domestic extraction + natural baseflow discharge to streams.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Specific Yield (S_y):</b> Dimensionless ratio of water volume released by gravity per unit aquifer volume (typically 0.01–0.03 for hard basalt; 0.10–0.25 for unconfined sand).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Δh (Water Table Fluctuation):</b> Mean_DTW_May - Mean_DTW_OctNov (seasonal rise in water level)."
    )
    eq_table = Table([[Paragraph(eq_intro, body_style)]], colWidths=[536])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(eq_table)

    # =========================================================================
    # PAGE 2: Baseline vs Interventions & Performance Measures
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("3. Baseline Conditions vs. Intervention Options (Rubric Question 3)", h1_section_style))

    interventions_data = [
        [
            Paragraph("<b>Category</b>", table_header_style),
            Paragraph("<b>Definition / Specific Options</b>", table_header_style),
            Paragraph("<b>Engineering & Hydrological Justification</b>", table_header_style)
        ],
        [
            Paragraph("<b>Baseline Conditions</b>", bold_body),
            Paragraph("The existing, unmanaged watershed state (Business-as-Usual). Pre-intervention land use, traditional cropping, unmanaged pumping, natural runoff.", body_style),
            Paragraph("Provides the benchmark reference to quantify whether interventions produce a statistically significant positive impact.", body_style)
        ],
        [
            Paragraph("<b>Supply-Side Interventions (Water Harvesting)</b>", bold_body),
            Paragraph("<b>1. Continuous Contour Trenches (CCT) & Bunds:</b> Along ridge lines.<br/>"
                      "<b>2. Check Dams & Nala Bunds:</b> On 1st–3rd order streams.<br/>"
                      "<b>3. Percolation Tanks:</b> In permeable foothill zones.<br/>"
                      "<b>4. Farm Ponds (Shettale):</b> Field-level runoff storage.", body_style),
            Paragraph("Follows the <b>'Ridge-to-Valley' principle</b>: slows down runoff velocity, reduces soil erosion, increases time-of-concentration, and maximizes groundwater percolation into aquifers.", body_style)
        ],
        [
            Paragraph("<b>Demand-Side Interventions (Water Budgeting)</b>", bold_body),
            Paragraph("<b>1. Micro-irrigation:</b> Drip and sprinkler systems.<br/>"
                      "<b>2. Crop Diversification:</b> Replacing water-guzzling crops (e.g., sugarcane) with pulses, millets, or oilseeds.<br/>"
                      "<b>3. Mulching & Deficit Irrigation:</b> Minimizing evaporative loss.", body_style),
            Paragraph("In semi-arid hard-rock regions, supply measures alone cannot offset overdraft. Demand management directly curtails agricultural draft, maintaining long-term water table sustainability.", body_style)
        ]
    ]
    t_interv = Table(interventions_data, colWidths=[115, 235, 186])
    t_interv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_interv)
    story.append(Spacer(1, 8))

    # 4. IDENTIFICATION OF MEASURES (PERFORMANCE METRICS)
    story.append(Paragraph("4. Performance Measures / Indicators of Success (Rubric Question 4)", h1_section_style))

    measures_data = [
        [
            Paragraph("<b>Performance Metric</b>", table_header_style),
            Paragraph("<b>Measurement Unit & Formula</b>", table_header_style),
            Paragraph("<b>Target Direction / Success Criterion</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Depth-to-Water (DTW) Reduction</b>", bold_body),
            Paragraph("Metres below ground level (m bgl). Monitored at observation wells.", body_style),
            Paragraph("<b>Decrease in DTW</b> (water table rises closer to surface; post-monsoon DTW should ideally stay within 2–4 m bgl).", body_style)
        ],
        [
            Paragraph("<b>2. Volumetric Groundwater Recharge</b>", bold_body),
            Paragraph("Cubic metres (m³) or ha-m. Calculated via ΔS = Area × Specific Yield (Sy) × Δh.", body_style),
            Paragraph("<b>Increase in ΔS</b>; net positive annual storage balance after accounting for draft.", body_style)
        ],
        [
            Paragraph("<b>3. Runoff Coefficient ($C$)</b>", bold_body),
            Paragraph("Dimensionless ratio: $C = \text{Runoff Volume} / \text{Rainfall Volume}$.", body_style),
            Paragraph("<b>Reduction in $C$</b> (more rainfall is retained and infiltrated rather than lost as rapid surface runoff).", body_style)
        ],
        [
            Paragraph("<b>4. Water Productivity (Crop per Drop)</b>", bold_body),
            Paragraph("Crop yield per unit water applied ($kg/m^3$ or $₹/m^3$).", body_style),
            Paragraph("<b>Increase in productivity</b>, stabilizing farmer income even during below-normal rainfall years.", body_style)
        ]
    ]
    t_measures = Table(measures_data, colWidths=[130, 206, 200])
    t_measures.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_measures)

    # =========================================================================
    # PAGE 3: Uncertainties, Implementation Challenges & Universal Concepts
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("5. Identification of Uncertainties in Watershed Studies (Rubric Question 5)", h1_section_style))

    uncertainties_data = [
        [
            Paragraph("<b>Uncertainty Category</b>", table_header_style),
            Paragraph("<b>Physical / Methodological Cause</b>", table_header_style),
            Paragraph("<b>How to Mitigate in Watershed Studies</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Input Data Uncertainty</b>", bold_body),
            Paragraph("Rainfall varies significantly across space; using single taluka rain-gauge records introduces spatial interpolation error.", body_style),
            Paragraph("Use Thiessen Polygons, Isohyetal mapping, or satellite gridded rainfall (IMD / CHIRPS).", body_style)
        ],
        [
            Paragraph("<b>2. Hydrogeological Parameter Uncertainty</b>", bold_body),
            Paragraph("Hard-rock basalt aquifers have highly irregular fractures and weathered zones; Specific Yield ($S_y$) and permeability ($K$) vary widely.", body_style),
            Paragraph("Pumping tests, geophysical resistivity surveys (VES), and sensitivity analysis across $S_y$ ranges.", body_style)
        ],
        [
            Paragraph("<b>3. Groundwater Abstraction Uncertainty</b>", bold_body),
            Paragraph("Agricultural tube wells are unmetered. Pumping draft is usually estimated indirectly from electricity consumption or crop area.", body_style),
            Paragraph("Farmer sample surveys, remote-sensing crop evapotranspiration mapping, and participatory monitoring.", body_style)
        ],
        [
            Paragraph("<b>4. Boundary & Scale Uncertainty</b>", bold_body),
            Paragraph("Administrative boundaries (Taluka/District) do NOT coincide with hydrological watershed boundaries (ridgelines).", body_style),
            Paragraph("Delineate natural topographic catchment boundaries using GIS and Digital Elevation Models (DEMs).", body_style)
        ]
    ]
    t_uncert = Table(uncertainties_data, colWidths=[125, 215, 196])
    t_uncert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_uncert)
    story.append(Spacer(1, 8))

    # 6. IMPLEMENTATION CHALLENGES & DEVIATIONS
    story.append(Paragraph("6. Implementation Challenges & Methodological Deviations (Rubric Question 6)", h1_section_style))

    challenges_text = (
        "<b>When answering 'What challenges did you face?', state these standard watershed study bottlenecks:</b><br/>"
        "• <b>Temporal Gap:</b> Government monitoring stations only record twice a year (May & Oct/Nov), missing intra-monsoon recharge events and immediate post-storm responses.<br/>"
        "• <b>Missing Observation Records:</b> Some monitoring wells are dry, damaged, or omitted in certain cycles (hence sample count <i>n</i> varies; records must remain blank rather than zero).<br/>"
        "• <b>Spatial Data Mismatch:</b> Socioeconomic, agricultural, and rainfall data are reported at administrative taluka level, whereas hydrology follows drainage basins.<br/>"
        "• <b>Resolution of Crop Water Use:</b> High-resolution, seasonal, village-level crop acreage data is often missing or unverified, limiting exact draft calculations.<br/>"
        "• <b>Current Work Status:</b> Results represent a <b>descriptive baseline</b>; full model calibration and intervention simulation require calibrated boundary heads and recharge parameters."
    )
    t_chal = Table([[Paragraph(challenges_text, body_style)]], colWidths=[536])
    t_chal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_chal)
    story.append(Spacer(1, 8))

    # 7. UNIVERSAL QUIZ CHEAT-SHEET
    story.append(Paragraph("7. Quick Universal Concepts (Checklist for Fast Oral Questions)", h1_section_style))

    quick_checklist = [
        [
            Paragraph("<b>Question / Prompt</b>", table_header_style),
            Paragraph("<b>Instant 1-Sentence Answer to Give</b>", table_header_style)
        ],
        [
            Paragraph("<b>Does DTW decrease mean water level rose?</b>", bold_body),
            Paragraph("<b>YES.</b> DTW is depth from the surface; a smaller depth means the water table is shallower (closer to the ground).", body_style)
        ],
        [
            Paragraph("<b>Why not fill missing values with 0?</b>", bold_body),
            Paragraph("0 m bgl means water is standing on the ground surface (artesian spring/flooding), which destroys statistical validity.", body_style)
        ],
        [
            Paragraph("<b>Why compare May and Oct/Nov?</b>", bold_body),
            Paragraph("May is the pre-monsoon minimum; Oct/Nov is the post-monsoon peak. Their difference isolates net monsoon recharge.", body_style)
        ],
        [
            Paragraph("<b>Why didn't 2018 rise despite rainfall?</b>", bold_body),
            Paragraph("Rainfall alone doesn't dictate levels; high agricultural pumping, dry antecedent soil moisture, and rapid runoff consumed it.", body_style)
        ],
        [
            Paragraph("<b>How do you convert DTW to storage volume?</b>", bold_body),
            Paragraph("Multiply fluctuation Δh by the Aquifer Area (A) and Specific Yield (Sy): ΔS = A × Sy × Δh.", body_style)
        ],
        [
            Paragraph("<b>What is the Ridge-to-Valley principle?</b>", bold_body),
            Paragraph("Treat the upper catchment (ridges) first with contour trenches to reduce runoff velocity, then install storage structures in valleys.", body_style)
        ]
    ]
    t_quick = Table(quick_checklist, colWidths=[180, 356])
    t_quick.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EBF8FF')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_quick)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Master Guide PDF built successfully:", pdf_path.resolve())

if __name__ == "__main__":
    build_pdf()
