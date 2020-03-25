FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install fastapi uvicorn

COPY ./app /app

ADD requirements.txt .
RUN pip install -r requirements.txt

CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-8080}