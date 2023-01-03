FROM python:3.8

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

EXPOSE 5000
ENTRYPOINT ["python3","server.py"]
