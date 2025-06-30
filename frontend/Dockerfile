# Use the official Python image as a base image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Add the app directory to the PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy the dependencies file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies as root
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Create a non-root user for security
# No home directory is created, which is fine since we run from /app
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Switch to the non-root user to run the application
USER appuser

# Set the command to run the application
CMD ["panel", "serve", "app/main.py", "--address", "0.0.0.0", "--port", "8001", "--autoreload"] 