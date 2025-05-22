# Use a Python base 
FROM python:3.10-slim

# working directory
WORKDIR /app

# Copies files in the working directory
COPY . .

# Installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# To run the FastAPI app
#using python -m uvicorn instead of uvicorn directly — always working.
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]