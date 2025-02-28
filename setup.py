"""
Script d'installation du package FEC Generator
"""

from setuptools import setup, find_packages

setup(
    name="fec_generator",
    version="1.0.0",
    description="Générateur de Fichier des Écritures Comptables (FEC)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Votre Nom",
    author_email="votre.email@exemple.com",
    url="https://github.com/votre-compte/fec-generator",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "faker>=8.0.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fec-generator=fec_generator.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires=">=3.6",
)