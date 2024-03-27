import array
import time
# from fpdf.fpdf import _Format, _Orientation
# from fpdf.util import _Unit

import requests
from fpdf import FPDF
# from dashboard.models import Admission
# from dashboard.models import Admission

from gtccore import settings


class PDF(FPDF):
    '''Custom PDF class.'''
    def header(self):
        # Rendering logo:
        logo = "gtccore\library\gimpa-round-logo.jpg"
        self.image(logo, x=10, y=10, w=20)  # Adjust the position and size of the logo as needed
        # Setting font: helvetica bold 15
        self.set_font("Helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Gimpa Training & Consulting", align="C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("Helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_admission_letter(admission):
    '''Generates an admission letter for the specified admission.'''
    print(f"Value of admission from generate_admission_letter: {admission}")
    # values
    applicant_name = admission.application.name if admission.application else "John Doe"
    applicant_email = admission.application.email if admission.application else "john@gmail.com"
    applicant_phone = admission.application.phone if admission.application else "0240000000"
    program_name = admission.application.course.title if admission.application else "Course Name"
    program_fee = admission.application.course.price if admission.application else "1000"
    admission_id = admission.application.application_id if admission.application else "AD12345"

    # Create a PDF object
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Set up the document
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Admission Letter", ln=True, align="C")

    # Set font and size for the content
    pdf.set_font('Arial', '', 12)

    # Add the date
    pdf.cell(0, 10, f"Date: {time.strftime('%d %B %Y')}", ln=True, align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the recipient's address
    pdf.cell(0, 10, applicant_name, ln=True, align='L')
    pdf.cell(0, 10, applicant_email, ln=True, align='L')
    pdf.cell(0, 10, applicant_phone, ln=True, align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the salutation
    pdf.multi_cell(0, 10, f'Dear {applicant_name},', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the body of the letter
    pdf.multi_cell(0, 10, 'We are pleased to inform you that you have been admitted to Gimpa Training and Consulting short professional courses.', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add program details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Program: {program_name}', ln=True, align='L')
    # pdf.set_font('Arial', '', 12)
    # pdf.cell(0, 10, 'Course Name', ln=True, align='L')

    # Add fee details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Fees: GHC{program_fee}', ln=True, align='L')
    # pdf.set_font('Arial', '', 12)
    # pdf.cell(0, 10, 'USD 1000', ln=True, align='L')

    # Add admission ID
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Admission ID: {admission_id}', ln=True, align='L')
    # pdf.set_font('Arial', '', 12)
    # pdf.cell(0, 10, 'AD12345', ln=True, align='L')

     # Add administrator's signature (as an image)
    signature_image = "gtccore\library\signature.png"  # Replace with the actual path to the administrator's signature image
    pdf.image(signature_image, x=10, y=pdf.get_y() + 10, w=30)  # Adjust the position and size of the signature image as needed

    # Add a blank line
    pdf.ln(30)

    # Add the closing
    pdf.multi_cell(0, 10, 'Sincerely, \nProf. Charles Teye Amoatey\nDirector, GTC', align='L')


    return pdf


def send_sms(sender: str, message: str, recipients: array.array):
    '''Sends an SMS to the specified recipients'''
    header = {"api-key": settings.ARKESEL_API_KEY, 'Content-Type': 'application/json',
              'Accept': 'application/json'}
    SEND_SMS_URL = "https://sms.arkesel.com/api/v2/sms/send"
    payload = {
        "sender": sender,
        "message": message,
        "recipients": recipients
    } 
    try:
        response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    except Exception as e:
        print(f"Error: {e}")
        return False
    else:
        print(response.json())
        return response.json()