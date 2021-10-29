FROM python:3
WORKDIR /usr/src

COPY requirements.txt /usr/src
RUN pip install -r requirements.txt

COPY . /usr/src

CMD ["python", "server.py"]