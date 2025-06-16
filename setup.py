#!/usr/bin/env python
"""Setup script for Sortify AI - Intelligent Image Organization Tool"""

from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sortify-ai",
    version="1.0.0",
    author="Dmytro Dziublenko",
    author_email="d.dziublenko@gmail.com",
    description="AI-powered image organization and categorization tool using OpenAI Vision API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d-dziublenko/sortify-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "rich>=13.0.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sortify-ai=image_analyzer:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/d-dziublenko/sortify-ai/issues",
        "Source": "https://github.com/d-dziublenko/sortify-ai",
    },
)
