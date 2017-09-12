FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-pip python-dev build-essential && rm -rf /var/lib/apt/lists/*

COPY app /app
WORKDIR /app

RUN pip install -r submitter/requirements.txt

CMD ["python", "/app/submitter.py"]