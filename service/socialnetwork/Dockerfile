FROM python:3.12-slim

WORKDIR /service

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN apt update && apt install -y postgresql-client build-essential postgresql-server-dev-all python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 gettext

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .

# RUN adduser --disabled-password service-user && chmod -R +w .

EXPOSE 8000

# USER service-user

# CMD ["stripe", "listen", "--forward-to", "localhost:8000/payment/stripe/webhook/"]

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1