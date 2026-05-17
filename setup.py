"""
Setup script for SRGL package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
 long_description = fh.read()

setup(
 name="surgul",
 version="1.0.0",
 author="Chatchai Tritham",
 author_email="chatchait66@nu.ac.th, chakkrits@nu.ac.th",
 description="Safety-first Universal Risk Governance Logic for Clinical Triage AI",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="https://github.com/ChatchaiTritham/SURgul",
 package_dir={"": "src"},
 packages=find_packages(where="src"),
 classifiers=[
 "Development Status :: 4 - Beta",
 "Intended Audience :: Science/Research",
 "Topic :: Scientific/Engineering :: Artificial Intelligence",
 "Topic :: Scientific/Engineering :: Medical Science Apps.",
 "License :: OSI Approved :: MIT License",
 "Programming Language :: Python :: 3",
 "Programming Language :: Python :: 3.9",
 "Programming Language :: Python :: 3.10",
 ],
 python_requires=">=3.9",
 install_requires=[
 "numpy>=1.21.0",
 "pandas>=1.3.0",
 "scipy>=1.7.0",
 "scikit-learn>=1.0.0",
 "matplotlib>=3.4.0",
 "seaborn>=0.11.0",
 "pydantic>=1.9.0",
 "pyyaml>=6.0.0",
 "tqdm>=4.62.0",
 ],
 extras_require={
 "dev": [
 "pytest>=7.0.0",
 "pytest-cov>=3.0.0",
 "black>=22.0.0",
 "flake8>=4.0.0",
 "mypy>=0.950",
 ],
 "notebooks": [
 "jupyter>=1.0.0",
 "ipykernel>=6.0.0",
 "ipywidgets>=7.6.0",
 ],
 },
 entry_points={
 "console_scripts": [
 "surgul=surgul.cli.trix_cli:main",
 ],
 },
)
