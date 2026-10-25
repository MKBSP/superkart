FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy app.py and requirements.txt into the container
COPY . .

# Install dependencies without cache to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Run Streamlit on port 8501, open to outside connections
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
