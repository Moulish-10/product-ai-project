FROM python:3.11-slim

WORKDIR /app

# Ultralytics configuration directory
ENV YOLO_CONFIG_DIR=/app/.config/Ultralytics

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --default-timeout=300 \
    --retries=10 \
    -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root application user
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/.config/Ultralytics \
    && chown -R appuser:appuser /app

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY yolo11n.pt ./
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Run the application as a non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1


ENTRYPOINT ["/entrypoint.sh"]