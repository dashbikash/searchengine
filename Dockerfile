FROM ubuntu:22.04

WORKDIR /app

COPY embeddedsearch/ ./embeddedsearch 
COPY requirements.txt ./
RUN apt update -y && \
    apt upgrade -y && \
    apt install python3 python3-pip python3-xapian libxapian-dev -y --no-install-recommends && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt  --no-cache-dir

EXPOSE 8000
CMD [ "python3","embeddedsearch/main.py" ]
