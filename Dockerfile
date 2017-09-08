FROM python:alpine

ADD check.py .
RUN pip install --no-cache-dir requests

CMD python check.py $MODEL $ZIP $SEC $DEST $LOGIN $PASS
