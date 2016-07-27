from invoke import Collection
from invoke import run
from invoke import task


@task()
def build(ctx):
    run('python setup.py bdist_wheel')
    run('docker build -t {docker_repo} .'.format(**ctx))


@task()
def test_image(ctx):
    run('''
        docker run --rm=true --entrypoint nosetests \
        {docker_repo} {test_modules}
    '''.format(**ctx))


@task()
def push(ctx):
    run('docker push {docker_repo}'.format(**ctx))


ns = Collection(build, test_image, push)
ns.configure({
    'docker_repo': 'docker.qsensei.com/yang-to-fuse',
    'test_modules': 'yangtofuse',
})
