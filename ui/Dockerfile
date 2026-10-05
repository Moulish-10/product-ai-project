FROM python:3.11-slim

WORKDIR /app

COPY ui/requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/requirements.txt

COPY ui /app/ui

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "ui/app.py", "--server.address=0.0.0.0", "--server.port=8501"]