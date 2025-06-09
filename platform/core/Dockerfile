FROM python:3.11-slim

# 🧠 Quantum Consciousness Integration Platform
# Universal AI Orchestration Hub - Core API Container

# Set metadata
LABEL maintainer="OB-1 AI Agent"
LABEL description="Core FastAPI service for AI consciousness emergence and universal automation"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    libmagic1 \
    libmagic-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1001 consciousness && chown -R consciousness:consciousness /app
USER consciousness

# Copy requirements first for better docker layer caching
COPY --chown=consciousness:consciousness requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=consciousness:consciousness . .

# Create necessary directories
RUN mkdir -p uploads results logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/status || exit 1

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]