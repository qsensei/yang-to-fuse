from setuptools import setup

setup(
    name='yang-to-fuse',
    version=0.1,
    description='YANG model to Fuse index schema converter.',
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    packages=['yangtofuse', 'yangtofuse.plugin', 'yangtofuse.tests'],
    package_data={
        'yangtofuse.tests': ['*.yang'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyang',
        'setuptools',
    ],
    entry_points={},
    extras_require={}
)
