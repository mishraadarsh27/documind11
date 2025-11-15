"""
Setup script for DocuMind
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]

setup(
    name="documind",
    version="1.0.0",
    description="AI Document Intelligence Agent - Multi-agent system for document analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DocuMind Team",
    author_email="documind@example.com",
    url="https://github.com/documind/documind",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "documind=documind.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
)

