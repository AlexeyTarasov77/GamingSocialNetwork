from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnetwork.settings")

app = Celery("socialnetwork")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from posts.tasks import recommend_posts_by_mail  # Import your task here

    # Add your periodic task
    sender.add_periodic_task(crontab(minute=0, hour=0), recommend_posts_by_mail.s())
