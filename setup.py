from setuptools import setup, find_packages

setup(
    name='yang-to-fuse',
    version=0.1,
    description='YANG model to Fuse index schema converter.',
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    packages=['yangtofuse'],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'colander',
        'pyang',
        'setuptools',
    ],
    entry_points={
        'paste.app_factory': [
        ],
        'console_scripts': [
            'yang-to-fuse = yangtofuse.cli:main'
        ],
    },
    extras_require={
        'test': [
        ],
    }
)
