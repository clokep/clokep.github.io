import os

from invoke import run, task

# local path configuration (can be absolute or relative to tasks)
env = {
    'deploy_path': 'output',
    'listen_port': 8000,
}


@task
def clean():
    """Delete any built output."""
    if os.path.isdir(env.get('deploy_path')):
        run('rm -rf {deploy_path}'.format(**env))
        run('mkdir {deploy_path}'.format(**env))


@task
def build():
    """Build the blog."""
    run('pelican -s pelicanconf.py content')


@task
def rebuild():
    """Clean, then build the blog."""
    clean()
    build()


@task
def regenerate():
    """Watch files and continually build the blog as changes occur."""
    run('pelican -r -s pelicanconf.py content', pty=True)


@task
def serve():
    """runly serve the blog."""
    run('cd {deploy_path} && python -m SimpleHTTP404Server {listen_port}'.format(**env), pty=True)


@task
def reserve():
    """First build the blog, then serve it."""
    build()
    serve()


@task
def preview():
    """Clean then build with the publish config."""
    clean()
    run('pelican -s publishconf.py content', pty=True)


@task
def publish():
    """Build with the publish config and push to the remote server."""
    preview()
    run('ghp-import -p -b master output')
