#!/usr/bin/env python3
"""
Setup script for the FAL Image-to-Image Package
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'docs', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "FAL AI Image-to-Image Generator with Multi-Model Support"

# Read requirements from requirements.txt
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['fal-client', 'python-dotenv', 'requests', 'typing-extensions']

setup(
    name="fal-image-to-image",
    version="2.0.0",
    author="AI Assistant",
    author_email="assistant@example.com",
    description="A comprehensive Python package for FAL AI image-to-image generation with multi-model support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/fal-image-to-image",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
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
            "pillow>=8.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "fal-image-to-image=fal_image_to_image.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "fal_image_to_image": [
            "config/*.json",
            "*.md",
        ],
        "": ["docs/*.md", "examples/*.py", "assets/sample_images/*"]
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/fal-image-to-image/issues",
        "Source": "https://github.com/your-username/fal-image-to-image",
        "Documentation": "https://fal-image-to-image.readthedocs.io/",
    },
    keywords="image-to-image, ai, fal, image-editing, seededit, photon, kontext, computer-vision",
)