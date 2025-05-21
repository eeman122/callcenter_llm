FROM python:3.9-slim

WORKDIR /app

# Explicitly expose port (matches what your app uses)
EXPOSE $PORT

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
