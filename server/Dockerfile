FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install build-essential python-dev -y

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

RUN pip3 install uwsgi

COPY . /app

CMD ["uwsgi", "--http", ":9201", "--wsgi-file", "server.py"]