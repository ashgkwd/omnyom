FROM python:3.12 AS builder

WORKDIR /code

RUN apt-get update \
    && apt-get -y install libpq-dev cron

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "-c"]
CMD ["python wsgi.py"]
