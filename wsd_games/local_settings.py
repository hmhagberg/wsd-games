import dj_database_url

from .settings import *

DATABASES["default"] = dj_database_url.config()
