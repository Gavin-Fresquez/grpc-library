# Multi-stage Dockerfile for gRPC Library Project
# This Dockerfile builds a complete environment with Python, MySQL, MongoDB, and the gRPC library service

# Stage 1: Base Python environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development environment with databases
FROM base as development

# Install additional development tools
RUN apt-get update && apt-get install -y \
    mysql-client \
    mongodb-tools \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data/mysql /app/data/mongodb

# Set permissions
RUN chmod +x scripts/gen-proto-exports.py

# Generate protobuf files
RUN make compile-proto

# Expose ports
EXPOSE 50051 50052 3306 27017

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting development environment..."\n\
echo "Waiting for databases to be ready..."\n\
sleep 10\n\
echo "Starting gRPC server..."\n\
python main.py\n\
' > /app/start-dev.sh && chmod +x /app/start-dev.sh

# Default command for development
CMD ["/app/start-dev.sh"]

# Stage 3: Production environment
FROM base as production

# Install production dependencies only
RUN apt-get update && apt-get install -y \
    mysql-client \
    mongodb-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs

# Set permissions
RUN chmod +x scripts/gen-proto-exports.py

# Generate protobuf files
RUN make compile-proto

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 50051 50052

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import grpc; print('Health check passed')" || exit 1

# Production command
CMD ["python", "main.py"]