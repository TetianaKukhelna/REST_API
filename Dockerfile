FROM python:3.9.9-slim

RUN apt-get update \
    && apt-get clean

WORKDIR /app

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 3889
