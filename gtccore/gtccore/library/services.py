
from fpdf import FPDF

def generate_admission_letter():
    # Create a PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set up the document
    pdf.set_title('Admission Letter')

    # Set font and size for the letterhead
    pdf.set_font('Arial', 'B', 16)

    # Add the letterhead
    pdf.cell(0, 20, 'University of Example', ln=True, align='C')

    # Set font and size for the content
    pdf.set_font('Arial', '', 12)

    # Add the date
    pdf.cell(0, 10, 'Date: November 25, 2023', ln=True, align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the recipient's address
    pdf.multi_cell(0, 10, 'John Doe', align='L')
    pdf.multi_cell(0, 10, '123 Main Street', align='L')
    pdf.multi_cell(0, 10, 'Anytown, USA', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the salutation
    pdf.multi_cell(0, 10, 'Dear John Doe,', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the body of the letter
    pdf.multi_cell(0, 10, 'We are pleased to inform you that you have been admitted to the University of Example for the upcoming semester.', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the closing
    pdf.multi_cell(0, 10, 'Congratulations once again!', align='L')

    # Add a blank line
    pdf.ln(10)

    # Add the signature
    pdf.multi_cell(0, 10, 'Sincerely,', align='L')

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
    response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    print(response.json())
    return response.json()