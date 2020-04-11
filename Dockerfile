FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install fastapi uvicorn psycopg2 sqlalchemy pydantic alembic numpy pytz pandas python-multipart

COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app

ADD requirements.txt .
RUN pip install -r requirements.txt

CMD bash -c "alembic upgrade head && python app/initial_data.py && uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8080}"