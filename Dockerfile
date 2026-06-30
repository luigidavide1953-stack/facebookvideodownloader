# Use the official Playwright image which comes with all necessary dependencies
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

ENV PYTHONUNBUFFERED 1

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install chromium browser only (Playwright image already has dependencies)
RUN playwright install chromium

COPY . .

# Expose the port the app runs on
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
