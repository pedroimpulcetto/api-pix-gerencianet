FROM ubuntu:18.04

WORKDIR /code

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

COPY . /code

RUN pip3 install --no-cache-dir -r requirements.txt

CMD python3 src/main.py

EXPOSE 5000