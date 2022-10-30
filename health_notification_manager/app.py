import io
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .db import create_db_and_tables, engine
from .routes import main_router
from .routes.notification import Scheduler



def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("VERSION")
    """
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


description = """
health_notification_manager API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="health_notification_manager",
    description=description,
    version=read("VERSION"),
    terms_of_service="http://health_notification_manager.com/terms/",
    contact={
        "name": "WagnoLeaoSergio",
        "url": "http://health_notification_manager.com/contact/",
        "email": "WagnoLeaoSergio@health_notification_manager.com",
    },
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
)

if settings.server and settings.server.get("cors_origins", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=settings.get("server.cors_allow_credentials", True),
        allow_methods=settings.get("server.cors_allow_methods", ["*"]),
        allow_headers=settings.get("server.cors_allow_headers", ["*"]),
    )

app.include_router(main_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)

    Scheduler.add_jobstore('sqlalchemy', alias="notifications", url="sqlite:///scheduler.db")
    #Scheduler.remove_all_jobs()

    try:
        Scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Error while creating scheduler")

