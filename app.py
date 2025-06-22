import os
import logging
import asyncio
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from email_service import send_document_submission_email
# Temporarily disable telegram imports to fix startup issue
try:
    from telegram_bot import initialize_bot, send_application_to_telegram
    TELEGRAM_ENABLED = True
except ImportError as e:
    logging.warning(f"Telegram bot disabled due to import error: {e}")
    TELEGRAM_ENABLED = False
    def initialize_bot():
        return False
    async def send_application_to_telegram(form_data, files):
        logging.info("Telegram bot not available - skipping notification")
import uuid
from datetime import datetime
import threading
import io

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Telegram bot
telegram_bot_initialized = False
def init_telegram_bot():
    global telegram_bot_initialized
    if not telegram_bot_initialized:
        try:
            if initialize_bot():
                telegram_bot_initialized = True
                logging.info("Telegram bot initialized successfully")
            else:
                logging.warning("Telegram bot initialization failed - check TELEGRAM_BOT_TOKEN")
        except Exception as e:
            logging.error(f"Error initializing Telegram bot: {e}")

# Initialize bot on startup
init_telegram_bot()

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Brokerage companies data
BROKERAGE_COMPANIES = [
    {"name": "Partner Company 1", "logo": "static/images/logo1.webp"},
    {"name": "Partner Company 2", "logo": "static/images/logo2.webp"},
    {"name": "Partner Company 3", "logo": "static/images/logo3.webp"},
    {"name": "Partner Company 4", "logo": "static/images/logo4.webp"},
    {"name": "Partner Company 5", "logo": "static/images/logo5.webp"},
    {"name": "Partner Company 6", "logo": "static/images/logo6.webp"},
    {"name": "Partner Company 7", "logo": "static/images/logo7.webp"},
    {"name": "Partner Company 8", "logo": "static/images/logo8.webp"}
]

