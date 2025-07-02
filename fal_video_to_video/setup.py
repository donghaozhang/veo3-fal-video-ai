"""
Setup script for FAL Video to Video package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="fal-video-to-video",
    version="0.1.0",
    description="AI-powered video audio generation using FAL's ThinkSound API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FAL Video to Video",
    author_email="contact@example.com",
    url="https://github.com/yourusername/fal-video-to-video",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai video audio generation fal thinksound",
    entry_points={
        "console_scripts": [
            "fal-video-to-video=fal_video_to_video.__main__:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
        "video": [
            "moviepy>=1.0.3",
        ],
    },
)