#!/usr/bin/env python3
"""
Setup script for the ElevenLabs Text-to-Speech Package
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "ElevenLabs Text-to-Speech Package"

# Read requirements from requirements.txt
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['requests>=2.31.0', 'python-dotenv>=1.0.0', 'elevenlabs>=1.0.0']

setup(
    name="elevenlabs-tts-package",
    version="1.0.0",
    author="Text-to-Speech Team",
    author_email="your-email@example.com",
    description="A comprehensive Python package for ElevenLabs text-to-speech with advanced features",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/elevenlabs-tts-package",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=1.0.0",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "matplotlib>=3.5.0",
            "numpy>=1.21.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "elevenlabs-tts=text_to_speech.cli.interactive:main",
            "tts-quick-start=text_to_speech.cli.quick_start:main",
        ],
    },
    include_package_data=True,
    package_data={
        "text_to_speech": [
            "config/*.json",
            "examples/*.py",
            "*.md",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/elevenlabs-tts-package/issues",
        "Source": "https://github.com/your-username/elevenlabs-tts-package",
        "Documentation": "https://elevenlabs-tts-package.readthedocs.io/",
    },
    keywords="text-to-speech, tts, elevenlabs, audio, speech-synthesis, ai, voice",
)