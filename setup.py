from setuptools import setup, find_packages

setup(
    name='kpl',
    install_requires='pluggy>=0.3,<1.0',
    entry_points={'console_scripts': ['kpl=kpl.main:main']},
    packages=find_packages(),
)
