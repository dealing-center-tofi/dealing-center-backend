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
def restart_gunicorn():
    sudo('systemctl stop gunicorn-dealing_center.service')
    sudo('systemctl start gunicorn-dealing_center.service')


@task
def deploy():
    fetch_files_from_repository()
    migrate()
    restart_gunicorn()
