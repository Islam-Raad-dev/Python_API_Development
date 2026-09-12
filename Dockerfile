FROM python:3.12.3

WORKDIR /usr/src/backend/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .