FROM ubuntu:14.04

RUN apt-get update && apt-get install -fqq python
RUN mkdir /code

COPY server.py /code/server.py
COPY client.py /code/client.py
COPY driver.py /code/driver.py
