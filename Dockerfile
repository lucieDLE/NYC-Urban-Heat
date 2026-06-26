FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    libexpat1 \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["gunicorn", "app:server", "--chdir", "app", "-b", "0.0.0.0:7860", "--timeout", "120"]
