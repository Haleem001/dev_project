
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import AdoptionRequest
# utils.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_adoption_pdf(adoption_request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        leading=15,
        spaceAfter=15
    )
    
    elements.append(Spacer(1, 12))
    
    title = Paragraph("Adoption Approval Certificate", title_style)
    elements.append(title)
    elements.append(Spacer(1, 24))
    
    full_name = f"{adoption_request.user.first_name} {adoption_request.user.last_name}"
    child_name = f"Child: {adoption_request.child.name}"
    adopter_name = f"Adopted by: {full_name}"
    approval_date = f"Date of Approval: {adoption_request.approved_date.strftime('%Y-%m-%d')}"
    thank_you_note = "Thank you for providing a loving home."
    
    elements.append(Paragraph(child_name, normal_style))
    elements.append(Paragraph(adopter_name, normal_style))
    elements.append(Paragraph(approval_date, normal_style))
    elements.append(Paragraph(thank_you_note, normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


# utils.py



def send_adoption_approval_email(adoption_request):
    pdf_buffer = generate_adoption_pdf(adoption_request)
    full_name = f"{adoption_request.user.first_name} {adoption_request.user.last_name}"
    email = EmailMessage(
        'Adoption Approval Certificate',
        f'Dear {full_name},\n\nCongratulations! Your adoption request has been approved. Please find attached the adoption approval certificate for your recent adoption.',
        'your_email@gmail.com',
        [adoption_request.user.email],
    )
    email.attach('Adoption_Approval_Certificate.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send()

def send_adoption_rejection_email(adoption_request):
    full_name = f"{adoption_request.user.first_name} {adoption_request.user.last_name}"
    email = EmailMessage(
        'Adoption Request Update',
        f'Dear {full_name},\n\nWe regret to inform you that your adoption request has been rejected. Please contact us for further details.',
        'your_email@gmail.com',
        [adoption_request.user.email],
    )
    email.send()
