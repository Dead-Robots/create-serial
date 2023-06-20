from setuptools import setup

setup(
    name='createserial',
    version='1.4',
    packages=['createserial'],
    url='https://github.com/Dead-Robots/create-serial',
    license='',
    author='DRS',
    author_email='',
    description='Python serial interface for Create',
    install_requires=[
        'colorama',
        'pyserial'
    ]
)
