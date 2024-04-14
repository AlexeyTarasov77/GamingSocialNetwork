FROM python:3.12-slim

WORKDIR /service

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN apt update && apt install -y postgresql-client build-essential postgresql-server-dev-all 

RUN apt install -y python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .

# RUN adduser --disabled-password service-user && chmod -R +w .

EXPOSE 8000

# USER service-user

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1