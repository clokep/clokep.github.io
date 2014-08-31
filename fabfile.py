from fabric.api import *
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
env.listen_port = 8000
DEPLOY_PATH = env.deploy_path

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py content')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py content')

def serve():
    local('cd {deploy_path} && python ../fake_server.py {listen_port}'.format(**env))

def reserve():
    build()
    serve()

def preview():
    clean()
    local('pelican -s publishconf.py content')

def publish():
    preview()
    local('ghp-import -p -b master output')
