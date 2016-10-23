import os

from fabric.api import env, task, run, cd

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
