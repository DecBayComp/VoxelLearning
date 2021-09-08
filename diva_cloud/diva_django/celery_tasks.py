from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django
# http://docs.celeryproject.org/en/master/django/first-steps-with-django.html#extensions
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diva_cloud.settings')
django.setup()

from jobapp.joblauncher import job_launcher

app = Celery('diva_cloud')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def launch_asynchron(jobid, inputs_dict, parameters_dict, jobtype):
    res = job_launcher(jobid, inputs_dict, parameters_dict, jobtype)
    return res

