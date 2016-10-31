from datetime import timedelta

from celery.task import task, periodic_task


@task
def task():
    print 'Task'


@periodic_task(run_every=timedelta(seconds=10))
def periodic_task():
    print 'Periodic task'
