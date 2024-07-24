from fastapi.background import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi_mail import ConnectionConfig
from constants import *
from builtins import str


class EmailSchema(BaseModel):
    email: List[EmailStr]


def check_email(email):
    import re

    regex = r"\b[A-Za-z0-9._%]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_FROM=MAIL_FROM,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


def email_template_otp(user_name, otp_code):
    email_template_otp_ = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <p>Dear {user_name},</p>
        <p>Greetings from !</p>
        <p>As requested, here is your One-Time Password (OTP) for accessing your  account:</p>
        <p>OTP: <span style="color: #FF0000;">{otp_code}</span></p>
        <p>Please use this OTP to log in securely. It will expire after a single use or after a short period, ensuring your account's safety.</p>
        <p>Should you encounter any issues or have any questions, don't hesitate to contact our friendly support team at <a href="mailto:pdfchat@mlxai.co.in">pdfchat@mlxai.co.in</a>.</p>
        <p>Thank you for choosing . We look forward to providing you with a seamless experience!</p>
        <p>Best regards,<br></p>
    </body>
    </html>
    """
    email_subject = "Your OTP for  Account"
    return email_subject, email_template_otp_


def send_otp(email_body, email_subject, email, background_task: BackgroundTasks):
    email_data = [EmailStr(object=email)]
    email_instance = EmailSchema(email=email_data)
    body = email_body
    subject = email_subject
    msg = MessageSchema(
        subject=subject,
        recipients=email_instance.dict().get("email"),
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    try:
        background_task.add_task(fm.send_message, msg)
    except Exception as e:
        return {"status": False, "message": str(e)}
    return f"Please check the email {email_instance} for otp details"
