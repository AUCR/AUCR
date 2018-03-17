FROM python:3-alpine AS AUCR
MAINTAINER Wyatt Roersma <wyattroersma@gmail.com>

RUN mkdir /opt
RUN mkdir /opt/aucr/
COPY aucr.py /opt/aucr
COPY app /opt/aucr/app
COPY serve.py /opt/aucr
COPY serve.py /opt/aucr
COPY babel.cfg /opt/aucr
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY requirements.txt /opt/aucr
COPY config.py /opt/aucr

ENV FLASK_APP=aucr.py

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
  && pip install -r requirements.txt \
  && apk del --purge gcc \
    libc-dev \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    py-pillow \
    openssl-dev

CMD ["flask", "run", "--host=0.0.0.0"]
