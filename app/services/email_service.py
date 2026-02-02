import asyncio
from email.message import EmailMessage
import aiosmtplib


async def send_email(recipient: str, subject: str, body: str):
    admin_email = "admin@gmail.com"

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="127.0.0.1",
        port=25,
    )