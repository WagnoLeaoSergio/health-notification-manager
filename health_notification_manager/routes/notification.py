from fastapi import APIRouter
import logging
from typing import Union
from pydantic import BaseModel
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from ..security import AuthenticatedUser, User, UserResponse

Scheduler = BackgroundScheduler()

router = APIRouter()


def send_notification(email, message):
    logging.warning(f"Sending email to {email} with the message {message}.")


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
