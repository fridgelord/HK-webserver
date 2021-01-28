import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def send_mail(
    sender_email,
    receiver_email,
    subject,
    smtp_server,
    body="",
    password=None,
    smtp_port=25,
    attachments=None,
):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if attachments:
        if isinstance(attachments, str):
            attachments = (attachments,)
        for attachment_path in attachments:
            attachment_name = Path(attachment_path).name
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_name}",
            )
            message.attach(part)

    text = message.as_string()

    context = ssl.create_default_context()
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    elif smtp_port == 587:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    else:
        pass # should be someting for 25



def send_mail_read_credentials(
    receiver_email,
    subject,
    credentials_file="credentials.txt",
    body="",
    attachments=None,
):
    """Read info about server and usr/pw
    from credentials_file

    credentials_file is a text file with following lines:
    smpt_server
    smtp_port
    user/sender_email
    password
    """
    with open(credentials_file) as fp:
        smtp_server, smtp_port, sender_email, password = fp.read().splitlines()

    send_mail(
        sender_email=sender_email,
        receiver_email=receiver_email,
        subject=subject,
        body=body,
        smtp_server=smtp_server,
        smtp_port=int(smtp_port),
        password=password,
        attachments=attachments,
    )
