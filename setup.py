"""Setup script for AI Content Platform."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version
version_file = Path(__file__).parent / "ai_content_platform" / "__version__.py"
version_dict = {}
with open(version_file) as f:
    exec(f.read(), version_dict)

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file."""
    req_file = Path(__file__).parent / "requirements" / filename
    if req_file.exists():
        with open(req_file) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

# Base requirements
install_requires = read_requirements("base.txt")

# Optional requirements
extras_require = {
    "fal": read_requirements("fal.txt"),
    "google": read_requirements("google.txt"),
    "tts": read_requirements("tts.txt"),
    "video": read_requirements("video.txt"),
    "dev": read_requirements("dev.txt"),
}

# All optional dependencies
extras_require["all"] = list(set(
    req for reqs in [extras_require["fal"], extras_require["google"], 
                    extras_require["tts"], extras_require["video"]] 
    for req in reqs
))

setup(
    name="ai-content-platform",
    version=version_dict["__version__"],
    author=version_dict["__author__"],
    author_email=version_dict["__email__"],
    description=version_dict["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=version_dict["__url__"],
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "ai-content=ai_content_platform.cli.main:cli",
            "aicp=ai_content_platform.cli.main:cli",  # Short alias
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai, content generation, images, videos, audio, fal, elevenlabs, google, parallel processing",
    project_urls={
        "Documentation": "https://github.com/username/ai-content-platform",
        "Source": "https://github.com/username/ai-content-platform",
        "Tracker": "https://github.com/username/ai-content-platform/issues",
    },
)