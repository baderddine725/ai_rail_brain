FROM python:3.10-bullseye

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Installer pip wheels avant
RUN pip install --upgrade pip wheel setuptools

# Copier requirements d'abord (cache docker)
COPY requirements.txt .

# Installer python deps
RUN pip install --prefer-binary -r requirements.txt

# Copier code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
