from setuptools import setup

setup(
    # Application name:
    name="ecg",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Quentin Guilloteau, Antoine Waehren",
    author_email="Quentin.Guilloteau@unibas.ch, Antoine.Waehren@stud.unibas.ch",

    # Packages
    packages=["app"],

    # Include additional files into the package
    entry_points={
        'console_scripts': ['ecg=app.ecg:main'],
    },

    # Details
    url="https://forge.chapril.org/GuilloteauQ/study-docker-repro-longevity",

    description="Test the software environment of Dockerfiles from research artifacts",

    long_description="""
    ECG is a program that automates software environment checking for scientific artifacts.
    It is meant to be executed periodically to analyze variations in the software environment of the artifact through time.
    """,

    install_requires=[
        "requests",
    ],
    
    include_package_data=True,
)
