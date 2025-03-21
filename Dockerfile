FROM python:3.10-slim

# Set working directory
WORKDIR /gradio_app.py

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for temporary audio files
RUN mkdir -p /gradio_app.py/temp_audio && chmod 777 /gradio_app.py/temp_audio

# Expose the port Gradio runs on
EXPOSE 7863

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:7863/ || exit 1

# Environment variables (will be overridden by docker-compose)
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7863

# Command to run the application
CMD ["python", "gradio_app.py"]