FROM ubuntu:22.04

WORKDIR /app

RUN apt update 
RUN apt install -y python3 python3-pip python3-xapian libxapian-dev
RUN apt autoclean


COPY embeddedsearch/ ./embeddedsearch
COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt  --no-cache-dir 

EXPOSE 8000
CMD [ "python3","embeddedsearch/main.py" ]
