FROM python:3.11-slim
WORKDIR /app
# PostgreSQL için sistem kütüphanelerini yükle
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]