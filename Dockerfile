# Use the official Python base image
FROM python:3.10-slim

WORKDIR /wasata

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean \
    && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip


# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app /wasata/app
COPY dev-database /wasata/dev-database


# Make the entrypoint script executable
COPY alembic.ini /wasata/alembic.ini
COPY .env /wasata/.env
COPY Makefile /wasata/Makefile
COPY entrypoint.sh wasata/entrypoint.sh

CMD ["make"]

RUN chmod +x wasata/entrypoint.sh

ENTRYPOINT ["./wasata/entrypoint.sh"]
