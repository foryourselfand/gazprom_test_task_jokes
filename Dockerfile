FROM python:3.7-slim
MAINTAINER foryourselfand

# Start Installing the Basic Dependencies
RUN pip install --upgrade pip

RUN mkdir -p /sanic/config
RUN mkdir -p /sanic/gazprom_test_task_jokes

COPY config/ /sanic/config/
COPY gazprom_test_task_jokes/ /sanic/gazprom_test_task_jokes/
COPY requirements.txt /sanic
COPY run.py /sanic
COPY .env /sanic

RUN pip install -r /sanic/requirements.txt

WORKDIR /sanic

RUN find . -type f

EXPOSE ${SANIC_PORT}

ENTRYPOINT ["python", "run.py"]

