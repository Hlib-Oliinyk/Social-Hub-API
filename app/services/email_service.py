from email.message import EmailMessage

import aiosmtplib

from app.models import User
from app.core.config import ADMIN_GMAIL, APP_PASSWORD

async def send_email(recipient: str, subject: str, body: str):
    admin_email = ADMIN_GMAIL
    app_password = APP_PASSWORD

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=admin_email,
        password=app_password,
    )


async def send_welcome_email(user: User):
    await send_email(
        recipient=user.email,
        subject="Welcome!",
        body=f"Dear {user.username}, Thank you for registration!"
    )


async def print_welcome_message(user: User):
    print(f"Dear {user.username}, Thank you for registration!")