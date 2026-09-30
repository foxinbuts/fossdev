"""Setup configuration for the sales package."""

from setuptools import setup, find_packages

setup(
    name="sales",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "sales=sales.cli:main",
        ],
    },
)
