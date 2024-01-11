FROM python:3.11.7-alpine

COPY requirements.txt /requirements.txt
COPY entrypoint.sh /entrypoint.sh
COPY App /App

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
RUN pip install --no-deps ruamel.yaml

ENTRYPOINT ["/entrypoint.sh"]