class DocumentUploadForm(FlaskForm):
    # Driver Information
    full_name = StringField('Полное имя', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Required Documents
    drivers_license = FileField('Водительское удостоверение CDL', 
                               validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    medical_certificate = FileField('Медицинская справка DOT', 
                                   validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    social_security = FileField('Карточка социального страхования', 
                               validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    vehicle_registration = FileField('Регистрация транспортного средства', 
                                    validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    insurance_certificate = FileField('Страховой сертификат', 
                                     validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    ifta_permit = FileField('Разрешение IFTA (если применимо)', 
                           validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    mc_authority = FileField('MC Authority (если есть)', 
                            validators=[FileAllowed(ALLOWED_EXTENSIONS)])
    
    submit = SubmitField('Отправить документы')

@app.route('/')
def index():
    return render_template('index.html', companies=BROKERAGE_COMPANIES)

@app.route('/success.html')
def success():
    return render_template('success.html')

@app.route('/upload', methods=['POST'])
def upload_documents():
    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'full_name': request.form.get('full_name', ''),
                'phone': request.form.get('phone', ''),
                'email': request.form.get('email', '')
            }
            
            # Validate required fields
            if not all([form_data['full_name'], form_data['phone'], form_data['email']]):
                flash('All personal information fields are required', 'error')
                return redirect(url_for('index'))
            
            # Get uploaded files
            files = {}
            file_fields = ['drivers_license', 'medical_certificate', 'w9_form',
                          'vehicle_registration', 'insurance_certificate', 'mc_authority']
            
            for field_name in file_fields:
                if field_name in request.files:
                    file_obj = request.files[field_name]
                    if file_obj and file_obj.filename:
                        if allowed_file(file_obj.filename):
                            files[field_name] = file_obj
                        else:
                            flash(f'Invalid file type for {field_name}', 'error')
                            return redirect(url_for('index'))
            
            # Check if required documents are present
            required_docs = ['drivers_license', 'medical_certificate', 'w9_form',
                           'vehicle_registration', 'insurance_certificate']
            missing_docs = [doc for doc in required_docs if doc not in files]
            
            if missing_docs:
                flash(f'Missing required documents: {", ".join(missing_docs)}', 'error')
                return redirect(url_for('index'))
            
            # Send email with documents
            email_success = send_document_submission_email(form_data, files)
            
            # Send to Telegram bot
            telegram_success = False
            if telegram_bot_initialized:
                try:
                    # Create copies of files for Telegram (since we need to reset file pointers)
                    telegram_files = {}
                    for field_name, file_obj in files.items():
                        file_obj.seek(0)
                        file_content = file_obj.read()
                        telegram_files[field_name] = io.BytesIO(file_content)
                        telegram_files[field_name].name = file_obj.filename
                        file_obj.seek(0)  # Reset original file pointer
                    
                    # Send to Telegram asynchronously
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    telegram_success = loop.run_until_complete(
                        send_application_to_telegram(form_data, telegram_files)
                    )
                    loop.close()
                    
                    if telegram_success:
                        logging.info("Application sent to Telegram successfully")
                    else:
                        logging.error("Failed to send application to Telegram")
                        
                except Exception as e:
                    logging.error(f"Error sending to Telegram: {e}")
            
            if email_success or telegram_success:
                # Create unique folder for backup storage
                submission_id = str(uuid.uuid4())
                submission_folder = os.path.join(app.config['UPLOAD_FOLDER'], submission_id)
                os.makedirs(submission_folder, exist_ok=True)
                
                # Save files locally as backup
                for field_name, file_obj in files.items():
                    filename = secure_filename(file_obj.filename)
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    final_filename = f"{field_name}_{timestamp}_{name}{ext}"
                    
                    filepath = os.path.join(submission_folder, final_filename)
                    file_obj.save(filepath)
                    file_obj.seek(0)  # Reset file pointer after saving
                
                app.logger.info(f"Document submission from {form_data['full_name']}, Email: {form_data['email']}")
                app.logger.info(f"Submission ID: {submission_id}")
                
                flash('Documents submitted successfully!', 'success')
                return redirect('/success.html')
            else:
                flash('Failed to send email. Please try again.', 'error')
                return redirect(url_for('index'))
                
        except Exception as e:
            app.logger.error(f"Error processing document submission: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('index'))
    
    flash('Method not allowed', 'error')
    return redirect(url_for('index'))

@app.route('/api/submit', methods=['POST'])
def api_submit():
    """API endpoint for form submission from static HTML"""
    try:
        # Get form data
        form_data = {
            'full_name': request.form.get('full_name', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'email': request.form.get('email', '').strip(),
            'experience': request.form.get('experience', '').strip(),
            'comments': request.form.get('comments', '').strip()
        }
        
        # Validate required fields
        if not all([form_data['full_name'], form_data['phone'], form_data['email']]):
            return jsonify({'success': False, 'error': 'All personal information fields are required'}), 400
        
        # Get uploaded files
        files = {}
        file_fields = ['drivers_license', 'medical_certificate', 'w9_form',
                      'vehicle_registration', 'insurance_certificate', 'mc_authority']
        
        for field_name in file_fields:
            if field_name in request.files:
                file_obj = request.files[field_name]
                if file_obj and file_obj.filename:
                    if allowed_file(file_obj.filename):
                        files[field_name] = file_obj
                    else:
                        return jsonify({'success': False, 'error': f'Invalid file type for {field_name}'}), 400
        
        # Check if required documents are present
        required_docs = ['drivers_license', 'medical_certificate', 'w9_form',
                       'vehicle_registration', 'insurance_certificate']
        missing_docs = [doc for doc in required_docs if doc not in files]
        
        if missing_docs:
            return jsonify({'success': False, 'error': f'Missing required documents: {", ".join(missing_docs)}'}), 400
        
        # Send to Telegram bot
        telegram_success = False
        if telegram_bot_initialized:
            try:
                # Create copies of files for Telegram
                telegram_files = {}
                for field_name, file_obj in files.items():
                    file_obj.seek(0)
                    file_content = file_obj.read()
                    telegram_files[field_name] = io.BytesIO(file_content)
                    telegram_files[field_name].name = file_obj.filename
                    file_obj.seek(0)
                
                # Send to Telegram asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                telegram_success = loop.run_until_complete(
                    send_application_to_telegram(form_data, telegram_files)
                )
                loop.close()
                
                if telegram_success:
                    logging.info("Application sent to Telegram successfully")
                
            except Exception as e:
                logging.error(f"Error sending to Telegram: {e}")
        
        # Also try sending email as backup
        email_success = send_document_submission_email(form_data, files)
        
        if telegram_success or email_success:
            # Save files locally as backup
            submission_id = str(uuid.uuid4())
            submission_folder = os.path.join(app.config['UPLOAD_FOLDER'], submission_id)
            os.makedirs(submission_folder, exist_ok=True)
            
            for field_name, file_obj in files.items():
                filename = secure_filename(file_obj.filename)
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_filename = f"{field_name}_{timestamp}_{name}{ext}"
                
                filepath = os.path.join(submission_folder, final_filename)
                file_obj.save(filepath)
            
            return jsonify({
                'success': True, 
                'message': 'Documents submitted successfully!',
                'telegram_sent': telegram_success,
                'email_sent': email_success
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to send documents. Please try again.'}), 500
            
    except Exception as e:
        logging.error(f"Error in API submit: {e}")
        return jsonify({'success': False, 'error': 'An error occurred while processing your submission.'}), 500

@app.route('/telegram/status')
def telegram_status():
    """Check Telegram bot status"""
    return jsonify({
        'bot_initialized': telegram_bot_initialized,
        'bot_token_configured': bool(os.environ.get('TELEGRAM_BOT_TOKEN'))
    })

@app.errorhandler(413)
def too_large(e):
    flash('Файл слишком большой. Максимальный размер файла: 16MB', 'error')
    return redirect(url_for('upload_documents'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
