FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/files && \
    echo "Q1 Patient Report - Internal Use Only" > /app/files/report.txt

EXPOSE 5000

CMD ["python", "-c", "import init_db; init_db.wait_for_db(); import subprocess; subprocess.run(['python', 'app.py'])"]