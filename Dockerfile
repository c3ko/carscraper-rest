FROM python:3.7-alpine3.8

RUN mkdir -p /opt/services/flaskapp/src

WORKDIR /opt/services/flaskapp/src

COPY requirements_freeze.txt requirements_freeze.txt

RUN apk add -U --no-cache gcc build-base linux-headers \
    ca-certificates python3-dev libffi-dev libressl-dev libxslt-dev
RUN apk add sqlite
RUN python -m venv env
RUN env/bin/pip3 install -r requirements_freeze.txt
RUN env/bin/pip3 install gunicorn


COPY carscraper carscraper
COPY app.py db.py models.py resources.py settings.py ./
COPY start.sh ./
RUN chmod +x start.sh
ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./start.sh"]
