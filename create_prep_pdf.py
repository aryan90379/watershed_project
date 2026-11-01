from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that adds clean header & footer with 'Page X of Y' on all pages."""
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#718096'))
        
        # Header (on page 2)
        if self._pageNumber > 1:
            self.drawString(40, letter[1] - 30, "CE766: Watershed Hydrology & Management | Project Review Guide")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 34, letter[0] - 40, letter[1] - 34)

        # Footer
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(letter[0] - 40, 24, footer_text)
        self.drawString(40, 24, "Department of Civil Engineering | Groundwater Preliminary Analysis")
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.5)
        self.line(40, 34, letter[0] - 40, 34)
        
        self.restoreState()


def build_pdf():
    pdf_path = Path("CE766_Quiz_Prep_Guide.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Typography styles
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
        leading=13,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=6,
        spaceAfter=5
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#1A202C')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#2D3748')
    )

    trap_style = ParagraphStyle(
        'TrapStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#C53030')
    )

    highlight_box_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1A365D')
    )

    story = []

    # Title Banner
    story.append(Paragraph("CE766: Watershed Management & Groundwater Analysis", title_style))
    story.append(Paragraph("Conceptual Project Review & Quick Quiz Prep | Malshiras Taluka (2015–2019)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=8))

    # Section 1: The 30-Second Elevator Pitch
    story.append(Paragraph("1. The 30-Second Pitch (If asked: <i>\"Tell me what you did in your project\"</i>)", h2_style))
    pitch_text = (
        "<b>\"We collected 5 years (2015–2019) of pre-monsoon and post-monsoon water level records from 22 government monitoring "
        "wells in Malshiras Taluka, alongside annual rainfall data. Using an automated Python script, we computed the mean seasonal "
        "water table rise and analyzed recharge behavior. This establishes the empirical baseline needed before carrying out "
        "sub-watershed delineation and numerical groundwater modeling.\"</b>"
    )
    pitch_table = Table([[Paragraph(pitch_text, highlight_box_style)]], colWidths=[532])
    pitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF8FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BEE3F8')),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(pitch_table)
    story.append(Spacer(1, 8))

    # Section 2: Core Concept Questions
    story.append(Paragraph("2. The 5 Classic \"Do You Know What You Did?\" Conceptual Questions", h2_style))

    q1_q3 = [
        (
            "Q1: If Depth-to-Water decreases from 7 m to 3 m, did the water table rise or fall?",
            "Common Trap: People instinctively assume 'number decreased = water level decreased'.",
            "The Right Answer: The water table ROSE. Depth-to-water (DTW) measures depth from the ground surface down to the water level. A smaller depth means the water level is closer to the surface (aquifer recharge occurred)."
        ),
        (
            "Q2: Why specifically compare May and October/November?",
            "Key Concept: Captures the maximum seasonal fluctuation cycle.",
            "The Right Answer: May is the pre-monsoon baseline (driest period, deepest water table after summer extraction). October/November is the post-monsoon peak (recharge complete). The difference gives the net seasonal water table recovery."
        ),
        (
            "Q3: Did higher annual rainfall always result in a bigger water table rise?",
            "Key Concept: Rainfall alone does NOT dictate groundwater dynamics.",
            "The Right Answer: No! In 2018, rainfall was moderate (332.5 mm, well above 2015's 215.3 mm), yet the seasonal rise was almost zero (only 0.15 m). Agricultural pumping/draft, dry antecedent soil moisture, and rainfall distribution strongly control how much rain actually recharges the aquifer."
        )
    ]

    for q_text, trap, ans in q1_q3:
        box_content = [
            Paragraph(f"<b>{q_text}</b>", q_title_style),
            Spacer(1, 2),
            Paragraph(f"<b>⚠️ Trap / Concept:</b> {trap}", trap_style),
            Spacer(1, 2),
            Paragraph(f"<b>✓ Correct Answer:</b> {ans}", body_style)
        ]
        q_table = Table([[box_content]], colWidths=[532])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 5))

    # Clean Page Break so Page 2 starts with Q4 and Q5 followed by Fast Facts & Formulas
    story.append(PageBreak())

    q4_q5 = [
        (
            "Q4: How were missing well readings handled? Why not replace them with 0?",
            "Key Concept: Avoiding severe data pipeline distortion.",
            "The Right Answer: Missing entries were retained as null/blank and excluded from each season's average (valid well count n varied between 19 and 21). Setting missing entries to 0 would falsely imply water at ground surface (flooding/artesian spring), completely skewing the statistics."
        ),
        (
            "Q5: Is this current analysis a calibrated groundwater model?",
            "Key Concept: Distinguishing preliminary empirical analysis from numerical simulation.",
            "The Right Answer: No. This is a descriptive statistical baseline. A true groundwater model requires: (1) delineating the topographic sub-watershed ridge boundary, (2) estimating aquifer properties (Specific Yield Sy, hydraulic conductivity K), (3) quantifying draft/pumping, and (4) running numerical flow simulations (e.g., MODFLOW)."
        )
    ]

    for q_text, trap, ans in q4_q5:
        box_content = [
            Paragraph(f"<b>{q_text}</b>", q_title_style),
            Spacer(1, 2),
            Paragraph(f"<b>⚠️ Trap / Concept:</b> {trap}", trap_style),
            Spacer(1, 2),
            Paragraph(f"<b>✓ Correct Answer:</b> {ans}", body_style)
        ]
        q_table = Table([[box_content]], colWidths=[532])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Fast Facts & Core Equations Reference", h2_style))

    table_data = [
        [Paragraph("<b>Study Area</b>", body_style), Paragraph("Malshiras Taluka, Solapur District, Maharashtra (Rain-shadow semi-arid zone)", body_style)],
        [Paragraph("<b>Monitoring Wells</b>", body_style), Paragraph("22 wells total: 14 monitored by GSDA (State) + 8 by CGWB (Central Govt)", body_style)],
        [Paragraph("<b>Primary Equation 1</b>", body_style), Paragraph("Mean_DTW(year, season) = (Sum of valid well DTW readings) / (Valid wells count n)", body_style)],
        [Paragraph("<b>Primary Equation 2</b>", body_style), Paragraph("Seasonal_Rise = Mean_DTW_May - Mean_DTW_OctNov  (Positive difference = shallower table)", body_style)],
        [Paragraph("<b>Storage Caveat</b>", body_style), Paragraph("DTW is NOT volumetric storage. Storage change ΔS requires: ΔS = Area × Specific Yield (Sy) × Δh", body_style)],
        [Paragraph("<b>Project Repository</b>", body_style), Paragraph("Clean Python pipeline on GitHub: <u>github.com/aryan90379/watershed_project</u>", body_style)],
    ]

    facts_table = Table(table_data, colWidths=[130, 402])
    facts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(facts_table)
    story.append(Spacer(1, 10))

    # Final Takeaway Card
    takeaway_header = ParagraphStyle('THead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#744210'))
    takeaway_body = ParagraphStyle('TBody', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#744210'))
    
    card_content = [
        Paragraph("<b>Golden Rule for Tomorrow's Discussion:</b>", takeaway_header),
        Spacer(1, 3),
        Paragraph(
            "\"We compared the driest month (May) against the post-monsoon peak (Oct/Nov) over 5 years to measure "
            "seasonal aquifer recharge, discovering that rainfall alone does not explain water table recovery—groundwater "
            "extraction, agricultural demand, and soil moisture conditions play an equally dominant role.\"",
            takeaway_body
        )
    ]
    takeaway_table = Table([[card_content]], colWidths=[532])
    takeaway_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEFCBF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#ECC94B')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(takeaway_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF successfully updated:", pdf_path.resolve())

if __name__ == "__main__":
    build_pdf()
