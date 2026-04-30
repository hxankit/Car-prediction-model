import aiosmtplib
from email.message import EmailMessage

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "gamerzone0997@gmail.com"
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="gamerzone0997@gmail.com",
        password="ybvcjgmrcpnqokxh",
    )

    return {"message": "Email sent successfully"}