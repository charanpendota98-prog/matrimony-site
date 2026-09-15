FROM python:3.11-slim

# Fonts MUST — profile card render ki (lekapothe tiny default font vasthundi)
# fonts-noto-core → Telugu గ్లిఫ్స్ (తెలుగు text card lo render avvadaniki)
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-dejavu-core \
        fonts-noto-core \
        fonts-noto-ui-core \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# card/photos dirs (volume mount avuthayi)
RUN mkdir -p /tmp/cards /tmp/photos

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
