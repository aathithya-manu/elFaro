import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, send_file
from google.cloud import vision
from html import unescape
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from mailjet_rest import Client
from dotenv import load_dotenv
import io
import re

load_dotenv()
# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
vision_client = vision.ImageAnnotatorClient()

@app.route('/')
def home():
    """Renders the homepage for image upload."""
    return render_template("index.html", google_maps_api_key=os.getenv("google_maps_api_key"))

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    """Analyzes the uploaded image and generates a civic report."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    content = file.read()
    image = vision.Image(content=content)

    # Use Google Vision to get labels
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    label_descriptions = [label.description for label in labels]

    # Get location data from form
    location_address = request.form.get('location_address', '')
    latlng = request.form.get('location_latlng', '')

    location_info = ""
    if location_address:
        location_info = f"The reported issue is located at: {location_address} (Coordinates: {latlng}).\n"

    # Create the prompt
    prompt = f"""
You are a civic issue reporting assistant tasked with drafting formal complaint reports addressed to the appropriate Indian civic authority based on visual evidence.
Use the information below to write a concise, professional, and respectful civic complaint.If the labels {label_descriptions} do not show any relevance to any civic issue then Simply respond "The Uploaded Image is not clearly understandable.\nIf you are trying to upload any image relevant to any civic issue, try again with any different image from dfferent angle!\nDont try to Upload any image irrelevant to the scope of this webApp"

- Use a formal tone and structure suitable for government correspondence in India.
- Clearly identify and name the appropriate civic authority responsible for the issue, based on the location provided. Do not generically refer to "the concerned authority."
- Do not speculate about causes of the issue (e.g., construction, natural disasters) unless such causes are explicitly suggested by the labels.
- Do not use overly emotional or exaggerated language.
- End the report with the signature: "Sincerely,\nA Concerned Citizen"

---

Location Details:
{location_info}

Visual Evidence (Detected Labels):
{', '.join(label_descriptions)}

---

Based on the above, draft a formal civic complaint email/report.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    gemini_response = model.generate_content(prompt)
    raw_text = gemini_response.text

    # Clean HTML formatting
    clean_text = unescape(
        raw_text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    )

    email_prompt = f"""
    You are an AI assistant that helps identify the most appropriate civic authority and their email address to send a formal complaint to.

    Please do the following:
    - Based on the report below, determine which civic body or department should handle the issue (like municipal corporation, public works department, etc.).
    - Predict the *official email address* of that authority, based on the location mentioned in the report.
    - If unsure, provide the most likely official-sounding email (like commissioner.palakkad@kerala.gov.in or info@bbmp.gov.in).

    Return just the email in the format:
    Authority Email: <email_here>

    ---

    Civic Complaint Report:
    {clean_text}
    """

    email_response = model.generate_content(email_prompt)

    # Extract predicted email
    email_match = re.search(r'Authority Email:\s*([\w\.-]+@[\w\.-]+\.\w+)', email_response.text)
    authority_email = email_match.group(1) if email_match else ''


    return render_template(
        "index.html",
        google_maps_api_key=os.getenv("google_maps_api_key"),
        label=label_descriptions,
        report=clean_text,
        submitted=False,
        authority_email = authority_email
    )

@app.route('/submit_report', methods=['POST'])
def submit_report():
    """Handles the submission of the edited report."""
    edited_report = request.form.get('edited_report', '')
    authority_email = request.form.get('recipient_email', '') 
    
    # Render the template to show the final, submitted report
    return render_template(
        "index.html",
        google_maps_api_key=os.getenv("google_maps_api_key"), 
        report=edited_report, 
        submitted=True,
        labels=None, 
        authority_email = authority_email     # No need to show labels again on the final view
    )


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Generates and downloads the submitted report as a PDF
    report_text = request.form.get('report_to_download', '')
    
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Add a title
    title_style = styles['Title']
    story.append(Paragraph("Civic Report", title_style))
    story.append(Spacer(1, 12))
    
    # Add the report text
    report_style = styles['Normal']
    # Split the report by newlines and add each as a paragraph
    for line in report_text.split('\n'):
        story.append(Paragraph(line, report_style))
        story.append(Spacer(1, 6)) # Add a small spacer between lines
        
    doc.build(story)
    
    # Reset the buffer position to the beginning
    buffer.seek(0)
    
    # Return the PDF as a file attachment
    return send_file(buffer, as_attachment=True, download_name='civic_report.pdf', mimetype='application/pdf')

#MailJet Send Template
def send_email_with_mailjet(recipient, report):
    api_key = os.getenv('MAILJET_API_KEY')
    api_secret = os.getenv('MAILJET_API_SECRET')
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
      'Messages': [
        {
          "From": {
            "Email": "info@el-faro.tech",
            "Name": "El faro Admin"
          },
          "To": [
            {
              "Email": recipient,
              "Name": "Anonymous"
            }
          ],
          "Subject": "Regarding to a civic issue",
          "TextPart": report
        }
      ]
    }

    result = mailjet.send.create(data=data)
    return result.status_code == 200 or result.status_code == 201
@app.route('/send_email', methods=['POST'])
def send_email():
    #Sends the generated report to the given email address using Mailjet.

    recipient_email = request.form.get('recipient_email')
    report_text = request.form.get('report_to_send')

    if not recipient_email or not report_text:
        return jsonify({'error': 'Email address or report content missing'}), 400

    success = send_email_with_mailjet(recipient_email, report_text)


    if success:
        message = "✅ Email sent successfully to " + recipient_email
    else:
        message = "❌ Failed to send email. Please try again."

    return render_template(
        "index.html",
        google_maps_api_key=os.getenv("google_maps_api_key"), 
        report=report_text, 
        submitted=True,
        image_url=None,
        message=message
    )