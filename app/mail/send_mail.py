import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
load_dotenv()

class Envs:
    MAIL_USERNAME:str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")

conf = ConnectionConfig(
    MAIL_USERNAME = Envs.MAIL_USERNAME,
    MAIL_PASSWORD = Envs.MAIL_PASSWORD,
    MAIL_FROM = Envs.MAIL_FROM,
    MAIL_PORT = Envs.MAIL_PORT,
    MAIL_SERVER = Envs.MAIL_SERVER,
    MAIL_FROM_NAME = Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="app/mail/templates"
)

async def send_registration_mail(subject : str, email_to : str, body : dict):
    message = MessageSchema(
        subject = subject,
        recipients = [email_to],
        template_body = body,
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message, template_name="email.html")

async def password_reset(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject = subject,
        recipients = [email_to],
        template_body = body,
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message, 
                          template_name="password_reset.html")
