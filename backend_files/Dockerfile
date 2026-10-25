# same Python version as Colab
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy app.py, requirements.txt and the model into the container
COPY . .

# Install dependencies without cache to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Start the API with gunicorn: 4 workers, port 7860, the "superkart_api" object in app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
