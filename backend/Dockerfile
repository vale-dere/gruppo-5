FROM python:3.10-slim

WORKDIR /app

# Copy only requirements and install first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest only after installing
COPY . .

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]