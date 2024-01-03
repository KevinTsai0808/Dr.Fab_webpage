from flask_wtf import FlaskForm

from flask import flash, redirect, url_for
from flask_mail import Mail, Message
import random
import string
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.fields import EmailField
from wtforms import BooleanField
from application.author.model import UserRegister
from application import app, db
import secrets
import string

app.config.update(
    DEBUG=False,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('admin', ''),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='',
    MAIL_PASSWORD=''
)

mail = Mail(app)



class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    username = StringField('公司統編', validators=[
        validators.DataRequired(),
        validators.Length(8, 8)
    ])

    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('保持登入')

    submit = SubmitField('Log in')

class FormRegister(FlaskForm):
    """依照Model來建置相對應的Form
    
    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('公司統編', validators=[
        validators.DataRequired(),
        validators.Length(8, 8)
    ])
    email = EmailField('電子郵件', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])

    # password = PasswordField('密碼', validators=[
    #     validators.DataRequired(),
    #     validators.Length(5, 10),
    #     # validators.EqualTo('password2', message='兩次輸入密碼需相同！')
    # ])

    def generate_random_password(self):
        length = 10
        characters = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(random.choice(characters) for i in range(length))
        return random_password

    def generate_verification_token(self):
        # 生成一個隨機的、安全的驗證令牌
        return secrets.token_urlsafe(30)

    def send_registration_email(self, user_email, verification_token, random_password):
        subject = 'Registration Confirmation'
        verification_link = url_for('verify_registration', token=verification_token, _external=True)
        body = f"Thank you for registering! Please click the following link to verify your email and complete the registration:\n{verification_link}\nYour password is: {random_password}"
        
        msg = Message(subject, recipients=[user_email], body=body)
        mail.send(msg)

    def send_verification_email(self, user_email, verification_token):
        subject = 'Account Verification'
        verification_link = url_for('verify_email', token=verification_token, _external=True)
        body = f"Thank you for registering! Please click the following link to verify your email:\n{verification_link}"
        
        msg = Message(subject, recipients=[user_email], body=body)
        mail.send(msg)

    def validate_email(self, field):
        if UserRegister.query.filter_by(email=field.data).first():
            flash('此電子郵件已被註冊')
            raise validators.ValidationError('此電子郵件已被註冊')

    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            flash('此公司統編已被註冊')
            raise  validators.ValidationError('此公司統編已被註冊')

    submit = SubmitField('註冊')
    def on_submit(self):
        verification_token = self.generate_verification_token()
        random_password = self.generate_random_password()
        user = UserRegister(
            username=self.username.data,
            email=self.email.data,
            verification_token=verification_token,
            password=random_password,
            verified=False  # Assuming email is not verified initially
        )
        db.session.add(user)
        db.session.commit()
        self.send_registration_email(self.email.data, verification_token, random_password)