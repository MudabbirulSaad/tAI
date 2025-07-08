from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of your requirements file
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Package version
VERSION = "1.0.0"

setup(
    name="tai",
    version=VERSION,
    author="Shoaib",
    author_email="shoaib@gmail.com>",
    description="tAI is a tool that helps you to find the right command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tai=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    python_requires='>=3.12',
    project_urls={
        "Bug Tracker": "https://github.com/KillerShoaib/tAI/issues",
        "Source Code": "https://github.com/KillerShoaib/tAI",
    },
) 