FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install fastapi uvicorn psycopg2 sqlalchemy pydantic alembic numpy pytz pandas python-multipart celery tenacity

COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start_tests.sh /start_tests.sh
RUN chmod +x /start_tests.sh

ENV PYTHONUNBUFFERED=0

CMD bash -c "/start.sh && uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8080}"