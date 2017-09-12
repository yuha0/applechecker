FROM python:alpine

ADD * /work/

WORKDIR /work/
ENTRYPOINT ["python", "check.py"]
