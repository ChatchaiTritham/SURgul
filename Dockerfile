# SURgul Docker Image for Reproducible Research
# Based on official Python image

FROM python:3.8-slim

# Metadata
LABEL maintainer="your.email@university.edu"
LABEL description="SURgul: Screening-First Risk Governance Logic - Research Container"
LABEL version="1.0.0-research"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY notebooks/ ./notebooks/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install SURgul package
RUN pip install -e .

# Create directories for data and outputs
RUN mkdir -p data results figures

# Expose Jupyter port
EXPOSE 8888

# Default command: Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", \
     "--NotebookApp.token=''", "--NotebookApp.password=''"]
