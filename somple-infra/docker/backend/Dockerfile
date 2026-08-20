FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system somple && adduser --system --ingroup somple somple

COPY somple-backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY somple-backend/ .

RUN chown -R somple:somple /app
USER somple

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
