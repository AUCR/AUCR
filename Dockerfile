FROM python:3.6-alpine AS aucr

MAINTAINER Wyatt Roersma <wyatt@aucr.io>

ENV SURICATA_VERSION 4.1.0

RUN apk add --no-cache \
    suricata


ENV YARA_VERSION 3.8.1

RUN apk add --no-cache \
    openssl \
    file \
    jansson \
    bison \
    python \
    tini \
    su-exec

RUN apk add --no-cache -t .build-deps \
    py-setuptools \
    openssl-dev \
    jansson-dev \
    python-dev \
    build-base \
    libc-dev \
    file-dev \
    automake \
    autoconf \
    libtool \
    flex \
    git \
  && set -x \
  && echo "Install Yara from source..." \
  && cd /tmp/ \
  && git clone --recursive --branch v$YARA_VERSION https://github.com/VirusTotal/yara.git \
  && cd /tmp/yara \
  && ./bootstrap.sh \
  && sync \
  && ./configure --with-crypto \
                 --enable-magic \
                 --enable-cuckoo \
                 --enable-dotnet \
  && make \
  && make install \
  && echo "Install yara-python..." \
  && cd /tmp/ \
  && git clone --recursive --branch v$YARA_VERSION https://github.com/VirusTotal/yara-python \
  && cd yara-python \
  && python setup.py build --dynamic-linking \
  && python setup.py install \
  && rm -rf /tmp/* \
  && apk del --purge .build-deps

RUN mkdir /opt
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
    python \
    tini \
    su-exec \
    g++ \
    lapack-dev \
    gfortran \
    build-base \
  && pip install cython \
  && pip install --upgrade pip \
  && pip install --no-cache-dir mmbot \
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
    gcc

COPY aucr.py /opt/aucr
COPY aucr_app /opt/aucr/aucr_app
COPY babel.cfg /opt/aucr
COPY LICENSE /opt/aucr
COPY projectinfo.yml /opt/aucr
COPY config.py /opt/aucr
COPY migrations /opt/aucr/migrations


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
