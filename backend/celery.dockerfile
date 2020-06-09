FROM python:3.7

RUN pip install fastapi uvicorn psycopg2 sqlalchemy pydantic alembic numpy pytz pandas python-multipart celery future

COPY app /app/app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=0

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY app /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]