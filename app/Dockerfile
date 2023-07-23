# Use the official Python base image
FROM python:3.11-slim

WORKDIR /wasata

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip


# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"



# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /wasata/app
COPY .env /wasata/.env


# Make the entrypoint script executable
COPY alembic.ini /wasata/alembic.ini

COPY entrypoint.sh entrypoint.sh

RUN chmod +x /wasata/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
