FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install requirements.txt

COPY ./app /app

CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-8080}