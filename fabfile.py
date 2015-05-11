from fabric.api import env, local, task
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
env.listen_port = 8000
DEPLOY_PATH = env.deploy_path


@task
def clean():
    """Delete any built output."""
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


@task
def build():
    """Build the blog."""
    local('pelican -s pelicanconf.py content')


@task
def rebuild():
    """Clean, then build the blog."""
    clean()
    build()


@task
def regenerate():
    """Watch files and continually build the blog as changes occur."""
    local('pelican -r -s pelicanconf.py content')


@task
def serve():
    """Locally serve the blog."""
    local('cd {deploy_path} && python ../fake_server.py {listen_port}'.format(**env))


@task
def reserve():
    """First build the blog, then serve it."""
    build()
    serve()


@task
def preview():
    """Clean then build with the publish config."""
    clean()
    local('pelican -s publishconf.py content')


@task
def publish():
    """Build with the publish config and push to the remote server."""
    preview()
    local('ghp-import -p -b master output')
