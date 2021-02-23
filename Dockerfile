FROM python:3.8.6

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./workers workers/
COPY ./model model/
COPY ./main.py main.py

CMD ["python3", "main.py"]
