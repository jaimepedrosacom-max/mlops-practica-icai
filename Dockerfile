FROM python:3.11-slim

WORKDIR /app

COPY requirements-serve.txt .
# Parches de seguridad del SO y herramientas de empaquetado actualizadas
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements-serve.txt

COPY app.py model.pkl ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
