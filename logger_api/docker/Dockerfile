FROM python:3.11-alpine

EXPOSE 5001

ENV WORKING_DIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR $WORKING_DIR

COPY app $WORKING_DIR/app
COPY tests $WORKING_DIR/tests

ENTRYPOINT ["flask", "--app", "app", "run", "--port=5001", "--host=0.0.0.0"]