# Use official Python image ( from docker hub)
FROM python:3.10-slim

# Set environment variables ( 1 means yes, 0 means No)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install OS dependencies (container system)
RUN apt-get update && apt-get install -y build-essential poppler-utils && rm -rf /var/lib/apt/lists/*

# Copy requirements copy requirements.txt from . (dot means current directory pointing to the container above)
COPY requirements.txt .

COPY .env .

# Copy project files (from current directory to this container directory)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run FastAPI with uvicorn
CMD ["python", "-m","uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

# Replace last CMD in prod
#CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]