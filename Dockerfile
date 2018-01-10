FROM python:3

COPY . /opt/aucr
WORKDIR /opt/aucr

CMD ["python", "aucr.py"]
