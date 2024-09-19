FROM ubuntu:22.04

WORKDIR /app

COPY searchengine/ ./searchengine
COPY config/ ./config 

COPY requirements.txt ./
RUN apt update -y && \
    apt upgrade -y && \
    apt install python3 python3-pip python3-xapian libxapian-dev -y --no-install-recommends && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt  --no-cache-dir

EXPOSE 8619
CMD [ "python3","searchengine/main.py" ]
