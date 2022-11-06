from fastapi import APIRouter
import logging
import smtplib
from typing import Union
from pydantic import BaseModel
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..config import settings
from ..security import AuthenticatedUser, User, UserResponse

Scheduler = BackgroundScheduler()

router = APIRouter()


def send_notification(email, message):
        logging.info(f"Sending email to {email} with the message {message}.")

        SERVER = 'smtp.gmail.com'
        PORT = 587
        current_time = datetime.now()
        source_email = "wagnoleao@gmail.com"
        source_email_password = settings.source_email_password

        print("TESTE")
        print(source_email_password)

        body_message = MIMEMultipart()
        body_message['Subject'] = 'Notification alert of behavior'
        body_message['Subject'] += ' - '
        body_message['Subject'] += str(current_time.day) + \
            '-' + str(current_time.year)

        body_message['From'] = source_email
        body_message['To'] = email
        body_message.attach(MIMEText(message, 'plain'))

        logging.info('Initiating server...')

        try:
            server = smtplib.SMTP(SERVER, PORT)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(source_email, source_email_password)
            server.sendmail(source_email, email, body_message.as_string())
        except (
            smtplib.SMTPHeloError,
            smtplib.SMTPAuthenticationError,
            smtplib.SMTPSenderRefused
        ):
            logging.warning("Error! Unable to send the email!")
            return False

        logging.info('Notification was sended.')

        server.quit()
        return True


class Notification(BaseModel):
    id: str
    email: str
    day: int
    hour: int
    minute: int
    message: Union[str, None] = None


days_of_week = {
    1: "mon",
    2: "tue",
    3: "wed",
    4: "thu",
    5: "fri",
    6: "sat",
    7: "sun"
}


@router.get("/")
async def get_notifications():
    notifications = Scheduler.get_jobs()
    response = []
    for job in notifications:
        response.append([
            {
                "id": job.id,
                "name": job.name,
                "args": job.args,
                "misfire_grace_time": job.misfire_grace_time,
            }
        ])
    return response


@router.post("/")
async def set_notification(notification: Notification):
    Scheduler.add_job(
            send_notification, 
            'cron',
            day_of_week=days_of_week[notification.day],
            hour=notification.hour,
            minute=notification.minute,
            id=notification.id,
            coalesce=True,
            misfire_grace_time=60,
            replace_existing=True,
            jobstore='notifications',
            args=[ notification.email, notification.message ]
    )
    return { "ok": True }

@router.delete("/")
async def reset_notifications():
    return { "ok": False }
