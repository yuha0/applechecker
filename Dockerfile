FROM ubuntu:14.04

WORKDIR /usr/local/bin
COPY stock.py .
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
 && pip install requests \
 && rm -rf /var/lib/apt/lists/*

CMD python -u stock.py $MODEL $ZIP $DEST $SEC $LOGIN $PASS
