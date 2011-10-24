from armstrong.dev.tasks import *


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'armstrong.utils.celery',
    ),
    'SITE_ID': 1,
}

main_app = "celery"
tested_apps = (main_app,)
