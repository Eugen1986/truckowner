import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment
import base64
from werkzeug.datastructures import FileStorage

def send_document_submission_email(form_data, files):
    """
    Send document submission email via SendGrid
    
    Args:
        form_data: Dictionary containing form data
        files: Dictionary of uploaded files
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_key:
        print("SENDGRID_API_KEY not found in environment variables")
        return False
    
    sg = SendGridAPIClient(sendgrid_key)
    
    # Email content
    subject = "New Trucking Document Submission"
    from_email = Email("noreply@trucking-docs.com", "Trucking Document System")
    to_email = To(form_data.get('_replyto', 'admin@example.com'))
    
    # Create HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                New Driver Document Submission
            </h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">Personal Information</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold; width: 30%;">Full Name:</td>
                        <td style="padding: 8px;">{form_data.get('full_name', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Phone:</td>
                        <td style="padding: 8px;">{form_data.get('phone', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Email:</td>
                        <td style="padding: 8px;">{form_data.get('_replyto', 'N/A')}</td>
                    </tr>
                </table>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">Documents Submitted</h3>
                <ul style="list-style-type: none; padding: 0;">
    """
    
    # Add document list
    document_names = {
        'drivers_license': 'CDL Driver License',
        'medical_certificate': 'DOT Medical Certificate', 
        'social_security': 'Social Security Card',
        'vehicle_registration': 'Vehicle Registration',
        'insurance_certificate': 'Insurance Certificate',
        'ifta_permit': 'IFTA Permit',
        'mc_authority': 'MC Authority'
    }
    
    for field_name, display_name in document_names.items():
        file_obj = files.get(field_name)
        if file_obj and file_obj.filename:
            html_content += f'<li style="padding: 5px 0; border-bottom: 1px solid #ddd;"><strong>✓ {display_name}:</strong> {file_obj.filename}</li>'
    
    html_content += """
                </ul>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0; color: #856404;">
                    <strong>Next Steps:</strong> Review the attached documents and contact the driver within 24-48 hours to proceed with the registration process.
                </p>
            </div>
            
            <p style="color: #666; font-size: 12px; margin-top: 30px; text-align: center;">
                This email was sent automatically from the Trucking Document Management System.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Create message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    # Add file attachments
    for field_name, file_obj in files.items():
        if file_obj and file_obj.filename and hasattr(file_obj, 'read'):
            try:
                # Read file content
                file_content = file_obj.read()
                file_obj.seek(0)  # Reset file pointer
                
                # Encode file content
                encoded_content = base64.b64encode(file_content).decode()
                
                # Create attachment
                attachment = Attachment(
                    file_content=encoded_content,
                    file_name=file_obj.filename,
                    file_type=file_obj.content_type or 'application/octet-stream',
                    disposition='attachment'
                )
                message.add_attachment(attachment)
                
            except Exception as e:
                print(f"Error attaching file {file_obj.filename}: {e}")
    
    try:
        response = sg.send(message)
        print(f"Email sent successfully. Status code: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False