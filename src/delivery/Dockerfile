FROM python:3.7-alpine

RUN apk add build-base

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN pip --no-cache-dir install -r requirements.txt

CMD ["python", "delivery_app.py"]