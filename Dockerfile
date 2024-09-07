FROM ubuntu:22.04

WORKDIR /app

RUN apt update 
RUN apt install -y python3 python3-pip python3-xapian libxapian-dev
RUN pip install fastapi["standard"]

COPY embeddedsearch/ ./embeddedsearch

EXPOSE 8000
CMD [ "python3","embeddedsearch/main.py" ]
