import os

from fabric.api import env, task, run, cd, sudo, prefix

from dealing_center.settings.deploy import *


env.user = USER
env.hosts = [HOST]


@task
def connect_shell():
    os.execlp('ssh', '-C', '{user}@{host}'.format(user=USER, host=HOST))


@task
def ls():
    run('ls /home')
    with cd('/home'):
        run('ls')


@task
def fetch_files_from_repository():
    with cd(PROJECT_DIR):
        run('git fetch')
        run('git merge origin/master')


@task
def migrate():
    with cd(PROJECT_DIR), prefix('workon %s' % ENV_NAME):
        run('python manage.py migrate')


@task
def install_requirements():
    with cd(PROJECT_DIR), prefix('workon %s' % ENV_NAME):
        run('pip install -r requirements.txt')


@task
def restart_celery():
    sudo('service celeryd-dealing_center restart')
    sudo('service celerybeat-dealing_center restart')


@task
def restart():
    sudo('service gunicorn-dealing_center restart')
    restart_celery()


@task
def deploy():
    fetch_files_from_repository()
    install_requirements()
    migrate()
    restart()


@task
def stop_celery():
    sudo('service celeryd-dealing_center stop')
    sudo('service celerybeat-dealing_center stop')
