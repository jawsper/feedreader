from setuptools import setup, find_packages

from feedreader import get_version

setup(
    name='feedreader',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'django==2.0.3',
        'Pillow==5.0.0',
        'feedparser==5.2.1',
        'beautifulsoup4==4.6.0',
        'django-mptt==0.9.0',
        'psycopg2-binary==2.7.4',
        'celery==4.1.0',
        'django-celery-beat==1.1.1',
        'redis==2.10.6',
        'django-extensions==2.0.3',
        'raven==6.6.0',
    ],

    license='MIT',
    description='',
    long_description='',
    url='https://github.com/jawsper/feedreader',
    author='Jasper Seidel',
    author_email='code@jawsper.nl',
)
