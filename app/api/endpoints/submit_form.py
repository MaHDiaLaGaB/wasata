from fastapi import APIRouter, Body
from mailjet_rest import Client
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import logging
from app.core.config import config
from pydantic import EmailStr, BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from .routes import SUBMIT_FORM, CONTACTS
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

route = APIRouter(tags=["form"])


class MyEmailjetException(Exception):
    """
    problem happened your email did not send
    """


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    message: str


# create email message
@route.post(SUBMIT_FORM)
async def send_email(form: ContactForm = Body()):
    # configure emailjet client
    api_key = config.MJ_APIKEY_PUBLIC
    api_secret = config.MJ_APIKEY_PRIVATE
    emailjet = Client(auth=(api_key, api_secret), version="v3")

    # create email message
    message_body = {
        "From": {"Email": f"elmahdi0alagab@duck.com", "Name": f"{form.name}"},
        "To": [{"Email": "elmahdi0alagab@duck.com", "Name": "Mahdi"}],
        "Subject": f"New message from {form.name}",
        "TextPart": form.message,
        "HTMLPart": f"""
        <html>
          <body>
            <h1>New message from {form.name}</h1>
            <p><strong>Name:</strong> {form.name}</p>
            <p><strong>Email:</strong> {form.email}</p>
            <p><strong>Phone Number:</strong> {form.phone_number}</p>
            <p><strong>Message:</strong> {form.message}</p>
          </body>
        </html>
        """,
    }

    # send email message
    response = emailjet.send.create(data=message_body)

    return {"success": "Your message has been sent.", "response": f"{response}"}


def send_to_my_email(name, email, message, phone_number):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = 'elmahdi.alagab@gmail.com'
    msg['Subject'] = f'New message from {name}'

    body =f"""
    <h2 style="padding: 20px;">New Message</h2>
    <div style="margin: 20px;">
        <h3>Details:</h3>
        <ul style="margin-bottom: 20px; list-style-type: none; text-align: left;">
            <li><strong>Sender Name:</strong> {name}</li>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Phone:</strong> {phone_number}</li>
        </ul>
        <h3>Message:</h3>
        <p style="text-align: left;">{message}</p>
    </div>
    <div style="background-color: #f8f9fa; padding: 10px; text-align: center; margin-top: 20px;">
        <p>© 2023 Wasata. All rights reserved.</p>
    </div>
    """
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('elmahdi.alagab@gmail.com', 'firfnntwvndqhqjp')
    text = msg.as_string()
    server.sendmail('elmahdi.alagab@gmail.com', 'elmahdi.alagab@gmail.com', text)
    server.quit()


@route.post(CONTACTS)
async def contact(form: ContactForm):
    send_to_my_email(form.name, form.email, form.message, form.phone_number)
    return {"message": "Email sent successfully"}
