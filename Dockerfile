FROM python:3.11

WORKDIR /module_8_drf

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

