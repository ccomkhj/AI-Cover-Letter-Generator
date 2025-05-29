from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import re

def generate_cover_letter_pdf(cover_letter_text, name="Applicant"):
    """
    Generate a nicely formatted PDF for the cover letter.
    
    Args:
        cover_letter_text (str): The text content of the cover letter
        name (str): The name of the applicant
        
    Returns:
        BytesIO: A buffer containing the generated PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(
        name='Header',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.darkblue
    ))
    styles.add(ParagraphStyle(
        name='Signature',
        fontSize=12,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    # Document content will be stored in this list
    content = []
    
    # Parse the cover letter text to identify parts
    # Assume basic structure: greeting, body paragraphs, signature
    paragraphs = [p for p in re.split(r'\n\s*\n', cover_letter_text.strip()) if p.strip()]
    
    # Add current date at the top
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    content.append(Paragraph(today, styles['Normal']))
    content.append(Spacer(1, 0.2*inch))
    
    if paragraphs:
        # Identify greeting (assume it's the first paragraph and usually short)
        greeting = paragraphs[0]
        content.append(Paragraph(greeting, styles['Normal']))
        content.append(Spacer(1, 0.2*inch))
        
        # Body paragraphs (everything between greeting and signature)
        for para in paragraphs[1:-1]:
            content.append(Paragraph(para, styles['Justify']))
            content.append(Spacer(1, 0.2*inch))
        
        # Signature (assume it's the last paragraph)
        signature = paragraphs[-1]
        content.append(Paragraph(signature, styles['Signature']))
    else:
        # If parsing fails, just add the whole text
        content.append(Paragraph(cover_letter_text, styles['Justify']))
    
    # Build the PDF
    doc.build(content)
    buffer.seek(0)
    return buffer
