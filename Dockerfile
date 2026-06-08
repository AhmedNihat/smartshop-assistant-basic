FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY 09_fastapi_chat.py .
COPY smartshop_policy.pdf .

EXPOSE 8000

CMD ["uvicorn", "09_fastapi_chat:app", "--host", "0.0.0.0", "--port", "8000"]