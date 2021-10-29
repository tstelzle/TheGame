FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install build-essential python-dev -y

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN pip install uwsgi

COPY . /app

CMD ["uwsgi", "--http", ":9201", "--enable-threads", "--wsgi-file", "server.py"]