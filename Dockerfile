FROM python:3-alpine AS AUCR

MAINTAINER Wyatt Roersma <wyattroersma@gmail.com>

RUN mkdir /opt
RUN mkdir /opt/aucr/
RUN mkdir /opt/aucr/upload

ENV FLASK_APP=aucr.py

COPY requirements.txt /opt/aucr


WORKDIR /opt/aucr

RUN apk update
RUN apk upgrade

RUN apk add --no-cache \
    gcc \
    libc-dev \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    py-pillow \
    openssl-dev \
  && pip install -r /opt/aucr/requirements.txt --upgrade \
  && apk del --purge gcc \
    libc-dev \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    py-pillow \
    openssl-dev


COPY aucr.py /opt/aucr
COPY aucr_app /opt/aucr/aucr_app
COPY babel.cfg /opt/aucr
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY config.py /opt/aucr
COPY migrations /opt/aucr/migrations/

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
