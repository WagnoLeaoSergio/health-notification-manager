import logging
import smtplib
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from typing import Union, List
from pydantic import BaseModel
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..config import settings
from ..security import AuthenticatedUser, User, UserResponse

Scheduler = BackgroundScheduler()

router = APIRouter()

logger = logging.getLogger("uvicorn")


def send_notification(email, message, date=None):
    logger.info(f"Sending email to {email} with the message {message}.")

    SERVER = 'smtp.gmail.com'
    PORT = 587
    current_time = datetime.now()
    source_email = "wagnoleao@gmail.com"
    source_email_password = "mkjukgtsajmeornl"
    # source_email_password = settings.source_email_password

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

    logger.info('Initiating server...')

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
        logger.warning("Error! Unable to send the email!")
        return False

    logger.info('Notification was sended.')

    server.quit()
    return True


class Notification(BaseModel):
    id: str
    date: str
    email: str
    message: Union[str, None] = None


class ScheduledNotifications(BaseModel):
    notifications: List[Notification]


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
    print(response)
    return response


@router.post("/")
async def set_notification(schedules: ScheduledNotifications):
    logger.info(schedules)
    schedules_data = jsonable_encoder(schedules)
    for notification in schedules_data["notifications"]:
        date = datetime.strptime(notification["date"], '%Y-%m-%d %H:%M:%S')
        weekday = date.weekday() + 1

        Scheduler.add_job(
            send_notification,
            'cron',
            day_of_week=days_of_week[weekday],
            hour=date.hour,
            minute=date.minute,
            id=notification["id"],
            coalesce=True,
            misfire_grace_time=60,
            replace_existing=True,
            jobstore='notifications',
            args=[notification["email"], notification["message"], date]
        )
    return {"ok": True}


@router.delete("/")
async def reset_notifications():
    return {"ok": False}
