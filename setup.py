from setuptools import setup

setup(
    name='pomop-queue',
    version='0.1.0',
    description='Using Pomodoro and Task Queue to handle tasks productively',
    long_description=open('README.md').read(),
    author='Tung Son Do',
    author_email='dosontung007@gmail.com',
    packages=['pomop_queue'],
    license='MIT',
    install_requires=['pomop'],
    entry_points={
        'console_scripts': [
            'pomop-queue=pomop_queue.cli_parser:cli',
        ],
    }
)
