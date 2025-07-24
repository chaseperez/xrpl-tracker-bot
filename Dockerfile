# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install system dependencies needed for some python packages
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev make && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of your app source code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 8000

# Command to run your bot
CMD ["python", "backend/bot.py"]
