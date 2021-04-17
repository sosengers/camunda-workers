FROM python:3.8.6

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

RUN mkdir camunda_diagram

COPY bpmn/ /camunda_diagram

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["./entrypoint.sh"]
