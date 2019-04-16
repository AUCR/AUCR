FROM python:3.7-alpine AS aucr

MAINTAINER Wyatt Roersma <wyatt@aucr.io>
RUN adduser -D aucr
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
    postgresql-dev \
  && pip install psycopg2-binary \
  && pip install -r /opt/aucr/requirements.txt \
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
    gcc \
    git

COPY aucr.py /opt/aucr
COPY aucr_app /opt/aucr/aucr_app
COPY babel.cfg /opt/aucr
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY config.py /opt/aucr
COPY upload /opt/aucr/upload
COPY migrations /opt/aucr/migrations
COPY boot.sh  /opt/aucr/
RUN chmod a+x /opt/aucr/boot.sh
RUN chown -R aucr:aucr /opt/
USER aucr

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
