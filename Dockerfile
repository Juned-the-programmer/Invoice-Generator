# Use an official lightweight Python image
FROM python:3.12

# Install system dependencies (for WeasyPrint, if needed)
RUN apt-get update && apt-get install -y \
    libpangocairo-1.0-0 \
    libcairo2 \
    libpangoft2-1.0-0 \
    libjpeg62-turbo \
    libgif7 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Django port
EXPOSE 8000

# Start the Django app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "InvoiceGenerator.wsgi"]
