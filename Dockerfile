FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Hugging Face Spaces require port 7860
EXPOSE 7860

# Run the web server to keep the space alive and answer pings
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]