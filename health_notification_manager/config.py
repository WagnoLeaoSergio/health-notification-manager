import os

from dynaconf import Dynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    envvar_prefix="health_notification_manager",
    preload=[os.path.join(HERE, "default.toml")],
    settings_files=["settings.toml", ".secrets.toml"],
    environments=["development", "production", "testing"],
    env_switcher="health_notification_manager_env",
    load_dotenv=False,
)


"""
# How to use this application settings

```
from health_notification_manager.config import settings
```

## Acessing variables

```
settings.get("SECRET_KEY", default="sdnfjbnfsdf")
settings["SECRET_KEY"]
settings.SECRET_KEY
settings.db.uri
settings["db"]["uri"]
settings["db.uri"]
settings.DB__uri
```

## Modifying variables

### On files

settings.toml
```
[development]
KEY=value
```

### As environment variables
```
export health_notification_manager_KEY=value
export health_notification_manager_KEY="@int 42"
export health_notification_manager_KEY="@jinja {{ this.db.uri }}"
export health_notification_manager_DB__uri="@jinja {{ this.db.uri | replace('db', 'data') }}"
```

### Switching environments
```
health_notification_manager_ENV=production health_notification_manager run
```

Read more on https://dynaconf.com
"""
