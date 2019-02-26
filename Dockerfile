FROM python:3.7-alpine AS aucr

MAINTAINER Wyatt Roersma <wyatt@aucr.io>

RUN mkdir /opt/aucr/

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
    libffi-dev \
    py-pillow \
    python3-dev \
    openldap-dev \
    openssl \
    file \
    jansson \
    bison \
    tini \
    su-exec \
    g++ \
    lapack-dev \
    gfortran \
    build-base \
    git \
    p7zip \
  && pip install -r /opt/aucr/requirements.txt --upgrade \
  && apk del --purge gcc \
    libc-dev \
    musl-dev \
    linux-headers \
    libffi-dev \
    py-pillow \
    gfortran \
    g++ \
    python3-dev \
    build-base \
    openldap-dev \
    gcc \
    git

COPY aucr.py /opt/aucr
COPY aucr_app /opt/aucr/aucr_app
COPY babel.cfg /opt/aucr
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY config.py /opt/aucr
COPY upload /opt/aucr/upload

RUN mkdir /opt/aucr/migrations

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
