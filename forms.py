from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

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
