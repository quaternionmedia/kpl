from setuptools import setup, find_packages

setup(
    name='kpl',
    install_requires=[
        'pluggy>=0.3,<1.0',
        'krpc>=0.4.8',
        'fastapi>=0.63.0',
        'aiofiles>=0.5.0',
        'orjson>=3.5.1',
        'pika>=1.2.0',
        'uvicorn>=0.13.3'
    ],
    entry_points={'console_scripts': ['kpl=kpl.main:main']},
    packages=find_packages(),
)
