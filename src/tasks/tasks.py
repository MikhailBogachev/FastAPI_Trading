import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_report_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Тема письма'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}</h1>'
        '<img src="https://static.tildacdn.com/tild3961-3862-4039-b864-393237333162/dashboard-1.png" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_report_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
