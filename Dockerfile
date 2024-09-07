# Use the official Python image
FROM python:3.9-slim

# Set working directory inside the Docker container
WORKDIR /app

# Copy all files from your GitHub repo into the Docker container
COPY . .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080, which is used by the Flask app to serve requests
EXPOSE 8080

# Command to run your Flask app when the Docker container starts
CMD ["python", "app.py"]
