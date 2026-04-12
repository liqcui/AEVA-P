"""
AEVA - Algorithm Evaluation & Validation Agent
Setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="aeva",
    version="0.1.0",
    author="AEVA Development Team",
    author_email="aeva@example.com",
    description="Algorithm Evaluation & Validation Agent - Intelligent platform for algorithm quality assurance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liqcui/AVEA-P",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.6.0",
        "sqlalchemy>=2.0.25",
        "redis>=5.0.1",
        "torch>=2.1.2",
        "scikit-learn>=1.4.0",
        "numpy>=1.26.3",
        "pandas>=2.2.0",
        "transformers>=4.37.0",
        "anthropic>=0.18.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
        "structlog>=24.1.0",
        "celery>=5.3.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.4",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "isort>=5.13.2",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "aeva=aeva.cli_enhanced:cli",
            "aeva-server=aeva.api.server:main",
            "aeva-worker=aeva.auto.worker:main",
            "aeva-dashboard=aeva.dashboard.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
