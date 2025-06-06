FROM python:3.10-slim

WORKDIR /app

# Copia solo requirements e installa prima
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto solo dopo aver installato
COPY . .

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]