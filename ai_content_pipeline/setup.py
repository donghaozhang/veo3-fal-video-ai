"""
Setup script for AI Content Pipeline
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="ai-content-pipeline",
    version="1.0.0",
    author="AI Content Pipeline Team",
    author_email="developer@example.com",
    description="Unified content creation system that chains multiple AI operations together",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ai-content-pipeline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "video": [
            "moviepy>=1.0.3",
            "ffmpeg-python>=0.2.0",
        ],
        "all": [
            "moviepy>=1.0.3",
            "ffmpeg-python>=0.2.0",
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-content-pipeline=ai_content_pipeline.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_content_pipeline": [
            "config/*.yaml",
            "examples/*.yaml",
            "examples/*.json",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-org/ai-content-pipeline/issues",
        "Source": "https://github.com/your-org/ai-content-pipeline",
        "Documentation": "https://github.com/your-org/ai-content-pipeline/blob/main/README.md",
    },
)