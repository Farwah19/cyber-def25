# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model and inference script
COPY model.pkl .
COPY inference.py .

# Create input and output directories
RUN mkdir -p /input/logs /output

# Set the default command to run the inference script
CMD ["python", "inference.py"]
